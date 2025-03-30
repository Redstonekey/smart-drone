import random

class GPS:
    def __init__(self):
        self.update_position()

    def update_position(self):
        """Update current position with random values"""
        self._x = random.uniform(-100, 100)  # Random x between -100 and 100
        self._y = random.uniform(-100, 100)  # Random y between -100 and 100
        self._z = random.uniform(0, 50)      # Random altitude between 0 and 50

    def get_position(self):
        """Get current position as (x, y, z)"""
        self.update_position()
        return (self._x, self._y, self._z)

    def get_x(self):
        """Get current x coordinate"""
        self.update_position()
        return self._x

    def get_y(self):
        """Get current y coordinate"""
        self.update_position()
        return self._y

    def get_z(self):
        """Get current altitude"""
        self.update_position()
        return self._z

    def get_xy(self):
        """Get current x,y coordinates"""
        self.update_position()
        return (self._x, self._y)