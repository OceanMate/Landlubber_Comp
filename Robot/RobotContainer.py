from Robot.Subsystems.LinearMotors import LinearMotors
from Robot.Commands.DefaultLinearMotorCmd import DefaultLinearMotorCmd
from Robot.Commands.FunkyMotorCmd import FunkyMotorCmd
from Robot.Commands.OverrideCmd import OverrideCmd
from structure.Input.KeyboardInput import KeyboardInput
from structure.Input.ControllerButton import ControllerButton

class RobotContainer:
    def __init__(self):
        self.linear_motors = LinearMotors()
        
        # default command should schedule if no other command requiring is running
        self.linear_motors.defaultCommand(DefaultLinearMotorCmd(self.linear_motors))
        
        self.configure_button_bindings()


    def configure_button_bindings(self):
        # schedule FunkyMotorCmd when "f" is pressed
        KeyboardInput("f").on_false(FunkyMotorCmd(self.linear_motors))
        KeyboardInput("o").while_false(OverrideCmd(self.linear_motors))
        ControllerButton(1).on_true(FunkyMotorCmd(self.linear_motors)) 