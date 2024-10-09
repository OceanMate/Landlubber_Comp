from Robot.Subsystems.LinearMotors import LinearMotors
from Robot.Commands.DefaultLinearMotorCmd import DefaultLinearMotorCmd

class RobotContainer:
    def __init__(self):
        self.linear_motors = LinearMotors()
        
        motorCmd = DefaultLinearMotorCmd(self.linear_motors)
        self.linear_motors.defaultCommand(motorCmd)
