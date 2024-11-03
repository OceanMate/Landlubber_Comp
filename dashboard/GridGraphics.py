import time
from tkinter import Canvas, PhotoImage
from dashboard.GraphicConstants import GraphicConstants


class GridGraphics:
    _instance = None
    
    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance        
    
    def init(self, window, widgets):
        self.window = window
        self.widgets = widgets
        
    
    # Generate the grid on the canvas which the widgets will be placed on
    def generate_grid(self):
        # Calculate the height of the grid
        px_grid_height = GraphicConstants().window_height - GraphicConstants().tab_bar_height - GraphicConstants().bottom_bar_height
        
        self.grid_width, self.grid_height = self.convert_pixel_to_grid(GraphicConstants().window_width, px_grid_height)
        
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        # Create the canvas for the grid
        self.grid_canvas = Canvas(
            self.window,
            bg = GraphicConstants().white,
            height = px_grid_height,
            width = GraphicConstants().window_width,
            relief = "ridge"
        )
        
        self.grid_canvas.place(x=0, y=GraphicConstants().tab_bar_height, anchor="nw")
        
        # Load the image
        self.rabbit_logo = PhotoImage(file=GraphicConstants().get_asset_path("white_logo.png"))
        
        # Calculate the position to place the image in the center of the grid
        logo_x = (GraphicConstants().window_width - self.rabbit_logo.width()) // 2
        logo_y = (px_grid_height - self.rabbit_logo.height()) // 2
        
        # Create the image on the canvas with slight transparency
        self.background_image = self.grid_canvas.create_image(logo_x, logo_y, image=self.rabbit_logo, anchor="nw")
        
        # Draw the vertical grid lines, with thicker lines every 5 grid spaces
        for i in range(GraphicConstants().grid_dim, GraphicConstants().window_width, GraphicConstants().grid_dim):
            color = GraphicConstants().middle_blue if (i // GraphicConstants().grid_dim) % 5 == 0 else GraphicConstants().light_blue
            width = 2 if (i // GraphicConstants().grid_dim) % 5 == 0 else 1
            
            self.grid_canvas.create_line(i, 0, i, px_grid_height, fill=color, width=width)
    
        # Draw the horizontal grid lines, with thicker lines every 5 grid spaces
        for i in range(GraphicConstants().grid_dim, px_grid_height, GraphicConstants().grid_dim):
            color = GraphicConstants().middle_blue if (i // GraphicConstants().grid_dim) % 5 == 0 else GraphicConstants().light_blue
            width = 2 if (i // GraphicConstants().grid_dim) % 5 == 0 else 1
            
            self.grid_canvas.create_line(0, i, GraphicConstants().window_width, i, fill=color, width=width)

        # Bind the left mouse click and release events to the canvas
        self.grid_canvas.bind("<Button-1>", self._on_mouse_click)
        self.grid_canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
    
    def resize_grid(self):
        self.grid_canvas.config(width=GraphicConstants().window_width)
    
        px_grid_height = GraphicConstants().window_height - GraphicConstants().tab_bar_height - GraphicConstants().bottom_bar_height
        self.grid_canvas.config(height=px_grid_height)
        
        self.grid_width, self.grid_height = self.convert_pixel_to_grid(GraphicConstants().window_width, px_grid_height)
        
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        # Calculate the position to place the image in the center of the grid
        logo_x = (GraphicConstants().window_width - self.rabbit_logo.width()) // 2
        logo_y = (px_grid_height - self.rabbit_logo.height()) // 2
        
        # Delete the previous image if it exists
        if self.background_image is not None:
            self.grid_canvas.delete(self.background_image)
        
        # Create the image on the canvas with slight transparency
        self.background_image = self.grid_canvas.create_image(logo_x, logo_y, image=self.rabbit_logo, anchor="nw")
        
        # Draw the vertical grid lines, with thicker lines every 5 grid spaces
        for i in range(GraphicConstants().grid_dim, GraphicConstants().window_width, GraphicConstants().grid_dim):
            color = GraphicConstants().middle_blue if (i // GraphicConstants().grid_dim) % 5 == 0 else GraphicConstants().light_blue
            width = 2 if (i // GraphicConstants().grid_dim) % 5 == 0 else 1
            
            self.grid_canvas.create_line(i, 0, i, px_grid_height, fill=color, width=width)
    
        # Draw the horizontal grid lines, with thicker lines every 5 grid spaces
        for i in range(GraphicConstants().grid_dim, px_grid_height, GraphicConstants().grid_dim):
            color = GraphicConstants().middle_blue if (i // GraphicConstants().grid_dim) % 5 == 0 else GraphicConstants().light_blue
            width = 2 if (i // GraphicConstants().grid_dim) % 5 == 0 else 1
            
            self.grid_canvas.create_line(0, i, GraphicConstants().window_width, i, fill=color, width=width)
    
    def _on_mouse_click(self,event):
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
    
    def _on_mouse_release(self, event):
        #print("released at: " + str(event.x) + ", " + str(event.y))
        #print("Time between clicks: " + str(time.time() - self.clk_start_time))
        
        if(time.time() - self.clk_start_time > 0.2):
            if(self.widget_pressed != ""):
                gridx,gridy = self.convert_pixel_to_grid(event.x-self.x_offset, event.y-self.y_offset)
                grid_width,grid_height = self.convert_pixel_to_grid(event.x-self.widgets[self.widget_pressed].width, event.y-self.widgets[self.widget_pressed].height)
                
                if(self.on_edge):
                    self.widgets[self.widget_pressed].resize_widget(grid_width, grid_height)
                else:        
                    self.widgets[self.widget_pressed].move_widget(gridx, gridy)

    # Check if a rectangle of rect_width x rect_height can be placed at x, y
    def can_place_rectangle(self, x, y, rect_width, rect_height):
        
        if x + rect_width > self.grid_width or y + rect_height > self.grid_height:
            return False
        for i in range(y, y + rect_height):
            for j in range(x, x + rect_width):
                if self.grid[i][j] != 0:
                    return False
        return True

    # "Place" a rectangle of rect_width x rect_height at x, y (set all values in the rectangle to 1 not actually place anything)
    def place_rectangle(self, x, y, rect_width, rect_height):
        
        for i in range(y, y + rect_height):
            for j in range(x, x + rect_width):
                self.grid[i][j] = 1
    
    # Remove a rectangle of rect_width x rect_height at x, y (set all values in the rectangle to 0)
    def remove_rectangle(self, x, y, rect_width, rect_height):
        
        for i in range(y, y + rect_height):
            for j in range(x, x + rect_width):
                self.grid[i][j] = 0

    # Find the next available space to place a rectangle of rect_width x rect_height
    def find_next_available_space(self, rect_width, rect_height):        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.can_place_rectangle(x, y, rect_width, rect_height):
                    return (x, y) # Tuple of the x and y coordinates
        return (-1, -1)
    
    def convert_pixel_to_grid(self, x, y):
        return x // GraphicConstants().grid_dim, y // GraphicConstants().grid_dim
    
