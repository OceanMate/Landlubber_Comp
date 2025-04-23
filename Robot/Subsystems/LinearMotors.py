from jigboard.Jigboard import Jigboard
from structure.Subsystem import Subsystem
from transmission.ComsThread import ComsThread


# Max Forward speed for motors is .9 kg of thrust 
# Max Backward speed for motors is .8 kg of thrust
class LinearMotors(Subsystem):
    def __init__(self):
        super().__init__()
                
        self.FL = 0
        self.FR = 0
        self.BL = 0
        self.BR = 0
    
    # Runs the motors given the x, y, and z speeds (each from -1 to 1)
    def run_motors(self, xSpeed, ySpeed, zRotation):
        # calculate the absolute values
        abs_x = abs(xSpeed)
        abs_y = abs(ySpeed)
        abs_z = abs(zRotation)
        
        # Find the maximum of the absolute values
        maxXYZ = max([abs_x, abs_y, abs_z])
        
        # prevent division by zero
        if (maxXYZ == 0):
            # no movement
            self.stop_motors()
            return
        
        x_div_max = abs_x / maxXYZ
        y_div_max = abs_y / maxXYZ
        z_div_max = abs_z / maxXYZ
        
        # sum of the divided values
        total_sum = x_div_max + y_div_max + z_div_max

        # actual matrix input
        reducedX = xSpeed / total_sum
        reducedY = ySpeed / total_sum
        reducedZ = zRotation / total_sum

        # motor matrix output
        fl_speed = reducedX + reducedY + reducedZ
        fr_speed = reducedX - reducedY - reducedZ
        bl_speed = -reducedX + reducedY - reducedZ
        br_speed = -reducedX - reducedY + reducedZ
        
        self._set_motor_speeds(fl_speed, fr_speed, br_speed, bl_speed)
        
    
    def _set_motor_speeds(self, fl_speed, fr_speed, br_speed, bl_speed):
                
        self.FL = fl_speed * 0.888 if fl_speed > 0 else fl_speed
        self.FR = fr_speed * 0.888 if fr_speed > 0 else fr_speed
        self.BR = br_speed * 0.888 if br_speed > 0 else br_speed
        self.BL = bl_speed * 0.888 if bl_speed > 0 else bl_speed
        
        ComsThread().set_horizontal_motors(self.FL, self.FR, self.BR, self.BL)
        
    
    def stop_motors(self):
        self._set_motor_speeds(0, 0, 0, 0)
    
    def periodic(self):
        Jigboard().put_string("Linear Motor Speeds", "FL: {:.2f} FR: {:.2f} BL: {:.2f} BR: {:.2f}".format(self.FL, self.FR, self.BL, self.BR))

