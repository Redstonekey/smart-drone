import random
import math
import time
import threading # Import threading for running simulation in a separate thread

class GPS:
    def __init__(self, simulation_duration=60, update_interval=10):
        """
        Initializes the GPS simulator with a random starting position
        and starts the simulation task in a separate thread.

        Args:
            simulation_duration (float): How long the simulation should run in seconds.
            update_interval (float): How often to generate new movement parameters and update position in seconds.
        """
        # Initialize position
        self._x = 50.05496601675741
        self._y = 8.784217182244461
        self._z = 144.0

        # Initialize movement parameters (will be set by generate_movement_parameters)
        self._speed = 0  # Horizontal speed
        self._direction = 0 # Direction in radians (0 to 2*pi)
        self._vertical_speed = 0 # Vertical speed

        # Flag to control the simulation loop
        self._running = True

        print(f"Initial Position: x={self._x:.2f}, y={self._y:.2f}, z={self._z:.2f}")

        # Start the simulation in a separate thread
        self._simulation_thread = threading.Thread(
            target=self._simulate_movement_thread,
            args=(simulation_duration, update_interval),
            daemon=True # Set as daemon thread so it exits when the main program exits
        )
        self._simulation_thread.start()

    def get_position(self):
        """
        Returns the current simulated GPS coordinates.

        Returns:
            dict: A dictionary containing the current 'x', 'y', and 'z' coordinates.
        """
        return {"x": self._x, "y": self._y, "z": self._z}

    def generate_movement_parameters(self):
        """
        Generates new random speed, horizontal direction, and vertical speed.
        """
        # Generate a random horizontal speed (e.g., between 0 and 10 units per second)
        self._speed = random.uniform(0, 10)

        # Generate a random horizontal direction (angle in radians, 0 to 2*pi)
        self._direction = random.uniform(0, 2 * math.pi)

        # Generate a random vertical speed (e.g., between -1 and 1 units per second)
        self._vertical_speed = random.uniform(-1, 1)

        print(f"Generated new movement parameters: Speed={self._speed:.2f}, Direction={math.degrees(self._direction):.2f} deg, Vertical Speed={self._vertical_speed:.2f}")

    def update_position(self, time_delta):
        """
        Updates the current position based on the current speed, direction,
        vertical speed, and the elapsed time (time_delta).

        Args:
            time_delta (float): The time elapsed since the last update (in seconds).
        """
        # Calculate displacement in x and y based on horizontal speed and direction
        dx = self._speed * math.cos(self._direction) * time_delta
        dy = self._speed * math.sin(self._direction) * time_delta

        # Calculate displacement in z based on vertical speed
        dz = self._vertical_speed * time_delta

        # Update position
        self._x += dx
        self._y += dy
        self._z += dz

        print(f"Position after {time_delta} seconds: x={self._x:.2f}, y={self._y:.2f}, z={self._z:.2f}")

    def _simulate_movement_thread(self, simulation_duration, update_interval):
        """
        Simulates the GPS movement in a separate thread.
        This method runs the simulation loop.

        Args:
            simulation_duration (float): Total time to run the simulation.
            update_interval (float): Time between generating new parameters and updating position.
        """
        start_time = time.time()
        last_update_time = start_time

        print(f"\nStarting threaded GPS simulation for {simulation_duration} seconds...")

        while self._running and (time.time() - start_time) < simulation_duration:
            current_time = time.time()
            elapsed_since_last_update = current_time - last_update_time

            # Check if it's time for the next update interval
            if elapsed_since_last_update >= update_interval:
                # Generate new movement parameters for the next interval
                self.generate_movement_parameters()

                # Update position based on movement over the just completed interval
                # Use the fixed update_interval as the time delta for the position update
                self.update_position(update_interval)

                # Advance last_update_time by update_interval
                last_update_time += update_interval

                # If current_time is significantly past last_update_time (due to potential delays),
                # advance last_update_time further to catch up for future intervals.
                while current_time - last_update_time >= update_interval:
                     last_update_time += update_interval

            # Calculate time until the next scheduled update interval check
            time_until_next_check = (last_update_time + update_interval) - current_time

            # Calculate remaining simulation time
            remaining_simulation_time = (start_time + simulation_duration) - current_time

            # Time to sleep is the minimum of time until next check and remaining simulation time
            time_to_sleep = min(time_until_next_check, remaining_simulation_time)

            # Ensure time_to_sleep is not negative and not excessively large
            time_to_sleep = max(0.01, time_to_sleep) # Sleep at least 10ms to avoid busy-waiting

            # If remaining time is very small, break the loop
            if remaining_simulation_time <= 0:
                 break

            # Sleep until the next event or check for stop signal
            time.sleep(time_to_sleep)


        print("\nThreaded GPS simulation finished.")
        self._running = False # Ensure running flag is false when simulation ends

    def stop_simulation(self):
        """
        Signals the simulation thread to stop.
        """
        self._running = False
        # In a real application, you might want to join the thread here
        # to wait for it to finish, but for a daemon thread in a simple
        # script, relying on the main process exit is often sufficient.
