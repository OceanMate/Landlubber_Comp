from structure.commands.Command import Command
from Robot.Subsystems.Claw import Claw

class DefaultClawCmd(Command):
    def __init__(self, claw : Claw, b_button, a_button):
        super().__init__()
        self.claw = claw
        super().add_requirement(self.claw)
        
        self.b_button = b_button 
        self.a_button = a_button
        
    
    def initalize(self):
        return
    
    def execute(self):
        
        if self.a_button():
            if self.claw.is_claw_horiz():
                self.claw.roll_claw_vert()
            else:
                self.claw.roll_claw_horiz()
        
        if self.b_button():
            if self.claw.is_claw_open():
                self.claw.close_claw()
            else:
                self.claw.open_claw()
    
    def end(self, interrupted):
        return
    
    def is_finished(self):
        return False