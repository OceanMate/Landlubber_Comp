from Robot.Robot import Robot
from structure.RobotState import RobotState
from structure.Input.KeyboardListener import KeyboardListener
import time

def main():
    runRobot = Robot()
    runRobot.robot_init()
    robotState = RobotState()
    
    # temp, should come from GUI button
    robotState.enabled = True
    robotState.teleop_to_be_initialized = True
    
    while True:
        runRobot.robot_perodic()
        KeyboardListener().update()
        
        if robotState.enabled and robotState.teleop_to_be_initialized:
            runRobot.teleop_init()
            robotState.teleop_to_be_initialized = False
        
        if robotState.enabled:
            runRobot.teleop_periodic()
            
        if not robotState.enabled and robotState.disabled_to_be_initialized:
            runRobot.disabled_init()
            robotState.disabled_to_be_initialized = False
        
        time.sleep(0.02)
        
if __name__ == "__main__":
    main()