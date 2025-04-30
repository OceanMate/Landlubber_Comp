
from jigboard.Jigboard import Jigboard
from jigboard.JigboardTab import JigboardTab
from structure.Subsystem import Subsystem
from transmission.ComsThread import ComsThread


class VerticalMotors(Subsystem):
    def __init__(self):
        super().__init__()
        
        self.front_motor = 0
        self.back_motor = 0
        
        self.programmer_tab = JigboardTab("Programmer Board")

        
    def run_motors(self, speed):
        self._set_motor_speeds(speed, speed)
    
    def _set_motor_speeds(self, front_speed, back_speed):
        self.front_motor = front_speed
        self.back_motor = back_speed
        
        ComsThread().set_vertical_motors(self.front_motor, self.back_motor)

    def stop_motors(self):
        self._set_motor_speeds(0, 0)
    
    def periodic(self):
        self.programmer_tab.put_string("Vertical Motor Speeds", "Front: {:.2f} Back: {:.2f}".format(self.front_motor, self.back_motor))
