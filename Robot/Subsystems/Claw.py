from jigboard.JigboardTab import JigboardTab
from structure.Subsystem import Subsystem
from transmission.ComsThread import ComsThread


class Claw(Subsystem):
    def __init__(self):
        super().__init__()
        
        self.open_claw()
        self.roll_claw_horiz()
        
        self.programmer_tab = JigboardTab("Programmer Board")
        
    def open_claw(self):
        self._set_clamp(0.45) 
    
    def close_claw(self):
        self._set_clamp(-0.6)
    
    def is_claw_open(self):
        # Check if the claw is open by checking the clamp motor position
        return self.clamp_motor == 0.45

    def roll_claw_horiz(self):
        # Roll the claw to the horizontal position
        self._set_roll_angle(-0.27)
    
    def roll_claw_vert(self):
        # Roll the claw to the vertical position
        self._set_roll_angle(0.6)
    
    def is_claw_horiz(self) -> bool:
        # Check if the claw is in the horizontal position by checking the roll angle
        return self.roll_angle == -0.27
    
    def _set_clamp(self, clamp_angle):
        self.clamp_motor = clamp_angle
        
        ComsThread().set_claw_clamp(self.clamp_motor)
    
    def _set_roll_angle(self, roll_angle):
        # Set the roll motor speed based on the roll angle
        self.roll_angle = roll_angle
        
        # Send the command to the ComsThread to set the roll motor
        ComsThread().set_claw_roll(roll_angle)
    
    def periodic(self):
        self.programmer_tab.put_string("Claw Motor Angle", 
                             "Clamp: {:.2f} Roll: {:.2f}".format(self.clamp_motor, self.roll_angle))
