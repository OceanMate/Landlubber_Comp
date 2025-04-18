
from jigboard.Jigboard import Jigboard
from structure.Subsystem import Subsystem
from transmission.ComsThread import ComsThread


class Claw(Subsystem):
    def __init__(self):
        super().__init__()
        
        self.clamp_motor = 1
        self.roll_motor = 0
        
    def open_claw(self):
        self._set_clamp(1) 
    
    def close_claw(self):
        self._set_clamp(-0.6)
    
    def is_claw_open(self):
        # Check if the claw is open by checking the clamp motor position
        return self.clamp_motor == 1
    
    def set_roll_angle(self, angle):
        # Set the roll angle for the claw
        # Ensure the angle is within a valid range, e.g., 0 to 90 degrees
        if angle < 0:
            angle = 0
        elif angle > 90:
            angle = 90
        
        self._set_roll_angle(angle)
    
    def _set_clamp(self, clamp_angle):
        self.clamp_motor = clamp_angle
        
        ComsThread().set_claw_clamp(self.clamp_motor)
    
    def _set_roll_angle(self, roll_angle):
        # Set the roll motor speed based on the roll angle
        self.roll_motor = (roll_angle / 90) * 2 - 1
        
        # Send the command to the ComsThread to set the roll motor
        ComsThread().set_claw_roll(self.roll_motor)

    
    def periodic(self):
        Jigboard().put_string("Claw Motor Angle", 
                             "Clamp: {:.2f} Roll: {:.2f}".format(self.clamp_motor, self.roll_motor))
