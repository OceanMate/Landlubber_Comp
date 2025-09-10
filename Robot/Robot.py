from jigboard.Jigboard import Jigboard
from structure.CommandRunner import CommandRunner
from Robot.RobotContainer import RobotContainer

class Robot:    
    def __init__(self):
        self.command_runner = CommandRunner()
        self.robot_container = RobotContainer()
    
    def robot_init(self):
        pass
    
    def robot_periodic(self):
        self.command_runner.run_commands()
    
    def teleop_init(self):
        self.robot_container.teleop_init()
        self.command_runner.turn_on()
            
    def teleop_periodic(self):
        pass

    def test_init(self):
        self.robot_container.test_init()
        self.command_runner.turn_on()
    
    def test_periodic(self):
        pass
    
    def disabled_init(self):
        self.command_runner.turn_off()
        self.robot_container.stop_subsystems()
