from Robot.Robot import Robot
from structure.RobotState import RobotState
from structure.Input.KeyboardListener import KeyboardListener
import time

def main():
    runRobot = Robot()
    runRobot.robot_init()
    robotState = RobotState()
    
    # temp, should come from GUI button
    robotState.enable_teleop()
    
    while True:
        runRobot.robot_perodic()
        KeyboardListener().update()
        
        if robotState.is_init_teleop():
            runRobot.teleop_init()
        
        if robotState.is_teleop_enabled():
            runRobot.teleop_periodic()
            
        if robotState.is_init_disable():
            runRobot.disabled_init()
        
        time.sleep(0.02)
        
if __name__ == "__main__":
    main()