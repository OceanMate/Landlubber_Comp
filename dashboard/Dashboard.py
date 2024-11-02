import sys
import time
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from typing import Callable
import ctypes
from pathlib import Path

from dashboard.GraphicConstants import GraphicConstants
from dashboard.GridManager import GridManager
from dashboard.StringWidget import StringWidget
import tkinter.font as tkfont
from structure.Input.EventLoop import EventLoop
from structure.Input.KeyboardInput import KeyboardInput
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
        
        self.setup_hotkeys()
        
        # Enable the dashboard
        self.enable = True
  
    def setup_hotkeys(self):
        # Event loop for the dashboard for hotkeys
        self.dashboard_hotkeys_loop = EventLoop()
        
        def on_enter():
            if RobotState().is_teleop_enabled():
                RobotState().disable_robot()
                self.enable_button.config(fg=GraphicConstants().dark_green)
                self.enable_button.config(text="Enable")
        
        enter_hotkey = KeyboardInput("enter")
        enter_hotkey.non_cmd_on_true(func=on_enter)
        enter_hotkey.set_loop(loop=self.dashboard_hotkeys_loop)
        
  
    # Get the path of an asset in the assets folder
    def get_asset_path(self, path: str) -> Path:
        return Path(__file__).parent / "assets" / path
    
    # Generate the grid on the canvas which the widgets will be placed on
    def _generate_grid(self):
        # Calculate the height of the grid
        grid_height = GraphicConstants().window_height - GraphicConstants().tab_bar_height - GraphicConstants().bottom_bar_height
        # Create the grid manager which will keep track of the available space on the grid
        self.grid_manager = GridManager()
        self.grid_manager.init(GraphicConstants().window_width // GraphicConstants().grid_dim, grid_height // GraphicConstants().grid_dim)
        
        # Create the canvas for the grid
        self.grid_canvas = Canvas(
            self.window,
            bg = GraphicConstants().white,
            height = grid_height,
            width = GraphicConstants().window_width,
            relief = "ridge"
        )
        
        self.grid_canvas.place(x=0, y=GraphicConstants().tab_bar_height, anchor="nw")
        
        # Load the image
        self.rabbit_logo = PhotoImage(file=self.get_asset_path("white_logo.png"))
        
        # Calculate the position to place the image in the center of the grid
        logo_x = (GraphicConstants().window_width - self.rabbit_logo.width()) // 2
        logo_y = (grid_height - self.rabbit_logo.height()) // 2
        
        # Create the image on the canvas with slight transparency
        self.background_image = self.grid_canvas.create_image(logo_x, logo_y, image=self.rabbit_logo, anchor="nw")
        
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

        self.grid_canvas.bind("<Button-1>", self.on_mouse_click)
        self.grid_canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
    
    def _resize_grid(self):
        self.grid_canvas.config(width=GraphicConstants().window_width)
    
        grid_height = GraphicConstants().window_height - GraphicConstants().tab_bar_height - GraphicConstants().bottom_bar_height
        self.grid_canvas.config(height=grid_height)
        
        self.grid_manager.init(GraphicConstants().window_width // GraphicConstants().grid_dim, grid_height // GraphicConstants().grid_dim)
        
        # Calculate the position to place the image in the center of the grid
        logo_x = (GraphicConstants().window_width - self.rabbit_logo.width()) // 2
        logo_y = (grid_height - self.rabbit_logo.height()) // 2
        
        # Delete the previous image if it exists
        if self.background_image is not None:
            self.grid_canvas.delete(self.background_image)
        
        # Create the image on the canvas with slight transparency
        self.background_image = self.grid_canvas.create_image(logo_x, logo_y, image=self.rabbit_logo, anchor="nw")
        
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
    
    def _resize_tab_bar(self):
        self.tab_bar_canvas.config(width=GraphicConstants().window_width)
    
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
        
        if GraphicConstants().window_width != self.window.winfo_width() or GraphicConstants().window_height != self.window.winfo_height():
            GraphicConstants().window_width = self.window.winfo_width()
            GraphicConstants().window_height = self.window.winfo_height()
            
            self._resize_tab_bar()
            self._resize_grid()
            self._resize_bottom_bar()
            
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
    
    def _bottom_bar(self):
        # Some constants for the enable button
        button_y_offset = 5
        button_x_offset = 5
        
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
                self.enable_button.config(fg=GraphicConstants().red)
                self.enable_button.config(text="Disable")
            
            elif robot_state.is_teleop_enabled():
                robot_state.disable_robot()
                self.enable_button.config(fg=GraphicConstants().dark_green)
                self.enable_button.config(text="Enable")

        # Create the enable button and add it to the user inputs
        self.user_inputs["enable_button"] = UserInput()
        self.user_inputs["enable_button"].function = enable_robot
        
        # Function that is called when the enable button is pressed, sets its associated user input to run
        def enable_button_press():
            self.user_inputs["enable_button"].run = True
        
        # Create the enable button
        self.enable_button = Button(
            self.bottom_bar_canvas,
            text="Enable",
            bg=GraphicConstants().dark_grey,
            fg=GraphicConstants().dark_green,
            font=(GraphicConstants().bottom_bar_font, 16),
            command=enable_button_press,
        )
        
        bottom_bar_font = tkfont.Font(family=GraphicConstants().bottom_bar_font, size=16)
        enable_button_width = bottom_bar_font.measure("Disable") + 10
        
        self.enable_button.place(
            x=GraphicConstants().window_width - enable_button_width - button_x_offset,
            y= button_y_offset,
            height=GraphicConstants().bottom_bar_height - 2 * button_y_offset,
            width=enable_button_width
        )
        
        text_width = bottom_bar_font.measure("Controller: ")
        
        x_offset = 5
        y_offset = 10

        # Create a text to display the current controller connected
        self.bottom_bar_canvas.create_rectangle(
            x_offset,
            y_offset,
            bottom_bar_font.measure("Controller: Gamepad F310") + 5 + x_offset * 2,
            GraphicConstants().bottom_bar_height - y_offset,
            fill=GraphicConstants().dark_grey,
            outline=GraphicConstants().dark_grey
        )
        
        self.bottom_bar_canvas.create_text(
            x_offset + 5,
            GraphicConstants().bottom_bar_height // 2,
            text="Controller: ",
            fill=GraphicConstants().black,
            anchor="w",
            font=bottom_bar_font
        )
        
        self.controller_text = self.bottom_bar_canvas.create_text(
            10 + text_width,
            GraphicConstants().bottom_bar_height // 2,
            text="None",
            fill=GraphicConstants().red,
            anchor="w",
            font=bottom_bar_font
        )
    
    def _resize_bottom_bar(self):
        self.bottom_bar_canvas.config(width=GraphicConstants().window_width)
        self.bottom_bar_canvas.place(x=0, y=GraphicConstants().window_height - GraphicConstants().bottom_bar_height, anchor="nw")
        
        button_y_offset = 5
        button_x_offset = 5
        button_width = 100
        
        self.enable_button.place(
            x=GraphicConstants().window_width - button_width - button_x_offset,
            y= button_y_offset,
            height=GraphicConstants().bottom_bar_height - 2 * button_y_offset,
            width=button_width
        )
        
        controller_font = tkfont.Font(family=GraphicConstants().bottom_bar_font, size=16)
        text_width = controller_font.measure("Controller: ")
        
        x_offset = 5
        y_offset = 10

        self.bottom_bar_canvas.coords(
            1,
            x_offset,
            y_offset,
            controller_font.measure("Controller: Gamepad F310") + 5 + x_offset * 2,
            GraphicConstants().bottom_bar_height - y_offset
        )
        
        self.bottom_bar_canvas.coords(
            2,
            x_offset + 5,
            GraphicConstants().bottom_bar_height // 2
        )
        
        self.bottom_bar_canvas.coords(
            3,
            10 + text_width,
            GraphicConstants().bottom_bar_height // 2
        )
    
    def update_controller_text(self, controller_name):
        if controller_name == "None":
            self.bottom_bar_canvas.itemconfig(self.controller_text, fill=GraphicConstants().red)
        else:
            self.bottom_bar_canvas.itemconfig(self.controller_text, fill=GraphicConstants().dark_green)
        self.bottom_bar_canvas.itemconfig(self.controller_text, text= controller_name)
    
    
    # Close the window and exit the program
    def _close(self):
        self.window.destroy()
        sys.exit(0)
    
    # Disable the dashboard
    def _disable(self):
        self.enable = False
        
    def on_mouse_click(self,event):
        #print("clicked at: " + str(event.x) + ", " + str(event.y))
        self.clk_start_time = time.time()
        
        self.widget_pressed = ""
        self.on_edge = False
        
        for key in self.widgets.keys():
            if(self.widgets[key].am_i_pressed(event.x, event.y)):
                #print("pressed on: " + key)
                self.widget_pressed = key
                
                self.x_offset = event.x - self.widgets[key].x
                self.y_offset = event.y - self.widgets[key].y
                
                if(self.widgets[key].am_i_pressed_on_edge(event.x, event.y)):
                    print("on edge")
                    self.on_edge = True
    
    def on_mouse_release(self, event):
        #print("released at: " + str(event.x) + ", " + str(event.y))
        #print("Time between clicks: " + str(time.time() - self.clk_start_time))
        
        if(time.time() - self.clk_start_time > 0.2):
            if(self.widget_pressed != ""):
                gridx,gridy = self.grid_manager.convert_pixel_to_grid(event.x-self.x_offset, event.y-self.y_offset)
                grid_width,grid_height = self.grid_manager.convert_pixel_to_grid(event.x-self.widgets[self.widget_pressed].width, event.y-self.widgets[self.widget_pressed].height)
                
                if(self.on_edge):
                    self.widgets[self.widget_pressed].resize_widget(grid_width, grid_height)
                else:        
                    self.widgets[self.widget_pressed].move_widget(gridx, gridy)
        