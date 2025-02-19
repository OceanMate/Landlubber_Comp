import io
import socket
import struct
from PIL import Image, ImageTk
import cv2
import numpy
import threading
import tkinter as tk

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
    
    def _init(self, host='172.61.34.186', port=9999):
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        # I think this can be 1 instead of 5 because we make separate threads for each client
        # but it doesn't hurt to have a higher number
        self.server_socket.listen(5)
        # print(f"Listening on {host}:{port}")
        self.frames = {}
        self.lock = threading.Lock()
        self.num_cameras = 0

    def handle_client(self, connection, client_id):
        try:
            while True:
                image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))
                image_stream.seek(0)
                frame = Image.open(image_stream)
                image = cv2.cvtColor(numpy.array(frame), cv2.COLOR_RGB2BGR)
                with self.lock:
                    self.frames[client_id] = image
        finally:
            connection.close()

    def start(self):
        threading.Thread(target=self._start).start()
        
    def _start(self):
        while True:
            connection = self.server_socket.accept()[0].makefile('rb')
            threading.Thread(target=self.handle_client, args=(connection, self.num_cameras)).start()
            self.num_cameras += 1
    
    def get_num_of_cameras(self):
        return self.num_cameras
    
    def get_camera_image(self, camera_id):
        if self.lock.acquire(blocking=False):  # Try to acquire the lock without blocking
            try:
                return self.frames.get(camera_id, None)
            finally:
                self.lock.release()  # Make sure to release the lock
        else:
            # Handle the case where the lock is not acquired
            return None