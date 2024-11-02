import sys
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from typing import Callable
import ctypes
from pathlib import Path

from dashboard.GraphicConstants import GraphicConstants
from dashboard.GridManager import GridManager
from dashboard.StringWidget import StringWidget
import tkinter.font as tkfont
from structure.RobotState import RobotState


# UserInput class to store user input then run the function in the update loop
# prevents the user input events from crashing the program
class UserInput:
    run : bool = False
    # this is any function that takes no arguments
    function : Callable

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
        self.widgets = {}
        self.user_inputs = {}
             
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
        self.window.iconbitmap(self.get_asset_path("rabbit_logo.ico"))
        
        # Generate the various components of the dashboard
        self._generate_tab_bar()
        self._generate_grid()
        self._bottom_bar()
        
        # Enable the dashboard
        self.enable = True
  
    def get_asset_path(self, path: str) -> Path:
        return Path(__file__).parent / "assets" / path
    
    # Generate the grid on the canvas which the widgets will be placed on
    def _generate_grid(self):
        # Calculate the height of the grid
        grid_height = GraphicConstants().window_height - GraphicConstants().tab_bar_height - GraphicConstants().bottom_bar_height
        # Create the grid manager which will keep track of the available space on the grid
        self.grid_manager = GridManager(GraphicConstants().window_width // GraphicConstants().grid_dim, grid_height // GraphicConstants().grid_dim)
        
        # Create the canvas for the grid
        self.grid_canvas = Canvas(
            self.window,
            bg = GraphicConstants().white,
            height = grid_height,
            width = GraphicConstants().window_width,
            relief = "ridge"
        )
        
        self.grid_canvas.place(x=0, y=GraphicConstants().tab_bar_height, anchor="nw")
        
        # Draw the vertical grid lines, with thicker lines every 5 grid spaces
        for i in range(GraphicConstants().grid_dim, GraphicConstants().window_width, GraphicConstants().grid_dim):
            color = GraphicConstants().middle_blue if (i // GraphicConstants().grid_dim) % 5 == 0 else GraphicConstants().light_blue
            width = 2 if (i // GraphicConstants().grid_dim) % 5 == 0 else 1
            
            self.grid_canvas.create_line(i, 0, i, grid_height, fill=color, width=width)
    
        # Draw the horizontal grid lines, with thicker lines every 5 grid spaces
        for i in range(GraphicConstants().grid_dim, grid_height, GraphicConstants().grid_dim):
            color = GraphicConstants().middle_blue if (i // GraphicConstants().grid_dim) % 5 == 0 else GraphicConstants().light_blue
            width = 2 if (i // GraphicConstants().grid_dim) % 5 == 0 else 1
            
            self.grid_canvas.create_line(0, i, GraphicConstants().window_width, i, fill=color, width=width)
    
    # Generate the tab bar at the top of the window (currently unused)
    def _generate_tab_bar(self):
        self.tab_bar_canvas = Canvas(
            self.window,
            bg = GraphicConstants().blue,
            height = GraphicConstants().tab_bar_height,
            width = GraphicConstants().window_width,
            relief = "ridge"
        )
        
        self.tab_bar_canvas.place(x=0, y=0, anchor="nw")
    
    # Create a string widget on the dashboard, or can be called multiple times to update the text of the widget
    def put_string(self, label, text):
        if self.grid_canvas is None:
            return
        
        if label not in self.widgets.keys():
            # Create a new widget if it doesn't already exist
            self.widgets[label] = StringWidget(self.grid_canvas, label)
            wigit_grid_width, wigit_grid_height = self.widgets[label].get_default_dimensions()
            
            # Find the next available space for the widget, and tell the grid manager to place the widget there
            loc = self.grid_manager.find_next_available_space(wigit_grid_width, wigit_grid_height)
            self.grid_manager.place_rectangle(loc[0], loc[1], wigit_grid_width, wigit_grid_height)
            
            # Create the widget on the canvas
            self.widgets[label].create_string_widget(loc[0], loc[1], text)
        else:
            # Update the text of the widget if it already exists
            self.widgets[label].update_text(text)

    # Function that should be called periodicly to update the dashboard
    def update(self):        

        # Update the window, use this instead of mainloop to allow for other functions to be called (non-blocking)
        self.window.update()
        
        # Check if any user inputs have been made and run the associated function
        for user_input in self.user_inputs:
            if self.user_inputs[user_input].run:
                self.user_inputs[user_input].function()
                self.user_inputs[user_input].run = False
        
        # Check if the dashboard has been disabled, and close the window if it has
        if not self.enable:
            self._close()
    
    def _bottom_bar(self):
        # Some constants for the enable button
        button_y_offset = 5
        button_x_offset = 5
        button_width = 100
        
        # Create the canvas for the bottom bar
        self.bottom_bar_canvas = Canvas(
            self.window,
            bg = GraphicConstants().light_grey,
            height = GraphicConstants().bottom_bar_height,
            width = GraphicConstants().window_width,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        
        self.bottom_bar_canvas.place(x=0, y=GraphicConstants().window_height - GraphicConstants().bottom_bar_height, anchor="nw")
        
        # Function to enable or disable the robot and update the button text
        def enable_robot():
            robot_state = RobotState()
            if not robot_state.is_teleop_enabled():
                robot_state.enable_teleop()
                enable_button.config(fg=GraphicConstants().red)
                enable_button.config(text="Disable")
            
            elif robot_state.is_teleop_enabled():
                robot_state.disable_robot()
                enable_button.config(fg=GraphicConstants().dark_green)
                enable_button.config(text="Enable")

        # Create the enable button and add it to the user inputs
        self.user_inputs["enable_button"] = UserInput()
        self.user_inputs["enable_button"].function = enable_robot
        
        # Function that is called when the enable button is pressed, sets its associated user input to run
        def enable_button_press():
            self.user_inputs["enable_button"].run = True
        
        # Create the enable button
        enable_button = Button(
            self.bottom_bar_canvas,
            text="Enable",
            bg=GraphicConstants().dark_grey,
            fg=GraphicConstants().dark_green,
            font=("Arial", 16),
            command=enable_button_press,
        )
        
        enable_button.place(
            x=GraphicConstants().window_width - button_width - button_x_offset,
            y= button_y_offset,
            height=GraphicConstants().bottom_bar_height - 2 * button_y_offset,
            width=button_width
        )
        
        controller_font = tkfont.Font(family="Arial", size=16)
        text_width = controller_font.measure("Controller: ")

        # Create a text to display the current controller connected
        self.bottom_bar_canvas.create_text(
            10,
            GraphicConstants().bottom_bar_height // 2,
            text="Controller: ",
            fill=GraphicConstants().black,
            anchor="w",
            font=("Arial", 16)
        )
        
        self.controller_text = self.bottom_bar_canvas.create_text(
            10 + text_width,
            GraphicConstants().bottom_bar_height // 2,
            text="None",
            fill=GraphicConstants().black,
            anchor="w",
            font=("Arial", 16)
        )
    
    def update_controller_text(self, controller_name):
        self.bottom_bar_canvas.itemconfig(self.controller_text, text= controller_name)
    
    
    # Close the window and exit the program
    def _close(self):
        self.window.destroy()
        sys.exit(0)
    
    # Disable the dashboard
    def _disable(self):
        self.enable = False