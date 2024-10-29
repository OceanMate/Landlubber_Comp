from Robot.Robot import Robot
from structure.RobotState import RobotState
from structure.Input.KeyboardListener import KeyboardListener

import time

def main():
    run_robot = Robot()
    robot_state = RobotState()

    run_robot.robot_init()
    
    robot_state.enable_teleop()
    
    while True:
        # Run periodic functions
        run_robot.robot_perodic()
        KeyboardListener().update()
        
        
        if robot_state.is_init_teleop():
            run_robot.teleop_init()
        
        if robot_state.is_teleop_enabled():
            run_robot.teleop_periodic()
            
        if robot_state.is_init_disable():
            run_robot.disabled_init()
        
        # Add a small delay to prevent high CPU usage
        time.sleep(0.02)
        
if __name__ == "__main__":
    main()