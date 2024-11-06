class Transmission:
    _instance = None
    
    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance    
       
    def __init__(self):
        self.linear_motor_speeds = f"linear_motor_speeds {0} {0} {0} {0}"
        self.vertical_motor_speeds = f"vertical_motor_speeds {0} {0}"
        self.enabled = f"enabled {False}"
        
    
    def set_linear_motor_speeds(self, flSpeed : float, frSpeed : float, blSpeed : float, brSpeed : float):
        self.linear_motor_speeds = f"motor_speeds {flSpeed} {frSpeed} {blSpeed} {brSpeed}"
        # send command function here
    
    def set_vertical_motor_speeds(self, frontSpeed : float, backSpeed : float):
        self.vertical_motor_speeds = f"vertical_motor_speeds {frontSpeed} {backSpeed}"
        # send command function here
    
    def set_enable(self, enable : bool):
        self.enabled = f"enabled {enable}"
        # send command function here
    
    def update(self):
        pass
    
    