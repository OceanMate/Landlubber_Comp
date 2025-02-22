from Robot.Robot import Robot
from jigboard.Jigboard import Jigboard
from structure.RobotState import RobotState
from structure.Input.KeyboardListener import KeyboardListener
from structure.Input.ControllerListener import ControllerListener
from transmission.ComsThread import ComsThread
from transmission.CameraComs import CameraComs

import time


def main():
    run_robot = Robot()
    robot_state = RobotState()
    
    naut_coms = ComsThread()
    naut_coms.begin_thread()
    
    cam_coms = CameraComs()

    run_robot.robot_init()
    

    while True:
        # Update the dashboard
        Jigboard().update()
        
        # Run periodic functions
        ControllerListener().update()
        KeyboardListener().update()      
        run_robot.robot_periodic()
        
        if not ComsThread().connected:
            robot_state.disable_robot()
            # Update the enable button text and color to reflect the new state
            Jigboard().bottom_bar.update_enable_button(is_enabling=False)
        
        if robot_state.should_init_teleop():
            run_robot.teleop_init()
        
        if robot_state.is_teleop_enabled():
            run_robot.teleop_periodic()
            
        if robot_state.should_init_disable():
            run_robot.disabled_init()
        
        # Add a small delay to prevent high CPU usage
        time.sleep(0.01)
        
if __name__ == "__main__":
    main()