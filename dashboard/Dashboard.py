import sys
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ctypes

from dashboard.BottomBar import BottomBar
from dashboard.GraphicConstants import GraphicConstants
from dashboard.GridGraphics import GridGraphics
from dashboard.widgets.StringWidget import StringWidget
from dashboard.TabBar import TabBar
from structure.Input.EventLoop import EventLoop
from structure.Input.KeyboardInput import KeyboardInput
from structure.RobotState import RobotState



class Dashboard:
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
        # Widget Dictionary
        self.user_inputs = {}
        self.widgets = {}

             
        # Create window
        self.window = Tk()
        self.window.geometry(str(GraphicConstants().window_width) + "x" + str(GraphicConstants().window_height))
        self.window.configure(bg = "#FFFFFF")
        self.window.title("Dashboard")
        #self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self._disable)
        
        # Set the icon for the window
        appID = "Rabbit Dashboard"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appID)
        self.window.iconbitmap(GraphicConstants().get_asset_path("rabbit_logo.ico"))
        
        # Generate the various components of the dashboard
        self.tab_bar = TabBar(self.window)
        self.tab_bar.generate_tab_bar()
        
        self.grid_graphics = GridGraphics()
        self.grid_graphics.init(self.window, self.widgets)
        self.grid_graphics.generate_grid()
        
        self.bottom_bar = BottomBar(self.window, self.user_inputs)
        self.bottom_bar.create_bottom_bar()
        
        self.setup_hotkeys()
        
        # Enable the dashboard
        self.enable = True
  
    def setup_hotkeys(self):
        # Event loop for the dashboard for hotkeys
        self.dashboard_hotkeys_loop = EventLoop()
        
        def on_enter():
            if RobotState().is_teleop_enabled():
                RobotState().disable_robot()
                self.bottom_bar.enable_button.config(fg=GraphicConstants().dark_green)
                self.bottom_bar.enable_button.config(text="Enable")
        
        enter_hotkey = KeyboardInput("enter")
        enter_hotkey.non_cmd_on_true(func=on_enter)
        enter_hotkey.set_loop(loop=self.dashboard_hotkeys_loop)
        
    
    # Create a string widget on the dashboard, or can be called multiple times to update the text of the widget
    def put_string(self, label, text):
        if self.grid_graphics is None:
            return
        
        if label not in self.grid_graphics.widgets.keys():
            # Create a new widget if it doesn't already exist
            self.grid_graphics.widgets[label] = StringWidget(self.grid_graphics.grid_canvas, label)
            wigit_grid_width, wigit_grid_height = self.widgets[label].get_default_dimensions()
            
            # Find the next available space for the widget, and tell the grid manager to place the widget there
            loc = self.grid_graphics.find_next_available_space(wigit_grid_width, wigit_grid_height)
            self.grid_graphics.place_rectangle(loc[0], loc[1], wigit_grid_width, wigit_grid_height)
            
            # Create the widget on the canvas
            self.widgets[label].create_string_widget(loc[0], loc[1], text)
        else:
            # Update the text of the widget if it already exists
            self.widgets[label].update_text(text)

    # Function that should be called periodicly to update the dashboard
    def update(self):
        
        if GraphicConstants().window_width != self.window.winfo_width() or GraphicConstants().window_height != self.window.winfo_height():
            GraphicConstants().window_width = self.window.winfo_width()
            GraphicConstants().window_height = self.window.winfo_height()
            
            self.tab_bar.resize_tab_bar()
            self.grid_graphics.resize_grid()
            self.bottom_bar.resize_bottom_bar()
            
            for key in self.widgets.keys():
                self.widgets[key].recreate_widget()

        # Update the window, use this instead of mainloop to allow for other functions to be called (non-blocking)
        self.window.update()
        
        # Check if any user inputs have been made and run the associated function
        for user_input in self.user_inputs:
            if self.user_inputs[user_input].run:
                self.user_inputs[user_input].function()
                self.user_inputs[user_input].run = False
                
        # Check hotkeys
        self.dashboard_hotkeys_loop.poll()
        
        # Check if the dashboard has been disabled, and close the window if it has
        if not self.enable:
            self._close()
    
    
    
    # Close the window and exit the program
    def _close(self):
        self.window.destroy()
        sys.exit(0)
    
    # Disable the dashboard
    def _disable(self):
        self.enable = False   