from dashboard.Dashboard import Dashboard
from structure.Subsystem import Subsystem

class LinearMotors(Subsystem):
    def __init__(self):
        super().__init__()
        
        self.FL = 0
        self.FR = 0
        self.BR = 0
        self.BL = 0
    
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
            self._setMotor("FL", 0)
            self._setMotor("FR", 0)
            self._setMotor("BR", 0)
            self._setMotor("BL", 0)
            return

        # actual matrix input
        reducedX = xSpeed / total_sum
        reducedY = ySpeed / total_sum
        reducedZ = zRotation / total_sum

        # motor matrix output
        self.FL = reducedX + reducedY + reducedZ
        self.FR = reducedX - reducedY - reducedZ
        self.BR = reducedZ - reducedX - reducedY
        self.BL = reducedY - reducedX - reducedZ
        
        self._setMotor("FL", self.FL)
        self._setMotor("FR", self.FR)
        self._setMotor("BR", self.BR)
        self._setMotor("BL", self.BL)
          
    
    def _setMotor(self, motor, speed):
        # TODO define better
        pass
    
    def periodic(self):
        Dashboard().put_string("Motor Speeds", "FL: {:.2f} FR: {:.2f} BR: {:.2f} BL: {:.2f}".format(self.FL, self.FR, self.BR, self.BL), 10, 0)
