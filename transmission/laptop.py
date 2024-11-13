# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 15:42:57 2024

@author: deant
"""

# client.py
import socket
from typing import List, Tuple, Optional

class ROVClient:
    def __init__(self, host: str = '172.61.94.163', port: int = 8000):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self) -> bool:
        """Establish connection to ROV server"""
        try:
            self.socket = socket.socket()
            self.socket.settimeout(5)  # 5 second timeout
            self.socket.connect((self.host, self.port))
            self.connected = True
            return True
        except socket.error as e:
            print(f"Connection failed: {e}")
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
    
    def send_motor_command(self, motor_values: List[float]) -> bool:
        """Send motor command with validation"""
        #assumed values go from -100 to 100
        if not all(-100 <= v <= 100 for v in motor_values):
            print("Motor values must be between -100 and 100")
            return False
            
        command = f"motors {' '.join(map(str, motor_values))}"
        return self.send_command(command)

def run_client():
    client = ROVClient()
    
    if not client.connect():
        print("Failed to connect to ROV")
        return
    
    print("Connected to ROV")
    print("\nEnter commands as: motors <value1> <value2> ...")
    print("Values should be between -100 and 100")
    print("Enter 'quit' to exit")
    
    try:
        while True:
            cmd = input("> ").strip()
            
            if cmd.lower() == 'quit':
                break
                
            if cmd.startswith('motors'):
                try:
                    values = [float(x) for x in cmd.split()[1:]]
                    if not client.send_motor_command(values):
                        print("Failed to send motor command")
                except ValueError:
                    print("Invalid motor values")
            else:
                print("Unknown command")
    
    finally:
        client.disconnect()
        print("Disconnected from ROV")

if __name__ == "__main__":
    run_client()