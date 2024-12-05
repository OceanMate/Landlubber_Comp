from jigboard.DashboardTab import DashboardTab
from jigboard.Jigboard import Jigboard
from structure.Subsystem import Subsystem
from transmission.Transmission import Transmission

class LinearMotors(Subsystem):
    def __init__(self):
        super().__init__()
        
        self.programmer_tab = DashboardTab("Programmer Party")
        
        self.FL = 0
        self.FR = 0
        self.BL = 0
        self.BR = 0
    
    # Runs the motors given the x, y, and z speeds (each from -1 to 1)
    def runMotors(self, xSpeed, ySpeed, zRotation):
        # calculate the absolute values
        abs_x = abs(xSpeed)
        abs_y = abs(ySpeed)
        abs_z = abs(zRotation)

        # Calculate the sum of absolute values
        total_sum = abs_x + abs_y + abs_z
        
        # prevent division by zero
        if (total_sum == 0):
            # no movement
            self.stop_motors()
            return

        # actual matrix input
        reducedX = xSpeed / total_sum
        reducedY = ySpeed / total_sum
        reducedZ = zRotation / total_sum

        # motor matrix output
        fl_speed = reducedX + reducedY + reducedZ
        fr_speed = reducedX - reducedY - reducedZ
        bl_speed = reducedY - reducedX - reducedZ
        br_speed = reducedZ - reducedX - reducedY
        
        self._set_motor_speeds(fl_speed, fr_speed, bl_speed, br_speed)
        
    
    def _set_motor_speeds(self, fl_speed, fr_speed, bl_speed, br_speed):
        self.FL = fl_speed
        self.FR = fr_speed
        self.BL = bl_speed
        self.BR = br_speed
        
        Transmission().set_linear_motor_speeds(fl_speed, fr_speed, bl_speed, br_speed)
        
    
    def stop_motors(self):
        self._set_motor_speeds(0, 0, 0, 0)
    
    def periodic(self):
        self.programmer_tab.put_string("Motor Speeds", "FL: {:.2f} FR: {:.2f} BR: {:.2f} BL: {:.2f}".format(self.FL, self.FR, self.BR, self.BL))
        Jigboard().put_string("Motor Speedz", "FL: {:.2f} FR: {:.2f} BR: {:.2f} BL: {:.2f}".format(self.FL, self.FR, self.BR, self.BL))

