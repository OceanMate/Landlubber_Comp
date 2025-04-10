from structure.commands.Command import Command

class DefaultClawCmd(Command):
    def __init__(self, claw, right_bumper, left_bumper):
        super().__init__()
        self.claw = claw
        super().add_requirement(self.claw)
        
        self.right_bumper = right_bumper
        self.left_bumper = left_bumper
        
    
    def initalize(self):
        return
    
    def execute(self):
        if self.left_bumper():
            if self.claw.roll_motor <= 0.05: # if the roll motor close to 0, set it to 90
                self.claw.set_roll_angle(90)
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