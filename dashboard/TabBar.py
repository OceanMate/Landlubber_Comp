from tkinter import Canvas

from dashboard.GraphicConstants import GraphicConstants


class TabBar:
    def __init__(self, window):
        self.window = window
    
    # Generate the tab bar at the top of the window (currently unused)
    def generate_tab_bar(self):
        self.tab_bar_canvas = Canvas(
            self.window,
            bg = GraphicConstants().blue,
            height = GraphicConstants().tab_bar_height,
            width = GraphicConstants().window_width,
            relief = "ridge"
        )
        
        self.tab_bar_canvas.place(x=0, y=0, anchor="nw")
    
    def resize_tab_bar(self):
        self.tab_bar_canvas.config(width=GraphicConstants().window_width)