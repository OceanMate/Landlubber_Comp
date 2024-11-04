
from tkinter import Button, Canvas

from dashboard.GraphicConstants import GraphicConstants
from dashboard.graphics.UserInput import UserInput
from structure.RobotState import RobotState

import tkinter.font as tkfont

class BottomBar():
    def __init__(self, window, user_inputs):
        self.window = window
        self.user_inputs = user_inputs
    
    def create_bottom_bar(self):
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
    
    def resize_bottom_bar(self):
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
        