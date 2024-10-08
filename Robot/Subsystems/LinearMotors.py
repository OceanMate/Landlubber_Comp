from structure.Subsystem import Subsystem

class LinearMotors(Subsystem):
    def __init__(self):
        Subsystem.__init__(self, "LinearMotors")
    
    # Runs the motors given the x, y, and z speeds (each from -1 to 1)
    def runMotors(self, xSpeed, ySpeed, zRotation):
        # Tennille code goes here 
        pass
    
    def __setMotor(self, motor, speed):
        # TODO define better
        pass
