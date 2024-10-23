from structure.Subsystem import Subsystem

class LinearMotors(Subsystem):
    def __init__(self):
        super().__init__("LinearMotors")
    
    # Runs the motors given the x, y, and z speeds (each from -1 to 1)
    def runMotors(self, xSpeed, ySpeed, zRotation):
        # Tennille code goes here
        # calculate the absolute values
        abs_x = abs(x)
        abs_y = abs(y)
        abs_z = abs(z)

        # Calculate the sum of absolute values
        total_sum = abs_x + abs_y + abs_z

        # actual matrix input
        X = x / total_sum
        Y = y / total_sum
        Z = z / total_sum

        # motor matrix output
        FL = X + Y + Z
        FR = X - Y - Z
        BR = Z - X - Y
        BL = Y - X - Z
        pass
    
    def __setMotor(self, motor, speed):
        # TODO define better
        pass
