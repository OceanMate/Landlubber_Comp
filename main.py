from Robot.Robot import Robot
from dashboard.Dashboard import Dashboard
from structure.RobotState import RobotState
from structure.Input.KeyboardListener import KeyboardListener
from structure.Input.ControllerListener import ControllerListener

import time

def main():
    run_robot = Robot()
    robot_state = RobotState()
    dashboard = Dashboard()

    run_robot.robot_init()
    
    robot_state.enable_teleop()
    
    while True:
        # Run periodic functions
        dashboard.update()
        run_robot.robot_periodic()
        KeyboardListener().update()
        ControllerListener().update()
        
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