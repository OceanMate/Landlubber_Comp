

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 15:42:57 2024

@author: deant
"""

# client.py
import socket
from time import sleep
from typing import List



class Transmission:
    _instance = None

    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._start()
        return cls._instance
    
    
    def _start(self, host: str = '172.61.15.222', port: int = 8000):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        
    def set_linear_motor_speeds(self, flSpeed : float, frSpeed : float, blSpeed : float, brSpeed : float):
        self.linear_motor_speeds = f"l_motors {flSpeed} {frSpeed} {blSpeed} {brSpeed}"
        
        print(self.linear_motor_speeds)
        
        return self.send_command(self.linear_motor_speeds)
    
    def set_vertical_motor_speeds(self, frontSpeed : float, backSpeed : float):
        self.vertical_motor_speeds = f"vert_motors {frontSpeed} {backSpeed}"
        
        return self.send_command(self.vertical_motor_speeds)
    
    
    def setEnable(self, enable: bool):
        self.isEnable = f"isEnabled {enable}"
        
        return self.send_command(self.isEnable)
    
    def connect(self) -> bool:
        """Establish connection to ROV server"""
        try:
            self.socket = socket.socket()
            self.socket.settimeout(1)
            self.socket.connect((self.host, self.port))
            self.connected = True
            #print("Connected to ROV")
            return True
        except socket.error as e:
            #print(f"Connection failed: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
        """Gracefully disconnect from server"""
        if self.connected and self.socket:
            try:
                self.send_command("quit")
                self.socket.close()
            except socket.error:
                pass
            finally:
                self.connected = False
                self.socket = None
    
    def send_command(self, command: str) -> bool:
        """Send a command to the server"""
        if not self.connected or not self.socket:
            return False
        
        try:
            self.socket.send(command.encode())
            return True
        except socket.error as e:
            print(f"Failed to send command: {e}")
            self.connected = False
            return False
        
    def update(self):
        """Update the client"""
        if not self.connect():
            return
            #print("Failed to connect to ROV")

