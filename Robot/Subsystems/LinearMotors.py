from structure.Subsystem import Subsystem

class LinearMotors(Subsystem):
    def __init__(self):
        super().__init__("LinearMotors")
    
    # Runs the motors given the x, y, and z speeds (each from -1 to 1)
    def runMotors(self, xSpeed, ySpeed, zRotation):
        # calculate the absolute values
        abs_x = abs(xSpeed)
        abs_y = abs(ySpeed)
        abs_z = abs(zRotation)

        # Calculate the sum of absolute values
        total_sum = abs_x + abs_y + abs_z

        # actual matrix input
        reducedX = xSpeed / total_sum
        reducedY = ySpeed / total_sum
        reducedZ = zRotation / total_sum

        # motor matrix output
        FL = reducedX + reducedY + reducedZ
        FR = reducedX - reducedY - reducedZ
        BR = reducedZ - reducedX - reducedY
        BL = reducedY - reducedX - reducedZ
        
    
    def __setMotor(self, motor, speed):
        # TODO define better
        pass
