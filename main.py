from Robot.Robot import Robot

def main():
    runRobot = Robot()
    runRobot.robot_init()
    
    # temp, should come from GUI button
    enabled = True
    teleop_initialized = False
    disabled_initialized = False
    
    while True:
        runRobot.robot_perodic()
        
        if enabled and not teleop_initialized:
            runRobot.teleop_init()
            teleop_initialized = True
            disabled_initialized = False
        
        if enabled:
            runRobot.teleop_periodic()
            
        if not enabled and not disabled_initialized:
            runRobot.disabled_init()
            disabled_initialized = True
            teleop_initialized = False
        
        
if __name__ == "__main__":
    main()