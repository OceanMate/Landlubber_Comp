from robot.Robot import Robot
from jigboard.Jigboard import Jigboard
from structure.RobotState import RobotState
from structure.Input.KeyboardListener import KeyboardListener
from structure.Input.ControllerListener import ControllerListener

import time

from transmission.Transmission import Transmission

def main():
    run_robot = Robot()
    robot_state = RobotState()
    naut_coms = Transmission()

    naut_coms.start()
    run_robot.robot_init()
    
    start_time = time.time()

    while True:
        # Update the dashboard
        Jigboard().update()
        
        # Run periodic functions
        ControllerListener().update()
        KeyboardListener().update()      
        run_robot.robot_periodic()
        naut_coms.update()
        
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