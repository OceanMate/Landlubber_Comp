import socket

class Transmission:
    _instance = None
    
    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance    
       
    def start(self, host: str = '192.168.1.101', port: int = 8000):
        self.linear_motor_speeds = f"linear_motor_speeds {0} {0} {0} {0}"
        self.vertical_motor_speeds = f"vertical_motor_speeds {0} {0}"
        self.enabled = f"enabled {False}"
        
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.connected = False
    
    def set_connected(self, connected : bool):
        self.connected = connected
    
    def set_linear_motor_speeds(self, flSpeed : float, frSpeed : float, blSpeed : float, brSpeed : float):
        self.linear_motor_speeds = f"motor_speeds {flSpeed} {frSpeed} {blSpeed} {brSpeed}"
        
        return self.send_command(self.linear_motor_speeds)
    
    def set_vertical_motor_speeds(self, frontSpeed : float, backSpeed : float):
        self.vertical_motor_speeds = f"vertical_motor_speeds {frontSpeed} {backSpeed}"
        
        return self.send_command(self.vertical_motor_speeds)

    def set_enable(self, enable : bool):
        self.enabled = f"enabled {enable}"
        
        return self.send_command(self.enabled)
    
    def update(self):
        if not self.connected:
            self.connect()
            return
        
        # Receive data from server
        try:
            # Receive data from server
            data = self.socket.recv(1024)
            if not data:
                return
            # put a function to process the data here
            
        except socket.error as e:
            # debug
            # print(f"Failed to receive data: {e}")
            self.connected = False
            return
    
    def connect(self) -> bool:
        # Establish connection to ROV server
        try:
            self.socket = socket.socket()
            
            self.socket.settimeout(0)  # 0 second timeout to make non-blocking
            self.socket.connect((self.host, self.port))
            self.connected = True
            return True
        except socket.error as e:
            # debug
            #print(f"Connection failed: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
        # Gracefully disconnect from server
        if self.connected:
            try:
                self.send_command("quit")
                self.socket.close()
            except socket.error:
                pass
            finally:
                self.connected = False
    
    def send_command(self, command: str) -> bool:
        # Send a command to the server
        if not self.connected:
            return False
        
        try:
            self.socket.send(command.encode())
            return True
        except socket.error as e:
            # debug
            # print(f"Failed to send command: {e}")
            self.connected = False
            return False
    
    