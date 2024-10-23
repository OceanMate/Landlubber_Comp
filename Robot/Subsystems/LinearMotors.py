from numpy import double
from Robot import Robot
from structure.Subsystem import Subsystem

class LinearMotors(Subsystem):
    def __init__(self):
        super().__init__(self.__class__.__name__)
    
    # Runs the motors given the x, y, and z speeds (each from -1 to 1)
    def runMotors(self, xSpeed : double, ySpeed : double, zRotation : double):
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
        FL = reducedX + reducedY + reducedZ
        FR = reducedX - reducedY - reducedZ
        BR = reducedZ - reducedX - reducedY
        BL = reducedY - reducedX - reducedZ
        
        self._setMotor("FL", FL)
        self._setMotor("FR", FR)
        self._setMotor("BR", BR)
        self._setMotor("BL", BL)
          
    
    def _setMotor(self, motor, speed):
        # TODO define better
        pass
