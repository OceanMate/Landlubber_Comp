from Robot.Robot import Robot
from structure.RobotState import RobotState

def main():
    runRobot = Robot()
    runRobot.robot_init()
    robotState = RobotState()
    
    # temp, should come from GUI button
    robotState.set_enabled(True)
    
    while True:
        runRobot.robot_perodic()
        
        if robotState.is_enabled() and robotState.is_teleop_to_be_initialized():
            runRobot.teleop_init()
            robotState.set_teleop_to_be_initialized(False)
        
        if robotState.is_enabled():
            runRobot.teleop_periodic()
            
        if not robotState.is_enabled() and robotState.is_disabled_to_be_initialized():
            runRobot.disabled_init()
            robotState.set_disabled_to_be_initialized(False)
        
        
if __name__ == "__main__":
    main()