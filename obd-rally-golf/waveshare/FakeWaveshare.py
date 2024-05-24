import time
import random

class FakeWaveshare:
    def __init__(self):
        # Initialize with a base latitude and longitude
        self.base_latitude = 48.123
        self.base_longitude = 16.321

    def getGPS(self, callback):
        time.sleep(2)  # Simulate delay in getting GPS data
        
        # Generate small random adjustments
        # Assuming maximum deviation of 0.001 degrees for both latitude and longitude
        adjustment = 0.001
        latitude_variation = random.uniform(-adjustment, adjustment)
        longitude_variation = random.uniform(-adjustment, adjustment)
        
        # Calculate new coordinates with random adjustments
        new_latitude = self.base_latitude + latitude_variation
        new_longitude = self.base_longitude + longitude_variation
        
        # Call the callback with the new adjusted coordinates
        callback(new_latitude, new_longitude)
