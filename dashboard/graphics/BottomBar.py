
from tkinter import Button, Canvas

from dashboard.GraphicConstants import GraphicConstants
from dashboard.graphics.UserInput import UserInput
from structure.RobotState import RobotState

import tkinter.font as tkfont

class BottomBar():
    def __init__(self, window, user_inputs):
        self.window = window
        self.user_inputs = user_inputs
        
        # Measure the pixel width of the disable text
        self.bottom_bar_font = tkfont.Font(family=GraphicConstants().bottom_bar_font, size=16)
        self.enable_button_width = self.bottom_bar_font.measure("Disable") + 10
        
        # Measure the pixel length of the controller text
        self.controller_label_width = self.bottom_bar_font.measure("Controller: ")
        
        # Some constants for the enable button
        self.button_y_offset = 5
        self.button_x_offset = 5
        
        # Some constants for the controller text
        self.controller_x_offset = 5
        self.controller_y_offset = 10
    
    def create_bottom_bar(self):
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
        
        
        # Place the enable button on the bottom bar
        self.enable_button.place(
            x=GraphicConstants().window_width - self.enable_button_width - self.button_x_offset,
            y= self.button_y_offset,
            height=GraphicConstants().bottom_bar_height - 2 * self.button_y_offset,
            width=self.enable_button_width
        )
        


        # Create the rectangle for the controller label
        self.bottom_bar_canvas.create_rectangle(
            self.controller_x_offset,
            self.controller_y_offset,
            self.bottom_bar_font.measure("Controller: Gamepad F310") + 5 + self.controller_x_offset * 2, # measured width of "Controller: Gamepad F310"
            GraphicConstants().bottom_bar_height - self.controller_y_offset,
            fill=GraphicConstants().dark_grey,
            outline=GraphicConstants().dark_grey
        )
        
        # Create the text for the controller label
        self.bottom_bar_canvas.create_text(
            self.controller_x_offset + 5,
            GraphicConstants().bottom_bar_height // 2,
            text="Controller: ",
            fill=GraphicConstants().black,
            anchor="w",
            font=self.bottom_bar_font
        )
        
        # Create the text for the controller
        self.controller_text = self.bottom_bar_canvas.create_text(
            10 + self.controller_label_width,
            GraphicConstants().bottom_bar_height // 2,
            text="None",
            fill=GraphicConstants().red,
            anchor="w",
            font=self.bottom_bar_font
        )
    
    def resize_bottom_bar(self):
        self.bottom_bar_canvas.config(width=GraphicConstants().window_width)
        self.bottom_bar_canvas.place(x=0, y=GraphicConstants().window_height - GraphicConstants().bottom_bar_height, anchor="nw")
        
        
        self.enable_button.place(
            x=GraphicConstants().window_width - self.enable_button_width - self.button_x_offset,
            y= self.button_y_offset,
            height=GraphicConstants().bottom_bar_height - 2 * self.button_y_offset,
            width=self.enable_button_width
        )

        self.bottom_bar_canvas.coords(
            1,
            self.controller_x_offset,
            self.controller_y_offset,
            self.bottom_bar_font.measure("Controller: Gamepad F310") + 5 + self.controller_x_offset * 2,
            GraphicConstants().bottom_bar_height - self.controller_y_offset
        )
        
        self.bottom_bar_canvas.coords(
            2,
            self.controller_x_offset + 5,
            GraphicConstants().bottom_bar_height // 2
        )
        
        self.bottom_bar_canvas.coords(
            3,
            10 + self.controller_label_width,
            GraphicConstants().bottom_bar_height // 2
        )
    
    # Update the controller text to the given controller name
    def update_controller_text(self, controller_name):
        if controller_name == "None":
            self.bottom_bar_canvas.itemconfig(self.controller_text, fill=GraphicConstants().red)
        else:
            self.bottom_bar_canvas.itemconfig(self.controller_text, fill=GraphicConstants().dark_green)
        self.bottom_bar_canvas.itemconfig(self.controller_text, text= controller_name)
        