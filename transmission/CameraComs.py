import io
import socket
import struct
from PIL import Image
import cv2
import numpy
import threading
from typing import Union


class CameraComs:
    _instance = None

    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self, host='192.168.1.1', port=46389):
        self.host = host
        self.port = port
        self.frames = {}
        self.locks = {}  # Create a lock for each camera thread
        self.num_cameras = 0
        self.frame_displayed = {}  # Track if a frame has been displayed for each camera

    def handle_client(self, connection, client_id):
        try:
            while True:
                # Read the length of the image data
                data = connection.read(struct.calcsize('<L'))
                if not data:
                    break
                image_len = struct.unpack('<L', data)[0]
                if not image_len:
                    break

                # Use a buffer to read the image data
                image_data = b''
                while len(image_data) < image_len:
                    packet = connection.read(image_len - len(image_data))
                    if not packet:
                        break
                    image_data += packet

                if len(image_data) != image_len:
                    break

                # Process the image data
                image_stream = io.BytesIO(image_data)
                frame = Image.open(image_stream)
                frame = cv2.cvtColor(numpy.array(frame), cv2.COLOR_RGB2BGR)

                # Store the frame in a thread-safe manner
                with self.locks[client_id]:
                    self.frames[client_id] = frame
                    self.frame_displayed[client_id] = False  # Mark frame as not displayed
        except Exception as e:
            print(f"Error with client {client_id}: {e}")
        finally:
            connection.close()
            with self.locks[client_id]:
                if client_id in self.frames:
                    del self.frames[client_id]  # Remove stored frame
                if client_id in self.frame_displayed:
                    del self.frame_displayed[client_id]  # Clean up on client disconnect
            print(f"Camera {client_id} disconnected")

    def begin_thread(self):
        thread = threading.Thread(target=self._start)
        thread.daemon = True
        thread.start()
        
    def _start(self):
        self.server_sockets = []
        
        while True:
            self.server_sockets.append(socket.socket())
            self.server_sockets[self.num_cameras].bind((self.host, self.port + self.num_cameras))
            self.server_sockets[self.num_cameras].listen(5)
            print(f"Camera Stream listening on {self.host}:{self.port + self.num_cameras} for Camera {self.num_cameras}")
            
            connection, _ = self.server_sockets[self.num_cameras].accept()
            connection = connection.makefile('rb')
            client_id = self.num_cameras
            self.num_cameras += 1
            self.locks[client_id] = threading.Lock()  # Create a lock for the new client
            
            # Create a new thread for each client connection
            thread = threading.Thread(target=self.handle_client, args=(connection, client_id))
            thread.daemon = True
            thread.start()
    
    def get_camera_frame(self, camera_id, is_displaying = True) -> Union[numpy.ndarray, None]:
        if self.locks[camera_id].acquire(blocking=False):  # Try to acquire the lock without blocking
            try:
                frame = self.frames.get(camera_id, None)
                if is_displaying and frame is not None:
                    self.frame_displayed[camera_id] = True  # Mark frame as displayed
                return frame
            finally:
                self.locks[camera_id].release()  # Make sure to release the lock
        else:
            # Handle the case where the lock is not acquired
            return None

    def is_frame_displayed(self, camera_id):
        with self.locks[camera_id]:
            return self.frame_displayed.get(camera_id, True)  # Default to True if not found