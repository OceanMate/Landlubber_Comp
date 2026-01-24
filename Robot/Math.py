import math

class Math:
    @staticmethod
    def clamp(value, min_value, max_value):
        return max(min_value, min(value, max_value))
    
    @staticmethod
    def pitch_from_quat(quanternion: tuple[float, float, float, float]) -> float:
        x, y, z, w = quanternion
        # Pitch (x-axis rotation)
        sinp = 2 * (w * x + y * z)
        cosp = 1 - 2 * (x * x + y * y)
        pitch = math.atan2(sinp, cosp)
        return math.degrees(pitch)
    
    @staticmethod
    def roll_from_quat(quanternion: tuple[float, float, float, float]) -> float:
        x, y, z, w = quanternion
        # Roll (y-axis rotation)
        sinr = 2 * (w * y - z * x)
        sinr = Math.clamp(sinr, -1, 1)  # Clamp to avoid invalid input to asin
        roll = math.asin(sinr)
        return math.degrees(roll)