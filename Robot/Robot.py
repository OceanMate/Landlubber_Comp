from dashboard.Dashboard import Dashboard
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
        Dashboard().put_boolean("enabled", self.command_runner.enabled)
        def print_hi():
            print("hi")
        Dashboard().put_button("HIIII", print_hi)
        
    
    def teleop_init(self):
        self.command_runner.turn_on()
            
    def teleop_periodic(self):
            
        return
    
    def disabled_init(self):
        self.command_runner.turn_off()
