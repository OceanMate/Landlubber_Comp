from Robot.Commands import FindClawValuesCmd
from Robot.Commands.SaveImageCmd import SaveImageCmd
from Robot.Subsystems.Cameras import Cameras
from Robot.Subsystems.Claw import Claw
from Robot.Subsystems.VerticalMotors import VerticalMotors
from Robot.Subsystems.LinearMotors import LinearMotors
from Robot.Commands.DefaultLinearMotorCmd import DefaultLinearMotorCmd
from Robot.Commands.DefaultVerticalMotorCmd import DefaultVerticalMotorCmd
from Robot.Commands.DefaultClawCmd import DefaultClawCmd
from Robot.Commands.FindClawValuesCmd import FindClawValuesCmd

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
        self.cameras = Cameras()
        
        self.controller = ControllerListener()
        self.controller.deadband = .1
                
        # default command should schedule if no other command requiring is running
        self.linear_motors.defaultCommand(DefaultLinearMotorCmd(
            self.linear_motors, 
            lambda: self.controller.get_axis(1), # left stick y axis
            lambda: self.controller.get_axis(0), # left stick x axis
            lambda: -self.controller.get_axis(2), # right stick x axis
            ControllerButton(4).get_while_true(), # left trigger
        ))
        self.vertical_motors.defaultCommand(DefaultVerticalMotorCmd(
            self.vertical_motors,
            lambda: self.controller.get_axis(4), # left trigger
            lambda: self.controller.get_axis(5), # right trigger
            ControllerButton(4).get_while_true(), # left bumper
        ))
        self.claw.defaultCommand(DefaultClawCmd(
            self.claw,
            ControllerButton(5).get_on_true(), # right bumper
            ControllerButton(0).get_on_true(), # A button
        ))
        self.cameras.defaultCommand(SaveImageCmd(
            self.cameras,
            ControllerButton(2).get_on_true(), # save image button (X)
            ControllerButton(3).get_on_true(), # switch camera button (Y)
        ))
        
        # self.claw.defaultCommand(FindClawValuesCmd(
        #     self.claw,
        #     lambda: self.controller.get_axis(0), # left stick x axis
        #     lambda: self.controller.get_axis(2), # right stick x axis
        # ))
                                    
        self.configure_button_bindings()

    def configure_button_bindings(self):
        pass

    def stop_subsystems(self):
        self.linear_motors.stop_motors()