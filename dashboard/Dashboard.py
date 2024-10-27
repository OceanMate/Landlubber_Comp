import tkinter as tk
from structure.CommandRunner import CommandRunner

# need to figure out how to make none blocking
class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Dashboard")
        self.geometry("300x200")
        
        self.enable_button = tk.Button(self, text="Enable", command=self.enable_action)
        self.enable_button.pack(pady=20)
    
    def enable_action(self):
        if self.enable_button["text"] == "Enable":
            self.enable_button["text"] = "Disable"
        else:
            self.enable_button["text"] = "Enable"

