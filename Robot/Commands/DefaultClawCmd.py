from structure.commands.Command import Command
from Robot.Subsystems.Claw import Claw

class DefaultClawCmd(Command):
    def __init__(self, claw : Claw, b_button, dpad_left, dpad_right):
        super().__init__()
        self.claw = claw
        super().add_requirement(self.claw)
        
        self.b_button = b_button 
        self.dpad_left = dpad_left
        self.dpad_right = dpad_right
        
    
    def initialize(self):
        return
    
    def execute(self):
        # Handle claw rolling with D-pad left/right
        if self.dpad_left():
            self.claw.roll_left()  # Roll left
        elif self.dpad_right():
            self.claw.roll_right()   # Roll right
        else:
            self.claw.stop_roll()     # Stop rolling
        
        # Handle claw opening/closing with B button
        if self.b_button():
            if self.claw.is_claw_open():
                self.claw.close_claw()
            else:
                self.claw.open_claw()
    
    def end(self, interrupted):
        self.claw.stop_roll()
    
    def is_finished(self):
        return False