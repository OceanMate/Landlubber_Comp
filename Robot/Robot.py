from structure.CommandRunner import CommandRunner
from Robot.RobotContainer import RobotContainer

class Robot:    
    def __init__(self):
        self.command_runner = CommandRunner()
        self.robot_container = RobotContainer()
    
    def robot_init(self):
        
        return
    
    def robot_perodic(self):
        self.command_runner.run_commands()
        
    
    def teleop_init(self):
        self.command_runner.turn_on()
            
    def teleop_periodic(self):
            
        return
    
    def disabled_init(self):
        self.command_runner.turn_off()
