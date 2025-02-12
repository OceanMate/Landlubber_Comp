from tkinter import Canvas
from jigboard.GraphicConstants import GraphicConstants
from jigboard.graphics.GridGraphics import GridGraphics


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
                
    def destroy_grid(self):
        GridGraphics().move_grid(0,GraphicConstants().tab_bar_height)
        self.network_data_canvas.destroy()