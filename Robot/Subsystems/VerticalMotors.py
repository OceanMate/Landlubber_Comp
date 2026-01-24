
from jigboard.Jigboard import Jigboard
from jigboard.JigboardTab import JigboardTab
from structure.Subsystem import Subsystem
from transmission.ComsThread import ComsThread
from simple_pid import PID
from Robot.Math import Math


class VerticalMotors(Subsystem):
    def __init__(self):
        super().__init__()
        
        self.front_left_motor = 0
        self.front_right_motor = 0
        self.back_motor = 0
        
        # Pitch PID controller
        self.pitch_pid = PID(0.05, 0.01, 0.0, setpoint=0)
        self.pitch_pid.output_limits = (-1, 1)  # Limit output to motor
        # Roll PID controller
        self.roll_pid = PID(0.05, 0.0, 0.0, setpoint=0)
        self.roll_pid.output_limits = (-1, 1)  # Limit output to motor
        
        self.programmer_tab = JigboardTab("Programmer Board")
    
    def get_pitch_pid(self, target_angle : float):
        self.pitch_pid.setpoint = target_angle
        
        pitch = Math.pitch_from_quat(ComsThread().get_imu_data())
        motor_speed = self.pitch_pid(pitch) # current pitch angle
        
        if motor_speed == None:
            print("ERROR: Pitch PID returned None")
            motor_speed = 0
        return motor_speed

    def get_roll_pid(self, target_angle : float):
        self.roll_pid.setpoint = target_angle
        
        roll = Math.roll_from_quat(ComsThread().get_imu_data())
        motor_speed = self.roll_pid(roll) # current roll angle
        
        if motor_speed == None:
            print("ERROR: Roll PID returned None")
            motor_speed = 0
        return motor_speed

        
    def run_motors(self, zSpeed, pitchSpeed, rollSpeed):
        # calculate the absolute values
        abs_z = abs(zSpeed)
        abs_pitch = abs(pitchSpeed)
        abs_roll = abs(rollSpeed)
        
        # Find the maximum of the absolute values
        maxSpeed = max([abs_z, abs_pitch, abs_roll])
        
        # prevent division by zero
        if (maxSpeed == 0):
            # no movement
            self.stop_motors()
            return
        
        z_div_max = abs_z / maxSpeed
        pitch_div_max = abs_pitch / maxSpeed
        roll_div_max = abs_roll / maxSpeed
        
        # sum of the divided values
        total_sum = z_div_max + pitch_div_max + roll_div_max
        
        
        # actual matrix input
        reducedZ = zSpeed / total_sum
        reducedPitch = pitchSpeed / total_sum
        reducedRoll = rollSpeed / total_sum

        # motor matrix output
        front_left_speed = -reducedZ + reducedPitch - reducedRoll
        front_right_speed = -reducedZ + reducedPitch + reducedRoll
        back_speed = -reducedZ - reducedPitch
        
        self._set_motor_speeds(front_left_speed, front_right_speed, back_speed)
    
    def _set_motor_speeds(self, front_left_speed, front_right_speed, back_speed):
        self.front_left_motor = front_left_speed * 0.888 if front_left_speed > 0 else front_left_speed
        self.front_right_motor = front_right_speed * 0.888 if front_right_speed > 0 else front_right_speed
        self.back_motor = back_speed * 0.888 if back_speed > 0 else back_speed
        
        ComsThread().set_vertical_motors(self.front_left_motor, self.front_right_motor, self.back_motor)

    def stop_motors(self):
        self._set_motor_speeds(0, 0, 0)
    
    def periodic(self):
        self.programmer_tab.put_string("Vertical Motor Speeds", "Front Left: {:.2f} Front Right: {:.2f} Back: {:.2f}".format(self.front_left_motor, self.front_right_motor, self.back_motor))