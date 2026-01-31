import math

class Math:
    @staticmethod
    def clamp(value, min_value, max_value):
        return max(min_value, min(value, max_value))
    
    @staticmethod
    def pitch_from_quat(quanternion: tuple[float, float, float, float]) -> float:
        x, y, z, w = quanternion
        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        sinp = Math.clamp(sinp, -1, 1)  # Clamp to avoid invalid input to asin
        pitch = math.asin(sinp)
        return pitch
    
    @staticmethod
    def roll_from_quat(quanternion: tuple[float, float, float, float]) -> float:
        x, y, z, w = quanternion
        # Roll (x-axis rotation)
        sinr = 2 * (w * x + y * z)
        cosr = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr, cosr)
        return roll
    
    @staticmethod
    def euler_from_quat(quanternion: tuple[float, float, float, float]) -> tuple[float, float, float]:
        x, y, z, w = quanternion
        
        # Yaw (z-axis rotation)
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        
        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        sinp = Math.clamp(sinp, -1, 1)  # Clamp to avoid invalid input to asin
        pitch = math.asin(sinp)
        
        # Roll (x-axis rotation)
        sinr = 2 * (w * x + y * z)
        cosr = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr, cosr)
        
        return (yaw, pitch, roll)
    
    @staticmethod
    def degrees_from_radians(radians: float) -> float:
        return radians * (180.0 / math.pi)