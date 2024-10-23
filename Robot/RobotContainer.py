from Robot.Subsystems.LinearMotors import LinearMotors
from Robot.Commands.DefaultLinearMotorCmd import DefaultLinearMotorCmd
from Robot.Commands.FunkyMotorCmd import FunkyMotorCmd
from Robot.Commands.OverrideCmd import OverrideCmd
from structure.Input.KeyboardInput import KeyboardInput

class RobotContainer:
    def __init__(self):
        self.linear_motors = LinearMotors()
        
        self.linear_motors.defaultCommand(DefaultLinearMotorCmd(self.linear_motors))
        
        self.configure_button_bindings()


    # Configure button that will trigger commands
    def configure_button_bindings(self):
        KeyboardInput("f").on_false(FunkyMotorCmd(self.linear_motors))
        KeyboardInput("o").on_true(OverrideCmd(self.linear_motors))