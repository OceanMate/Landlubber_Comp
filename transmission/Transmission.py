import socket
import select

class Transmission:
    _instance = None
    
    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
       
    def start(self, host: str = '192.168.1.100', port: int = 8000):
        self.linear_motor_speeds = f"l_motors {0} {0} {0} {0}"
        self.vertical_motor_speeds = f"v_motors {0} {0}"
        self.enabled = f"enabled {False}"
        
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(False)
        self.connected = False
        
        self.disconnect()
        
    
    def set_linear_motor_speeds(self, flSpeed : float, frSpeed : float, blSpeed : float, brSpeed : float):
        self.linear_motor_speeds = f"motor_speeds {flSpeed} {frSpeed} {blSpeed} {brSpeed}"
        
        print(self.linear_motor_speeds)
        
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
    
    def connect(self):
        if self.connected:
            return
        
        try:
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            self.connected = True
        except BlockingIOError:
            pass
        except socket.error as e:
            if e.errno == 10056:  # WSAEISCONN (already connected)
                print("Socket is already connected.")
                self.connected = True
            else:
                print(f"Failed to connect to server: {e}")
                self.connected = False
    
    def disconnect(self):
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
            print(f"Failed to send command: {e}")
            self.connected = False
            return False

