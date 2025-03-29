import random
from time import sleep
from dataclasses import dataclass
from typing import Tuple

@dataclass
class GPSData:
    latitude: float
    longitude: float
    altitude: float
    satellites: int
    fix_quality: int

class GPSSensor:
    def __init__(self, initial_lat=48.137154, initial_lon=11.576124, initial_alt=520):
        self.current_lat = initial_lat
        self.current_lon = initial_lon
        self.current_alt = initial_alt
        self._connected = False

    def connect(self) -> bool:
        """Simulate GPS connection"""
        self._connected = True
        return True

    def disconnect(self) -> None:
        """Disconnect GPS"""
        self._connected = False

    def get_position(self) -> GPSData:
        """Simulate getting GPS position with small random variations"""
        if not self._connected:
            raise ConnectionError("GPS not connected")

        # Simulate slight position changes
        self.current_lat += random.uniform(-0.0001, 0.0001)
        self.current_lon += random.uniform(-0.0001, 0.0001)
        self.current_alt += random.uniform(-1, 1)

        return GPSData(
            latitude=self.current_lat,
            longitude=self.current_lon,
            altitude=self.current_alt,
            satellites=random.randint(6, 12),
            fix_quality=random.choice([1, 1, 1, 2])  # 1=GPS, 2=DGPS
        )

if __name__ == "__main__":
    # Example usage
    gps = GPSSensor()
    gps.connect()
    
    try:
        while True:
            position = gps.get_position()
            print(f"Lat: {position.latitude:.6f}, Lon: {position.longitude:.6f}, Alt: {position.altitude:.1f}m")
            print(f"Satellites: {position.satellites}, Fix Quality: {position.fix_quality}")
            sleep(1)
    except KeyboardInterrupt:
        gps.disconnect()