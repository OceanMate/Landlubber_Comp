from Robot.Robot import Robot
from dashboard.Dashboard import Dashboard
from structure.RobotState import RobotState
from structure.Input.KeyboardListener import KeyboardListener
from structure.Input.ControllerListener import ControllerListener

import time

def main():
    run_robot = Robot()
    robot_state = RobotState()

    run_robot.robot_init()
    
    start_time = time.time()

    while True:
        # Run periodic functions

        ControllerListener().update()
        KeyboardListener().update()
                     
        run_robot.robot_periodic()
        
        if robot_state.is_init_teleop():
            run_robot.teleop_init()
        
        if robot_state.is_teleop_enabled():
            run_robot.teleop_periodic()
            
        if robot_state.is_init_disable():
            run_robot.disabled_init()
        
        Dashboard().update()
        
        # Add a small delay to prevent high CPU usage
        time.sleep(0.01)
        
if __name__ == "__main__":
    main()