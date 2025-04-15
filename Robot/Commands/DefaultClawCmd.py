from structure.commands.Command import Command

class DefaultClawCmd(Command):
    def __init__(self, claw, right_bumper, a_button):
        super().__init__()
        self.claw = claw
        super().add_requirement(self.claw)
        
        self.right_bumper = right_bumper
        self.a_button = a_button
        
    
    def initalize(self):
        return
    
    def execute(self):
        if self.a_button():
            if self.claw.roll_angle <= 0.05: # if the roll motor close to 0, set it to 90
                self.claw.set_roll_angle(180)
            else:
                self.claw.set_roll_angle(0)
        
        if self.right_bumper():
            if self.claw.is_claw_open():
                self.claw.close_claw()
            else:
                self.claw.open_claw()
    
    def end(self, interrupted):
        return
    
    def is_finished(self):
        return False