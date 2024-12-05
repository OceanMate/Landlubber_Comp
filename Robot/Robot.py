from jigboard.Jigboard import Jigboard
from structure.CommandRunner import CommandRunner
from robot.RobotContainer import RobotContainer

class Robot:    
    def __init__(self):
        self.command_runner = CommandRunner()
        self.robot_container = RobotContainer()
    
    def robot_init(self):
        def print_hi():
            print("hi")
        Jigboard().put_button("HIIII", print_hi)

        return
    
    def robot_periodic(self):
        self.command_runner.run_commands()
        Jigboard().put_boolean("enabled", self.command_runner.enabled)

        
    
    def teleop_init(self):
        self.command_runner.turn_on()
            
    def teleop_periodic(self):
            
        return
    
    def disabled_init(self):
        self.command_runner.turn_off()
