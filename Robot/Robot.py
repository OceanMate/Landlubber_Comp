from jigboard.Jigboard import Jigboard
from structure.CommandRunner import CommandRunner
from Robot.RobotContainer import RobotContainer

class Robot:    
    def __init__(self):
        self.command_runner = CommandRunner()
        self.robot_container = RobotContainer()
    
    def robot_init(self):
        return
    
    def robot_periodic(self):
        self.command_runner.run_commands()
        Jigboard().put_all_camera_widgets()
    
    def teleop_init(self):
        self.command_runner.turn_on()
        self.robot_container.teleop_init_commands()
            
    def teleop_periodic(self):
            
        return
    
    def disabled_init(self):
        self.command_runner.turn_off()
        self.robot_container.stop_subsystems()
