
import sys
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from typing import Callable

from dashboard.GraphicConstants import GraphicConstants
from dashboard.StringWidget import StringWidget
from structure.RobotState import RobotState

class UserInput:
    run : bool = True
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
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self._disable)
        
        # Create canvas like the window but allows for drawing
        self.canvas = Canvas(
            self.window,
            bg = GraphicConstants().white,
            height = GraphicConstants().window_height,
            width = GraphicConstants().window_width,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        
        self._generate_tab_bar()
        self._generate_grid()
        self._bottom_bar()
        
        self.canvas.pack()
        
        # Enable the dashboard
        self.enable = True
        
    def _generate_grid(self):
        for i in range(GraphicConstants().grid_dim, GraphicConstants().window_width, GraphicConstants().grid_dim):
            color = GraphicConstants().middle_blue if (i // GraphicConstants().grid_dim) % 5 == 0 else GraphicConstants().light_blue
            width = 2 if (i // GraphicConstants().grid_dim) % 5 == 0 else 1
            
            self.canvas.create_line(i, GraphicConstants().tab_bar_height, i, GraphicConstants().window_height, fill=color, width=width)
    
        for i in range(GraphicConstants().tab_bar_height + GraphicConstants().grid_dim, GraphicConstants().window_height, GraphicConstants().grid_dim):
            color = GraphicConstants().middle_blue if ((i - GraphicConstants().tab_bar_height) // GraphicConstants().grid_dim) % 5 == 0 else GraphicConstants().light_blue
            width = 2 if ((i - GraphicConstants().tab_bar_height) // GraphicConstants().grid_dim) % 5 == 0 else 1
            
            self.canvas.create_line(0, i, GraphicConstants().window_width, i, fill=color, width=width)
    
    def _generate_tab_bar(self):
        self.canvas.create_rectangle(
            0, 0, GraphicConstants().window_width, GraphicConstants().tab_bar_height,
            fill=GraphicConstants().blue,
            outline=""
        )
    
    def put_string(self, label, text, grid_x, grid_y):
        if self.canvas is None:
            return
        if label not in self.widgets:
            self.widgets[label] = StringWidget(self.canvas, label)
            self.widgets[label].create_string_widget(grid_x, grid_y, text)
        else:
            self.widgets[label].update_text(text)
            self.widgets[label].move_widget(grid_x, grid_y)
    
    def update(self):
        self.window.update()
        for user_input in self.user_inputs:
            if self.user_inputs[user_input].run:
                self.user_inputs[user_input].function()
                self.user_inputs[user_input].run = False
        
        if not self.enable:
            self.close()
    
    def _bottom_bar(self):
        px_height = 70
        button_y_offset = 5
        button_x_offset = 5
        button_width = 100
        
        bottom_bar = self.canvas.create_rectangle(
            0, GraphicConstants().window_height - px_height, GraphicConstants().window_width, GraphicConstants().window_height,
            fill=GraphicConstants().light_grey,
            outline=""
        )
        
        def _enable_robot():
            robot_state = RobotState()
            if not robot_state.is_teleop_enabled():
                robot_state.enable_teleop()
                enable_button.config(fg=GraphicConstants().red)
                enable_button.config(text="Disable")
            
            elif robot_state.is_teleop_enabled():
                robot_state.disable_robot()
                enable_button.config(fg=GraphicConstants().dark_green)
                enable_button.config(text="Enable")
        
        def _enable_button_press():
            self.user_inputs["enable button"].run = True

        self.user_inputs["enable button"] = UserInput()
        self.user_inputs["enable button"].function = _enable_robot
        
        enable_button = Button(
            self.canvas,
            text="Enable",
            bg=GraphicConstants().dark_grey,
            fg=GraphicConstants().dark_green,
            font=("Arial", 16),
            command=_enable_button_press,
        )
        
        enable_button.place(
            x=GraphicConstants().window_width - button_width - button_x_offset,
            y=GraphicConstants().window_height - px_height + button_y_offset,
            height=px_height - 2 * button_y_offset,
            width=button_width
        )
    
    def close(self):
        self.window.destroy()
        sys.exit(0)
    
    def _disable(self):
        self.enable = False