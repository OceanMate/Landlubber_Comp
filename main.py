from Debug import Debug
from Robot.Robot import Robot
from jigboard.Jigboard import Jigboard
from structure.RobotState import RobotState
from structure.Input.KeyboardListener import KeyboardListener
from structure.Input.ControllerListener import ControllerListener
from transmission.ComsThread import ComsThread
from transmission.CameraComs import CameraComs

import time

def main():
    
    robot = Robot()
    robot_state = RobotState()
    
    naut_coms = ComsThread()
    if not Debug.disableComs:
        naut_coms.begin_thread()
    
    cam_coms = CameraComs()
    if not Debug.disableComs:
        cam_coms.begin_thread()

    robot.robot_init()
    

    while True:
        # Update the dashboard
        Jigboard().update()
        
        # Run periodic functions
        ControllerListener().update()
        KeyboardListener().update()      
        robot.robot_periodic()
        
        if not ComsThread().connected and not Debug.ignoreComsToEnable:
            robot_state.disable_robot()
            # Update the enable button text and color to reflect the new state
            Jigboard().bottom_bar.update_enable_button(is_enabling=False)
        
        # Teleop (human operated) mode
        if robot_state.should_init_teleop():
            print("Teleop mode enabled")
            robot.teleop_init()
        
        if robot_state.is_teleop_enabled():
            robot.teleop_periodic()
        
        # Test mode
        if robot_state.should_init_test():
            print("Test mode enabled")
            robot.test_init()
        
        if robot_state.is_test_enabled():
            robot.test_periodic()
        
        # Disabled check
        if robot_state.should_init_disable():
            robot.disabled_init()
        
        # Add a small delay to prevent high CPU usage
        time.sleep(0.01)
        
if __name__ == "__main__":
    main()