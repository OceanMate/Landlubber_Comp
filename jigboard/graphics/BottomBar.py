from tkinter import Button, Canvas, Menu

from jigboard.GraphicConstants import GraphicConstants
from structure.RobotState import RobotState

import tkinter.font as tkfont

import time


class BottomBar():
    def __init__(self, window):
        self.window = window
        
        # Measure the pixel width of the disable text
        self.bottom_bar_font = tkfont.Font(family=GraphicConstants().bottom_bar_font, size=16)
        
        # Text for the controller and connection status
        self.controller_label = "Controller: "
        self.connection_label = "Comp-Comms: "
        
        # Measure the pixel length of the controller text
        self.enable_button_width = self.bottom_bar_font.measure("Disable") + 10
        self.controller_label_width = self.bottom_bar_font.measure(self.controller_label)
        self.connection_label_width = self.bottom_bar_font.measure(self.connection_label)
        
        # Some constants for the enable button
        self.button_y_offset = 5
        self.button_x_offset = 5
        
        # Some constants for the controller text
        self.connections_x_offset = 5
        self.connections_y_offset = 5
        
        # Initialize the flash comms variable
        self.flash_comms = False
        self.start_flash_clk = False
    
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
            if not robot_state.is_enabled():
                match self.robot_mode:
                    case "Teleop":
                        if not robot_state.enable_teleop():
                            # Flash the connection status text if not connected to the nautical computer
                            self.flash_comms = True
                            return
                    case "Test":
                        if not robot_state.enable_test():
                            self.flash_comms = True
                            return
                    case _:
                        # Handle unexpected modes
                        print("Unknown mode")
                        
                # switch the color and text of the enable button to reflect the new state
                self.update_enable_button(is_enabling=True)
            
            else:
                # the switching of the button text and color is handled in the disable_robot function
                robot_state.disable_robot()
                self.update_enable_button(is_enabling=False)

        # Function to handle mode selection
        def select_mode(mode):
            robot_state = RobotState()
            if robot_state.is_enabled():
                robot_state.disable_robot()
                self.update_enable_button(is_enabling=False)
            if mode == "Teleop":
                
                self.mode_menu_button.config(text="Teleop")
            elif mode == "Test":
                self.mode_menu_button.config(text="Test")
            
            self.robot_mode = mode

        # Create the menu button for mode selection
        self.mode_menu_button = Button(
            self.bottom_bar_canvas,
            text="Teleop",
            bg=GraphicConstants().mild_grey,
            fg=GraphicConstants().black,
            font=(GraphicConstants().bottom_bar_font, 14),  # Slightly smaller font for better fit
            relief="groove",  # Add a subtle border for better appearance
            bd=5  # Border width
        )

        # Create the dropdown menu for the mode button
        self.mode_menu = Menu(self.mode_menu_button, tearoff=0)
        self.mode_menu.add_command(label="Teleop", command=lambda: select_mode("Teleop"))
        self.mode_menu.add_command(label="Test", command=lambda: select_mode("Test"))
        self.robot_mode = "Teleop"  # Initial mode

        # Bind the menu to the button
        self.mode_menu_button.config(command=lambda: self.mode_menu.post(
            self.mode_menu_button.winfo_rootx(),
            self.mode_menu_button.winfo_rooty() + self.mode_menu_button.winfo_height()
        ))

        # Place the mode menu button to the left of the enable button
        self.mode_menu_button.place(
            x=GraphicConstants().window_width - 2 * self.enable_button_width - self.button_x_offset - 10,
            y=self.button_y_offset + 2,  # Slightly adjust vertical position for alignment
            height=GraphicConstants().bottom_bar_height - 2 * self.button_y_offset - 4,  # Reduce height for a thinner look
            width=self.enable_button_width - 20  # Reduce width for a sleeker appearance
        )

        # Create the enable button
        self.enable_button = Button(
            self.bottom_bar_canvas,
            text="Enable",
            bg=GraphicConstants().dark_grey,
            fg=GraphicConstants().dark_green,
            font=(GraphicConstants().bottom_bar_font, 16),
            command=enable_robot,
        )
        
        
        # Place the enable button on the bottom bar
        self.enable_button.place(
            x=GraphicConstants().window_width - self.enable_button_width - self.button_x_offset,
            y= self.button_y_offset,
            height=GraphicConstants().bottom_bar_height - 2 * self.button_y_offset,
            width=self.enable_button_width
        )
        
        largest_text = max(self.controller_label_width, self.connection_label_width)

        largest_variable_text = self.bottom_bar_font.measure("Disconnected")

        # Create the rectangle for the connection labels
        self.bottom_bar_canvas.create_rectangle(
            self.connections_x_offset,
            self.connections_y_offset,
            largest_text + largest_variable_text + 5 + self.connections_x_offset * 2, # measured width of the connection status text
            GraphicConstants().bottom_bar_height - self.connections_y_offset,
            fill=GraphicConstants().dark_grey,
            outline=GraphicConstants().dark_grey
        )
        
        # Create the text for the controller label
        self.bottom_bar_canvas.create_text(
            self.connections_x_offset + 5 + largest_text - self.controller_label_width,
            GraphicConstants().bottom_bar_height * (1/3),
            text=self.controller_label,
            fill=GraphicConstants().black,
            anchor="w",
            font=self.bottom_bar_font
        )
        
        # Create the text for the controller
        self.controller_text = self.bottom_bar_canvas.create_text(
            largest_text + self.connections_x_offset,
            GraphicConstants().bottom_bar_height * (1/3),  # Adjust the y position as needed
            text="None",
            fill=GraphicConstants().red,
            anchor="w",
            font=self.bottom_bar_font
        )

        # Create the text for the Nautical Computer label
        self.bottom_bar_canvas.create_text(
            self.connections_x_offset + 5 + largest_text - self.connection_label_width,
            GraphicConstants().bottom_bar_height * (2/3), 
            text=self.connection_label,
            fill=GraphicConstants().black,
            anchor="w",
            font=self.bottom_bar_font
        )

        # Create the text for the Nautical Computer connection status
        self.comms_text = self.bottom_bar_canvas.create_text(
            self.connections_x_offset + largest_text,
            GraphicConstants().bottom_bar_height * (2/3),  # Adjust the y position as needed
            text="Disconnected",
            fill=GraphicConstants().red,
            anchor="w",
            font=self.bottom_bar_font
        )
    
    def resize_bottom_bar(self):
        self.bottom_bar_canvas.config(width=GraphicConstants().window_width)
        self.bottom_bar_canvas.place(x=0, y=GraphicConstants().window_height - GraphicConstants().bottom_bar_height, anchor="nw")
        
        self.mode_menu_button.place(
            x=GraphicConstants().window_width - 2 * self.enable_button_width - self.button_x_offset - 10,
            y=self.button_y_offset + 2,  # Slightly adjust vertical position for alignment
            height=GraphicConstants().bottom_bar_height - 2 * self.button_y_offset - 4,  # Reduce height for a thinner look
            width=self.enable_button_width - 20  # Reduce width for a sleeker appearance
        )
        
        self.enable_button.place(
            x=GraphicConstants().window_width - self.enable_button_width - self.button_x_offset,
            y= self.button_y_offset,
            height=GraphicConstants().bottom_bar_height - 2 * self.button_y_offset,
            width=self.enable_button_width
        )
    
    # Update the controller text to the given controller name
    def update_controller_text(self, controller_name):
        if (controller_name == "None"):
            self.bottom_bar_canvas.itemconfig(self.controller_text, fill=GraphicConstants().red)
        else:
            self.bottom_bar_canvas.itemconfig(self.controller_text, fill=GraphicConstants().dark_green)
        self.bottom_bar_canvas.itemconfig(self.controller_text, text= controller_name)

    # Update the Nautical Computer connection status text
    def update_comms_text(self, is_connected : bool):
        # Record the inital time for flashing the connection status text
        if self.flash_comms:
            self.start_flash_clk = True
            self.flash_comms = False
            self.comms_clk = time.time()
        
        # If the connection status text has been flashing for more than a second, stop flashing
        if self.start_flash_clk and time.time() - self.comms_clk > 1:
            self.start_flash_clk = False
        
        # Update the connection status text
        if not is_connected:
            self.bottom_bar_canvas.itemconfig(self.comms_text, fill=GraphicConstants().red)
            self.bottom_bar_canvas.itemconfig(self.comms_text, text="Disconnected")
        else:
            self.bottom_bar_canvas.itemconfig(self.comms_text, fill=GraphicConstants().dark_green)
            self.bottom_bar_canvas.itemconfig(self.comms_text, text="Connected")
            
        # Flash the connection status text by changing the color every 1/5 second
        if self.start_flash_clk:
            if (time.time() - self.comms_clk) % 0.2 < 0.1:
                if is_connected:
                    self.bottom_bar_canvas.itemconfig(self.comms_text, fill=GraphicConstants().dark_green)
                else:
                    self.bottom_bar_canvas.itemconfig(self.comms_text, fill=GraphicConstants().red)
            else:
                self.bottom_bar_canvas.itemconfig(self.comms_text, fill=GraphicConstants().orange)
    
    def update_enable_button(self, is_enabling):
        if is_enabling:
            self.enable_button.config(fg=GraphicConstants().red)
            self.enable_button.config(text="Disable")
        else:
            self.enable_button.config(fg=GraphicConstants().dark_green)
            self.enable_button.config(text="Enable")
