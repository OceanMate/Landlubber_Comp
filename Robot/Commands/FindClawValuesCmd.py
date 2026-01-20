from structure.commands.Command import Command
from Robot.Subsystems.Claw import Claw

class FindClawValuesCmd(Command):
    def __init__(self, claw : Claw, left_x_axis, right_x_axis ):
        super().__init__()
        self.claw = claw
        super().add_requirement(self.claw)
        
        self.left_x_axis = left_x_axis
        self.right_x_axis = right_x_axis
        
    
    def initalize(self):
        return
    
    def execute(self):
        self.claw._set_clamp(self.left_x_axis())
        self.claw._set_roll_angle(self.right_x_axis())
    
    def end(self, interrupted):
        return
    
    def is_finished(self):
        return False