import cv2
import numpy as np
from ultralytics import YOLO
import time
import math
from flask import Flask, Response, render_template_string # Import Flask components
import threading # To run Flask server and video processing concurrently
import queue # To safely pass frames between threads

# --- Configuration for Tracking ---
MODEL_PATH = "yolov8n.pt"
CONF_THRESHOLD_NEW_DETECTION = 0.5 # Minimum confidence to consider a new detection for tracking
IOU_THRESHOLD = 0.7              # Minimum IoU to match a new detection with an existing track
REQUIRED_MATCHED_FRAMES = 4      # Minimum number of frames an object must be *matched* for confirmation
MAX_MISSING_FRAMES_TOLERANCE = 10 # Number of frames a track can persist *without* a match before being dropped
DISPLAY_CONFIRMED_ONLY = True   # Set to False to see all potential tracks + confirmed highlights (tracking boxes)

# --- Configuration for Camera Motion Detection ---
# Feature Detection (ORB)
MAX_FEATURES = 5000              # Maximum number of features to detect
ORB_SCALE_FACTOR = 1.2
ORB_N_LEVELS = 8

# Optical Flow (Lucas-Kanade)
LK_PARAMS = dict(winSize=(21, 21),
                 maxLevel=3,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

# Transformation Estimation (Affine)
MIN_POINTS_FOR_MOTION_EST = 10 # Minimum number of good feature points needed to estimate motion

# Camera Motion Thresholds (pixels/degrees)
MIN_TRANSLATION_THRESHOLD = 2.0 # Minimum pixel movement in x or y to detect translation
MAX_ROTATION_THRESHOLD = 1.0   # Maximum rotation (in degrees) allowed for pure translation
MIN_ROTATION_THRESHOLD = 0.5   # Minimum rotation (in degrees) to detect rotation (beyond noise)

# Object Exclusion Zone Expansion
BOX_EXPANSION_PERCENTAGE = 20    # Expand box by 20% (10% on each side) when filtering points

# --- Streaming Configuration ---
FLASK_PORT = 4999
FLASK_HOST = '0.0.0.0' # Use '0.0.0.0' to make server accessible externally, '127.0.0.1' for local only
MJPEG_BOUNDARY = b'frame' # Boundary string for MJPEG stream

# --- Helper function for IoU ---
def iou(box1, box2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    Boxes are expected in [x1, y1, x2, y2] format.
    """
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection_area = max(0, x2 - x1) * max(0, y2 - y1)

    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    union_area = box1_area + box2_area - intersection_area

    if union_area == 0:
        return 0
    return intersection_area / union_area

# --- Helper function to expand box ---
def expand_box(box, frame_width, frame_height, percentage):
    """Expands a bounding box by a percentage, keeping it within frame bounds."""
    x1, y1, x2, y2 = box
    w, h = x2 - x1, y2 - y1
    exp_w = w * percentage / 100
    exp_h = h * percentage / 100

    new_x1 = x1 - exp_w / 2
    new_y1 = y1 - exp_h / 2
    new_x2 = x2 + exp_w / 2
    new_y2 = y2 + exp_h / 2

    new_x1 = max(0.0, new_x1)
    new_y1 = max(0.0, new_y1)
    new_x2 = min(float(frame_width), new_x2)
    new_y2 = min(float(frame_height), new_y2)

    return [new_x1, new_y1, new_x2, new_y2]

# --- Check if a point is inside an expanded box ---
def is_point_inside_expanded_box(point, box, frame_width, frame_height, percentage):
    """Checks if a point (x, y) is inside the expanded version of a box."""
    x, y = point
    expanded_x1, expanded_y1, expanded_x2, expanded_y2 = expand_box(box, frame_width, frame_height, percentage)

    return x >= expanded_x1 and x <= expanded_x2 and y >= expanded_y1 and y <= expanded_y2

# --- Data structure for tracking objects ---
# This will be managed inside the video processing thread
# {
#   'label': 'person',
#   'last_box': [x1, y1, x2, y2],
#   'total_matched_frames': 1,
#   'frames_since_last_match': 0,
#   'first_conf': 0.95
# }
tracked_objects = []

# --- Variables for Camera Motion Detection ---
orb = cv2.ORB_create(nfeatures=MAX_FEATURES, scaleFactor=ORB_SCALE_FACTOR, nlevels=ORB_N_LEVELS)
prev_gray_cam = None
prev_points_cam = None

# --- Queue to pass frames to Flask ---
output_frame_queue = queue.Queue(maxsize=1) # Use a queue with size 1 to keep only the latest frame

# --- Flask App Setup ---
app = Flask(__name__)

# HTML template for the landing page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>YOLOv8 Tracking & Camera Motion Stream</title>
</head>
<body>
    <h1>Live Video Feed</h1>
    <img src="{{ url_for('video_feed') }}" width="100%">
</body>
</html>
"""

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Streams MJPEG."""
    return Response(generate_frames(),
                    mimetype=f'multipart/x-mixed-replace; boundary={MJPEG_BOUNDARY.decode()}')

def generate_frames():
    """Generates JPEG frames for the MJPEG stream."""
    while True:
        # Get the latest frame from the processing queue
        try:
            frame = output_frame_queue.get(timeout=0.4) # Wait up to 1 second for a frame
        except queue.Empty:
            # If no frame in the queue after timeout, continue loop (prevents blocking forever)
            # Or you could send a blank frame or error image
            continue

        if frame is not None:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue # Skip frame if encoding failed

            frame_bytes = buffer.tobytes()

            # Yield frame in MJPEG format
            yield (b'--' + MJPEG_BOUNDARY + b'\r\n'
                   b'Content-Type: image/jpeg\r\n'
                   b'Content-Length: ' + str(len(frame_bytes)).encode() + b'\r\n'
                   b'\r\n' + frame_bytes + b'\r\n')
        else:
             # Optionally yield a blank frame or wait if the queue gave None
             time.sleep(0.01) # Prevent busy-waiting


# --- Video Processing Function (to run in a separate thread) ---
def process_video():
    """Captures video, performs detection/tracking, and puts frames in a queue."""
    global tracked_objects, prev_gray_cam, prev_points_cam # Use globals

    # Open webcam - moved inside the thread function
    cap = cv2.VideoCapture(0) # Use 0 for default camera
    if not cap.isOpened():
        print("Error: Could not open webcam in processing thread.")
        # Indicate error to main thread or Flask app if needed
        # For simplicity, just exit thread
        return

    # Get frame dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Processing thread: Webcam opened {frame_width}x{frame_height}")

    model_process_thread = YOLO(MODEL_PATH).cuda() # Load model in the thread

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Processing thread: Cannot receive frame (stream end?). Exiting ...")
            break

        # Convert to grayscale for motion detection
        gray_cam = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- 1. Run YOLO detection ---
        results = model_process_thread(frame, imgsz=640, verbose=False)[0]

        current_frame_detections = []
        if results.boxes:
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                label = model_process_thread.names[cls_id]
                if conf >= CONF_THRESHOLD_NEW_DETECTION:
                     current_frame_detections.append({
                         'box': [x1, y1, x2, y2],
                         'conf': conf,
                         'cls_id': cls_id,
                         'label': label
                     })

        # --- 2. Update Object Tracking ---
        # (Logic is the same as before, using current_frame_detections)
        next_tracked_objects = []
        matched_current_indices = set()

        for tracked_obj in tracked_objects:
            best_match_index = -1
            best_match_iou = IOU_THRESHOLD
            for i, current_det in enumerate(current_frame_detections):
                if i in matched_current_indices: continue
                if current_det['label'] == tracked_obj['label']:
                     current_iou = iou(tracked_obj['last_box'], current_det['box'])
                     if current_iou > best_match_iou:
                         best_match_iou = current_iou
                         best_match_index = i

            if best_match_index != -1:
                matched_current_indices.add(best_match_index)
                matched_detection = current_frame_detections[best_match_index]
                updated_tracked_obj = {
                    'label': tracked_obj['label'],
                    'last_box': matched_detection['box'],
                    'total_matched_frames': tracked_obj['total_matched_frames'] + 1,
                    'frames_since_last_match': 0,
                    'first_conf': tracked_obj['first_conf']
                }
                next_tracked_objects.append(updated_tracked_obj)
            else:
                tracked_obj['frames_since_last_match'] += 1
                if tracked_obj['frames_since_last_match'] <= MAX_MISSING_FRAMES_TOLERANCE:
                    next_tracked_objects.append(tracked_obj)

        for i, current_det in enumerate(current_frame_detections):
            if i not in matched_current_indices:
                 new_tracked_obj = {
                     'label': current_det['label'],
                     'last_box': current_det['box'],
                     'total_matched_frames': 1,
                     'frames_since_last_match': 0,
                     'first_conf': current_det['conf']
                 }
                 next_tracked_objects.append(new_tracked_obj)
        tracked_objects = next_tracked_objects # Update the global list

        # --- 3. Camera Motion Estimation ---
        camera_motion_text = "No Camera Motion"

        if prev_gray_cam is not None and prev_points_cam is not None:
            curr_points_cam, status, err = cv2.calcOpticalFlowPyrLK(prev_gray_cam, gray_cam, prev_points_cam, None, **LK_PARAMS)
            good_prev_points = []
            good_curr_points = []

            if curr_points_cam is not None:
                 for i, (curr_pt, stat) in enumerate(zip(curr_points_cam, status)):
                     if stat[0] == 1:
                         prev_pt = prev_points_cam[i]
                         (x_curr, y_curr) = curr_pt.ravel()
                         (x_prev, y_prev) = prev_pt.ravel()

                         is_inside_expanded_object = False
                         for det in current_frame_detections:
                             if is_point_inside_expanded_box((x_prev, y_prev), det['box'], frame_width, frame_height, BOX_EXPANSION_PERCENTAGE) or \
                                is_point_inside_expanded_box((x_curr, y_curr), det['box'], frame_width, frame_height, BOX_EXPANSION_PERCENTAGE):
                                 is_inside_expanded_object = True
                                 break
                         if not is_inside_expanded_object:
                             good_prev_points.append(prev_pt)
                             good_curr_points.append(curr_pt)

            if len(good_prev_points) >= MIN_POINTS_FOR_MOTION_EST:
                M, _ = cv2.estimateAffinePartial2D(np.array(good_prev_points), np.array(good_curr_points))
                if M is not None:
                    tx = M[0, 2]
                    ty = M[1, 2]
                    rotation_rad = math.atan2(M[1, 0], M[0, 0])
                    rotation_deg = math.degrees(rotation_rad)

                    abs_tx = abs(tx)
                    abs_ty = abs(ty)
                    abs_rotation_deg = abs(rotation_deg)

                    if abs_tx > MIN_TRANSLATION_THRESHOLD or abs_ty > MIN_TRANSLATION_THRESHOLD:
                        if abs_rotation_deg < MAX_ROTATION_THRESHOLD:
                            camera_motion_text = f"Translate: ({tx:.2f}, {ty:.2f})"
                        else:
                             camera_motion_text = f"Translate & Rotate: ({tx:.2f}, {ty:.2f}, {rotation_deg:.2f}°)"
                    elif abs_rotation_deg > MIN_ROTATION_THRESHOLD:
                         camera_motion_text = f"Rotate: {rotation_deg:.2f}°"

        # --- Prepare for next frame: Detect and filter features ---
        curr_keypoints_cam, _ = orb.detectAndCompute(gray_cam, None)
        filtered_curr_points_cam = []
        if curr_keypoints_cam is not None:
            for kp in curr_keypoints_cam:
                (x, y) = kp.pt
                is_inside_expanded_object = False
                for det in current_frame_detections:
                    if is_point_inside_expanded_box((x, y), det['box'], frame_width, frame_height, BOX_EXPANSION_PERCENTAGE):
                        is_inside_expanded_object = True
                        break
                if not is_inside_expanded_object:
                    filtered_curr_points_cam.append(np.array([[x, y]], dtype=np.float32))

        if filtered_curr_points_cam:
             prev_points_cam = np.array(filtered_curr_points_cam).reshape(-1, 1, 2)
             prev_gray_cam = gray_cam.copy()
        else:
             prev_points_cam = None
             prev_gray_cam = None


        # --- 4. Draw Bounding Boxes and Motion Info on the Frame ---

        # Draw bounding boxes and labels for tracked objects
        # Use tracked_objects which is updated in this thread
        for tracked_obj in tracked_objects:
            x1, y1, x2, y2 = tracked_obj['last_box']
            label = tracked_obj['label']
            matched_count = tracked_obj['total_matched_frames']
            missing_count = tracked_obj['frames_since_last_match']

            is_confirmed = matched_count >= REQUIRED_MATCHED_FRAMES

            if DISPLAY_CONFIRMED_ONLY and not is_confirmed:
                continue

            color = (0, 255, 0) if is_confirmed else (0, 165, 255)
            text = f"{label} ({matched_count}M, {missing_count}ms)"

            x1, y1, x2, y2 = max(0, x1), max(0, y1), min(frame_width, x2), min(frame_height, y2)
            if x1 < x2 and y1 < y2:
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Display Camera Motion Status
        cv2.putText(frame, camera_motion_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2) # Yellow color

        # --- Put the processed frame into the queue for Flask ---
        try:
            # If queue is full, get the old frame first to make space for the new one
            if output_frame_queue.full():
                output_frame_queue.get_nowait()
            output_frame_queue.put_nowait(frame) # Put the new frame without blocking
        except queue.Full:
             # This should not happen with maxsize=1 and get_nowait/put_nowait
             # but as a safeguard, just pass
             pass
        except queue.Empty:
             # Should not happen in put_nowait, but catch just in case
             pass

    # --- Cleanup (inside the thread) ---
    cap.release()
    print("Processing thread: Webcam released.")


# --- Main execution block ---
if __name__ == '__main__':
    # Start the video processing in a separate thread
    video_thread = threading.Thread(target=process_video)
    video_thread.daemon = True # Allow main thread to exit even if this thread is running
    video_thread.start()

    # Start the Flask web server
    print(f"Starting Flask server on http://{FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False, threaded=True) # threaded=True allows multiple clients