from Robot.Commands.SaveImageCmd import SaveImageCmd
from Robot.Subsystems.Claw import Claw
from Robot.Subsystems.VerticalMotors import VerticalMotors
from Robot.Subsystems.LinearMotors import LinearMotors
from Robot.Commands.DefaultLinearMotorCmd import DefaultLinearMotorCmd
from Robot.Commands.DefaultVerticalMotorCmd import DefaultVerticalMotorCmd
from Robot.Commands.DefaultClawCmd import DefaultClawCmd

from structure.Input.KeyboardInput import KeyboardInput
from structure.Input.ControllerButton import ControllerButton
from structure.Input.KeyboardListener import KeyboardListener
from structure.commands.InstantCommand import InstantCommand
from structure.commands.SequentialCommandGroup import SequentialCommandGroup
from structure.Input.ControllerListener import ControllerListener

class RobotContainer:
    def __init__(self):
        self.linear_motors = LinearMotors()
        self.vertical_motors = VerticalMotors()
        self.claw = Claw()
        
        self.controller = ControllerListener()
        self.controller.deadband = .1
                
        # default command should schedule if no other command requiring is running
        self.linear_motors.defaultCommand(DefaultLinearMotorCmd(
            self.linear_motors, 
            lambda: self.controller.get_axis(0),
            lambda: self.controller.get_axis(1),
            lambda: self.controller.get_axis(2),
        ))
        self.vertical_motors.defaultCommand(DefaultVerticalMotorCmd(
            self.vertical_motors,
            lambda: self.controller.get_axis(4),
            lambda: self.controller.get_axis(5)
        ))
        self.claw.defaultCommand(DefaultClawCmd(
            self.claw,
            ControllerButton(4).get_on_true(),
            ControllerButton(5).get_on_true(),
        ))
                                    
        self.configure_button_bindings()

    def configure_button_bindings(self):
        pass
    
    def teleop_init_commands(self):
        # start a save image command when the c button is pressed
        # and switch cameras when the v button is pressed
        SaveImageCmd(
            KeyboardInput("c").get_on_true(), 
            KeyboardInput("v").get_on_true(),
        ).schedule()

    
    def stop_subsystems(self):
        self.linear_motors.stop_motors()