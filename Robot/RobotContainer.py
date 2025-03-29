from Robot.Subsystems.VerticalMotors import VerticalMotors
from Robot.Subsystems.LinearMotors import LinearMotors
from Robot.Commands.DefaultLinearMotorCmd import DefaultLinearMotorCmd
from Robot.Commands.DefaultVerticalMotorCmd import DefaultVerticalMotorCmd
from structure.Input.KeyboardInput import KeyboardInput
from structure.Input.ControllerButton import ControllerButton
from structure.commands.InstantCommand import InstantCommand
from structure.commands.SequentialCommandGroup import SequentialCommandGroup
from structure.Input.ControllerListener import ControllerListener

class RobotContainer:
    def __init__(self):
        self.linear_motors = LinearMotors()
        self.vertical_motors = VerticalMotors()
        self.controller = ControllerListener()
        self.controller.deadband = .1
                
        # default command should schedule if no other command requiring is running
        self.linear_motors.defaultCommand(DefaultLinearMotorCmd(
            self.linear_motors, 
            lambda: self.controller.get_axis(0),
            lambda: self.controller.get_axis(1),
            lambda: self.controller.get_axis(3),
            ))
        self.vertical_motors.defaultCommand(DefaultVerticalMotorCmd(
            self.vertical_motors,
            lambda: self.controller.get_axis(2),
            lambda: self.controller.get_axis(5)
            ))
                                    
        self.configure_button_bindings()

    def configure_button_bindings(self):
        return
    
    def stop_subsystems(self):
        self.linear_motors.stop_motors()