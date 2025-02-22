from tkinter import Canvas, OptionMenu
from jigboard.GraphicConstants import GraphicConstants
from jigboard.graphics.GridGraphics import GridGraphics
from transmission.ComsThread import ComsThread
import tkinter.font as tkfont


class NetworkData:  
    _instance = None
        
    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance        
    
    def init(self, window):
        # Store the  window for use in the grid
        self.window = window
        self.robot_state = ComsThread().robot_state
        self.sensor_data = ComsThread().sensor_data
        
        self.font = tkfont.Font(family=GraphicConstants().font, size=12)
        self.data_spacing = 20
        
        self.generate_grid()
        
    def generate_grid(self):
        # Create the canvas
        self.network_data_canvas = Canvas(
            self.window,
            bg = GraphicConstants().white,
            width = GraphicConstants().network_data_width,
            height= GraphicConstants().window_height-GraphicConstants().tab_bar_height-GraphicConstants().bottom_bar_height,
            relief = "ridge"
        )
        
        GridGraphics().move_grid(GraphicConstants().network_data_width, GraphicConstants().tab_bar_height)
        self.network_data_canvas.place(x=0, y=GraphicConstants().tab_bar_height, anchor="nw")
        
        self.draw_network_data()

    def draw_network_data(self):
        # Clear the canvas
        self.network_data_canvas.delete("all")
        
        # Create the header text
        y = 10
        self.network_data_canvas.create_text(
            10, y, 
            anchor="nw", 
            text="Sensor Data", 
            fill="black",
            font=self.font,
        )
        
        # Draw the sensor data
        y = self.dictionary_list(self.sensor_data, y+self.data_spacing) + self.data_spacing
        
        # Create the header text for the robot state
        self.network_data_canvas.create_text(
            10, y, 
            anchor="nw", 
            text="Robot State", 
            fill="black",
            font=self.font,
        )
        
        # Draw the robot state data
        self.dictionary_list(self.robot_state, y+self.data_spacing)

    # Create function to display the dictionary data on the canvas
    def dictionary_list(self, dictionary, initial_y):
        y_position = initial_y ;int
        
        # Iterate through the dictionary and create text for each key-value pair
        for key, value in dictionary.items():
            self.network_data_canvas.create_text(
                20, y_position, 
                anchor="nw", 
                text=f"{key}: {value}", 
                fill="black",
                font=self.font,
            )
            y_position += self.data_spacing
        return y_position
            
        
        
        
    def resize_canvas(self):
        # Resize the canvas to fit the new window dimensions
        self.network_data_canvas.config(width=GraphicConstants().network_data_width)
        px_grid_height = GraphicConstants().window_height - GraphicConstants().tab_bar_height - GraphicConstants().bottom_bar_height
        self.network_data_canvas.config(height=px_grid_height)
        
        GridGraphics().move_grid(GraphicConstants().network_data_width, GraphicConstants().tab_bar_height)
        
                
    def destroy_grid(self):
        GridGraphics().move_grid(0,GraphicConstants().tab_bar_height)
        self.network_data_canvas.destroy()