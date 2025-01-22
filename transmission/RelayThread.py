import selectors
import socket
import threading
import traceback

import transmission.libclient as libclient


class RelayThread:
    _instance = None

    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._start()
        return cls._instance
    
    
    def _start(self):
        self.sel = selectors.DefaultSelector()
        self.sensor_data = {"IMU": (0.0, 0.0, 0.0)}
        self.robot_state = {"horizontal_motors": (0.0, 0.0, 0.0, 0.0), "vertical_motors": (0.0, 0.0), "enabled": False}
        
        self.host = 'localhost'
        self.port = 65432
        self.connected = False
    
    def set_horizontal_motors(self, fl : float, fr : float, br : float, bl : float):
        self.robot_state["horizontal_motors"] = (fl, fr, br, bl)
    
    def set_vertical_motors(self, front : float, back : float):
        self.robot_state["vertical_motors"] = (front, back)
    
    def set_enabled(self, enabled : bool):
        self.robot_state["enabled"] = enabled
    
    def get_imu_data(self):
        return self.sensor_data["IMU"]
    
    def begin_thread(self):
        thread = threading.Thread(target=self._run_client_socket)
        thread.start()

    def _create_request(self, robot_state):
        return dict(
            type="text/json",
            encoding="utf-8",
            content=robot_state,
        )
    
    def _start_connection(self, host, port):
        addr = (host, port)
        print(f"Starting connection to {addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)

        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        # Send intial message to establish connection with initial robot state
        request = self._create_request(self.robot_state)
        message = libclient.Message(self.sel, sock, addr, request, self.robot_state, self.sensor_data)
        self.sel.register(sock, events, data=message)
    
    def _check_for_connection(self):
        try:
            with socket.create_connection((self.host, self.port), timeout=3) as sock:
                print(f"Connection to {self.host}:{self.port} successful")
            return True
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            return False

    def _run_client_socket(self):
        try:
            # Send and recieve messages
            while True:
                # pass on the rest of  if it can't be found
                if not self.sel.get_map() and not self._check_for_connection():
                    self.connected = False
                    continue
                
                # connect if there are no active connections
                if not self.sel.get_map():
                    self._start_connection(self.host, self.port)
                    self.connected = True

                events = self.sel.select(timeout=1)
                
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask, self.robot_state)
                        print(f"Received: {message.sensor_data}")
                    except Exception:
                        print(
                            f"Main: Error: Exception for {message.addr}:\n"
                            f"{traceback.format_exc()}"
                        )
                        message.close()
                        self.connected = False
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()