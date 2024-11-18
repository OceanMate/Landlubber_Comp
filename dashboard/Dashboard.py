import sys
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ctypes

from dashboard.graphics.BottomBar import BottomBar
from dashboard.GraphicConstants import GraphicConstants
from dashboard.graphics.GridGraphics import GridGraphics
from dashboard.widgets.BooleanWidget import BooleanWidget
from dashboard.widgets.StringWidget import StringWidget
from dashboard.graphics.TabBar import TabBar
from structure.Input.EventLoop import EventLoop
from structure.Input.KeyboardInput import KeyboardInput
from structure.RobotState import RobotState
from dashboard.widgets.ButtonWidget import ButtonWidget
from transmission.Transmission import Transmission


# TODO - Add display for connection to rasberry pi
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
        self.tabs = {}
             
        # Create window
        self.window = Tk()
        self.window.geometry(str(GraphicConstants().window_width) + "x" + str(GraphicConstants().window_height))
        self.window.configure(bg = "#FFFFFF")
        self.window.title("Dashboard")
        
        # Make the program exit when the window is closed
        self.window.protocol("WM_DELETE_WINDOW", self._disable)
        
        # Set the icon for the window
        appID = "Rabbit Dashboard"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appID)
        self.window.iconbitmap(GraphicConstants().get_asset_path("rabbit_logo.ico"))
        
        # Generate the various components of the dashboard
        self.tab_bar = TabBar(self.window, self.tabs)
        self.tab_bar.generate_tab_bar()
        
        self.grid_graphics = GridGraphics()
        self.grid_graphics.init(self.window, self.tabs)
        self.grid_graphics.generate_grid()
        
        self.bottom_bar = BottomBar(self.window, self.user_inputs)
        self.bottom_bar.create_bottom_bar()
        
        # Setup hotkeys for the dashboard
        self._setup_hotkeys()
        
        # Enable the dashboard
        self.enable = True
                
    # Setup hotkeys for the dashboard 
    def _setup_hotkeys(self):
        # Event loop for the dashboard for hotkeys, need this to manage the keyboardListener thread
        self.dashboard_hotkeys_loop = EventLoop()
        
        # Hotkey to disable the robot
        def on_enter():
            if RobotState().is_teleop_enabled():
                RobotState().disable_robot()
                self.bottom_bar.enable_button.config(fg=GraphicConstants().dark_green)
                self.bottom_bar.enable_button.config(text="Enable")
        
        # Create the hotkey for the enter key
        enter_hotkey = KeyboardInput("enter")
        # Set the function to run when the hotkey is pressed
        enter_hotkey.non_cmd_on_true(func=on_enter)
        # Set the loop for the hotkey to be the dashboard loop
        enter_hotkey.set_loop(loop=self.dashboard_hotkeys_loop)     
    
    # Create a string widget on the dashboard, or can be called multiple times to update the text of the widget
    def put_string(self, label, text, tab = GraphicConstants().default_tab):
        # Check if the grid graphics have been initialized
        if self.grid_graphics is None:
            return
        
        # Check if the widget already exists
        if label not in self.grid_graphics.tabs[tab].keys():
            # Create a new widget if it doesn't already exist
            self.grid_graphics.tabs[tab][label] = StringWidget(self.grid_graphics.grid_canvas, label)
            wigit_grid_width, wigit_grid_height = self.tabs[tab][label].get_default_dimensions()
            
            # Find the next available space for the widget, and tell the grid manager to place the widget there
            loc = self.grid_graphics.find_next_available_space(wigit_grid_width, wigit_grid_height, tab)
            self.grid_graphics.place_rectangle(loc[0], loc[1], wigit_grid_width, wigit_grid_height, tab)
            
            # Create the widget on the canvas
            self.tabs[tab][label].create_string_widget(loc[0], loc[1], text)
            
            # Hide the widget if it is not in the current tab
            if tab != GraphicConstants().current_tab:
                self.tabs[tab][label].hide()
        else:
            # Update the text of the widget if it already exists
            self.tabs[tab][label].update_text(text)
    
    # Create a boolean widget on the dashboard, or can be called multiple times to update the boolean of the widget
    def put_boolean(self, label, boolean, tab = GraphicConstants().default_tab):
        # Create a new widget if it doesn't already exist
        if self.grid_graphics is None:
            return
        
        # Check if the widget already exists
        if label not in self.grid_graphics.tabs[tab].keys():
            # Create a new widget if it doesn't already exist
            self.grid_graphics.tabs[tab][label] = BooleanWidget(self.grid_graphics.grid_canvas, label)
            wigit_grid_width, wigit_grid_height = self.tabs[tab][label].get_default_dimensions()
            
            # Find the next available space for the widget, and tell the grid manager to place the widget there
            loc = self.grid_graphics.find_next_available_space(wigit_grid_width, wigit_grid_height, tab)
            self.grid_graphics.place_rectangle(loc[0], loc[1], wigit_grid_width, wigit_grid_height, tab)
            
            # Create the widget on the canvas
            self.tabs[tab][label].create_bool_widget(loc[0], loc[1], boolean)
            
            # Hide the widget if it is not in the current tab
            if tab != GraphicConstants().current_tab:
                self.tabs[tab][label].hide()
        else:
            # Update the text of the widget if it already exists
            self.tabs[tab][label].update_bool(boolean)

    # Create a button widget on the dashboard, or can be called again to update the command of the widget
    def put_button(self, label, command, tab=GraphicConstants().default_tab):
        # Check if the grid graphics have been initialized
        if self.grid_graphics is None:
            return
        
        # Check if the widget already exists
        if label not in self.grid_graphics.tabs[tab].keys():
            # Create a new widget if it doesn't already exist
            self.grid_graphics.tabs[tab][label] = ButtonWidget(self.grid_graphics.grid_canvas, label, command)
            widget_grid_width, widget_grid_height = self.tabs[tab][label].get_default_dimensions()
            
            # Find the next available space for the widget, and tell the grid manager to place the widget there
            loc = self.grid_graphics.find_next_available_space(widget_grid_width, widget_grid_height, tab)
            self.grid_graphics.place_rectangle(loc[0], loc[1], widget_grid_width, widget_grid_height, tab)
            
            # Create the widget on the canvas
            self.tabs[tab][label].create_button_widget(loc[0], loc[1])
            
            # Hide the widget if it is not in the current tab
            if tab != GraphicConstants().current_tab:
                self.tabs[tab][label].hide()
        else:
            # Update the command of the widget if it already exists
            self.tabs[tab][label].command = command

    # Function that should be called periodicly to update the dashboard
    def update(self):
        # Debug the grid
        # self.grid_graphics.debug_grid()
        
        # Check if the window has been resized, and resize all the widgets if it has        
        if GraphicConstants().window_width != self.window.winfo_width() or GraphicConstants().window_height != self.window.winfo_height():
            GraphicConstants().window_width = self.window.winfo_width()
            GraphicConstants().window_height = self.window.winfo_height()
            
            # recreate all the canvases
            self.tab_bar.resize_tab_bar()
            self.grid_graphics.resize_grid()
            self.bottom_bar.resize_bottom_bar()
            
            # recreate all the widgets
            current_tab = GraphicConstants().current_tab
            for widget in self.tabs[current_tab].values():
                widget.recreate_widget()
                self.grid_graphics.place_rectangle(widget.grid_x, widget.grid_y, widget.grid_width, widget.grid_height, GraphicConstants().current_tab)

            # Move all widgets that are out of bounds to the next available space
            out_of_bound_widgets = []
            
            # Check if the widget is out of bounds and add it to the list
            for widget in self.tabs[current_tab].values():
                if self.grid_graphics.is_out_of_bounds(widget.grid_x, widget.grid_y, widget.grid_width, widget.grid_height):
                    self.grid_graphics.remove_rectangle(widget.grid_x, widget.grid_y, widget.grid_width, widget.grid_height, GraphicConstants().current_tab)
                    out_of_bound_widgets.append(widget)
            
            # Move all widgets in the list to the next available space
            for widget in out_of_bound_widgets:
                new_x, new_y = self.grid_graphics.find_next_available_space(widget.grid_width, widget.grid_height, current_tab)
                widget.move_widget(new_x, new_y)
                    
        
        # Update the window, use this instead of mainloop to allow for other functions to be called (non-blocking)
        self.window.update()
        
        # Check if any user inputs have been made and run the associated function
        for user_input in self.user_inputs:
            if self.user_inputs[user_input].run:
                self.user_inputs[user_input].function()
                self.user_inputs[user_input].run = False
        
        # Update the connection status in the bottom bar
        self.bottom_bar.update_comms_text(Transmission().connected)
        
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
    
    # Add a tab to the dashboard. Creates a new tab and grid for the tab
    def add_tab(self, tab_name):
        if tab_name not in self.tabs.keys():
            self.tab_bar.add_tab(tab_name)
            self.grid_graphics.create_new_tab_grid(tab_name)