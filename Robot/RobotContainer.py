from Robot.Subsystems.LinearMotors import LinearMotors
from Robot.Commands.DefaultLinearMotorCmd import DefaultLinearMotorCmd
from Robot.Commands.FunkyMotorCmd import FunkyMotorCmd
from Robot.Commands.OverrideCmd import OverrideCmd
from structure.Input.KeyboardInput import KeyboardInput
from structure.Input.ControllerButton import ControllerButton
from structure.commands.InstantCommand import InstantCommand
from structure.commands.SequentialCommandGroup import SequentialCommandGroup
from structure.Input.ControllerListener import ControllerListener

class RobotContainer:
    def __init__(self):
        self.linear_motors = LinearMotors()
        self.controller = ControllerListener()
        self.controller.deadband = .1
        
        # default command should schedule if no other command requiring is running
        #print(f"{self.controller.get_axis(0)} {self.controller.get_axis(1)} {self.controller.get_axis(2)})
        
        self.linear_motors.defaultCommand(
            DefaultLinearMotorCmd(self.linear_motors, 
            lambda: self.controller.get_axis(0),
            lambda: self.controller.get_axis(1),
            lambda: self.controller.get_axis(2)))
        
        self.configure_button_bindings()

    def configure_button_bindings(self):
        # schedule FunkyMotorCmd when "f" is pressed
        KeyboardInput("f").on_true(FunkyMotorCmd(self.linear_motors))
        KeyboardInput("o").while_false(OverrideCmd(self.linear_motors))
        ControllerButton(0).on_true(FunkyMotorCmd(self.linear_motors)) 
        KeyboardInput("w").on_true(InstantCommand(lambda: print("w")))
    
    def stop_subsystems(self):
        self.linear_motors.stop_motors()