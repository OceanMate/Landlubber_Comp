import time
from tkinter import Canvas, PhotoImage
from dashboard.GraphicConstants import GraphicConstants
from dashboard.graphics.UserInput import UserInput


class GridGraphics:
    _instance = None
    
    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance        
    
    def init(self, window, tabs):
        self.window = window
        self.tabs = tabs
        
        self.grids = {}
        
    
    # Generate the grid on the canvas which the widgets will be placed on
    def generate_grid(self):
        # Calculate the height of the grid
        px_grid_height = GraphicConstants().window_height - GraphicConstants().tab_bar_height - GraphicConstants().bottom_bar_height
        
        self.grid_width, self.grid_height = self.convert_pixel_to_grid(GraphicConstants().window_width, px_grid_height)
        
        self.grids[GraphicConstants().default_tab] = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
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

        # Bind the left mouse click, release, and move events to the canvas
        self.grid_canvas.bind("<Button-1>", self._on_mouse_click)
        self.grid_canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
        self.grid_canvas.bind("<Motion>", self._on_mouse_move)
    
    def resize_grid(self):
        self.grid_canvas.config(width=GraphicConstants().window_width)
    
        px_grid_height = GraphicConstants().window_height - GraphicConstants().tab_bar_height - GraphicConstants().bottom_bar_height
        self.grid_canvas.config(height=px_grid_height)
        
        self.grid_width, self.grid_height = self.convert_pixel_to_grid(GraphicConstants().window_width, px_grid_height)
        
        for grid_keys in self.grids.keys():
            self.grids[grid_keys] = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
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
    
    def create_new_tab_grid(self, tab):
        self.grids[tab] = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    
    def _on_mouse_click(self,event):
        #print("clicked at: " + str(event.x) + ", " + str(event.y))
        self.clk_start_time = time.time()
        
        self.widget_pressed = ""
        self.is_resizing = False
        
        current_tab = GraphicConstants().current_tab
        for widget in self.tabs[current_tab].values():
            if(widget.is_pressed(event.x, event.y)):
                #print("pressed on: " + key)
                self.widget_pressed = widget.label
                
                self.x_offset = event.x - widget.x
                self.y_offset = event.y - widget.y
                
                self.edge_bools = widget.is_pressed_on_edge(event.x, event.y)
                if True in self.edge_bools:
                    self.is_resizing = True
    
    # TODO make move widget based of previous mouse location
    def _on_mouse_release(self, event):
        #print("released at: " + str(event.x) + ", " + str(event.y))
        #print("Time between clicks: " + str(time.time() - self.clk_start_time))
        current_tab = GraphicConstants().current_tab

        # Check if the widget is being resized
        if self.is_resizing:
            grid_x, grid_y = self.convert_pixel_to_grid(event.x, event.y)
            
            # Check if the widget is out of bounds
            grid_x = max(0, grid_x)
            grid_y = max(0, grid_y)
            grid_x = min(grid_x, self.grid_width - self.tabs[current_tab][self.widget_pressed].grid_width)
            grid_y = min(grid_y, self.grid_height - self.tabs[current_tab][self.widget_pressed].grid_height)
            
            
            self.tabs[GraphicConstants().current_tab][self.widget_pressed].resize_widget(grid_x, grid_y, self.edge_bools)
            
            return

        
        # Check if the widget is being moved
        if time.time() - self.clk_start_time > 0.2 and self.widget_pressed != "":
            grid_x, grid_y = self.convert_pixel_to_grid(event.x, event.y)
            
            # Check if the widget is out of bounds
            grid_x = max(0, grid_x)
            grid_y = max(0, grid_y)
            grid_x = min(grid_x, self.grid_width - self.tabs[current_tab][self.widget_pressed].grid_width)
            grid_y = min(grid_y, self.grid_height - self.tabs[current_tab][self.widget_pressed].grid_height)
            
            grid_x = grid_x - self.x_offset // GraphicConstants().grid_dim
            grid_y = grid_y - self.y_offset // GraphicConstants().grid_dim
            
            self.tabs[GraphicConstants().current_tab][self.widget_pressed].move_widget(grid_x, grid_y)
        
        # Reset cursor to default after releasing the mouse
        self.grid_canvas.config(cursor="")

    def _on_mouse_move(self, event):
        current_tab = GraphicConstants().current_tab
        cursor_set = False
        for widget in self.tabs[current_tab].values():
            if widget.is_pressed(event.x, event.y):
                edge_bools = widget.is_pressed_on_edge(event.x, event.y)
                if True in edge_bools:
                    cursor_set = True
                    on_left_edge, on_right_edge, on_top_edge, on_bottom_edge = edge_bools
                    if on_left_edge and on_top_edge:  # Top-left corner
                        self.grid_canvas.config(cursor="size_nw_se")
                    elif on_right_edge and on_bottom_edge:  # Bottom-right corner
                        self.grid_canvas.config(cursor="size_nw_se")
                    elif on_right_edge and on_top_edge:  # Top-right corner
                        self.grid_canvas.config(cursor="size_ne_sw")
                    elif on_left_edge and on_bottom_edge:  # Bottom-left corner
                        self.grid_canvas.config(cursor="size_ne_sw")
                    elif on_left_edge or on_right_edge:  # Left or right edge
                        self.grid_canvas.config(cursor="sb_h_double_arrow")
                    elif on_top_edge or on_bottom_edge:  # Top or bottom edge
                        self.grid_canvas.config(cursor="sb_v_double_arrow")
                    break
        if not cursor_set:
            self.grid_canvas.config(cursor="")
            
    # Check if a rectangle of rect_width x rect_height can be placed at x, y
    def can_place_rectangle(self, x, y, rect_width, rect_height, widget_tab):
        
        if x + rect_width > self.grid_width or y + rect_height > self.grid_height:
            return False
        for i in range(y, y + rect_height):
            for j in range(x, x + rect_width):
                if self.grids[widget_tab][i][j] != 0:
                    return False
        return True

    # "Place" a rectangle of rect_width x rect_height at x, y (set all values in the rectangle to 1 not actually place anything)
    def place_rectangle(self, x, y, rect_width, rect_height, widget_tab):
        
        for i in range(y, y + rect_height):
            for j in range(x, x + rect_width):
                self.grids[widget_tab][i][j] = 1
    
    # Remove a rectangle of rect_width x rect_height at x, y (set all values in the rectangle to 0)
    def remove_rectangle(self, x, y, rect_width, rect_height, widget_tab):
        
        for i in range(y, y + rect_height):
            for j in range(x, x + rect_width):
                self.grids[widget_tab][i][j] = 0

    # Find the next available space to place a rectangle of rect_width x rect_height
    def find_next_available_space(self, rect_width, rect_height, widget_tab):        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.can_place_rectangle(x, y, rect_width, rect_height, widget_tab):
                    return (x, y) # Tuple of the x and y coordinates
        return (-1, -1)
    
    def convert_pixel_to_grid(self, x, y):
        return x // GraphicConstants().grid_dim, y // GraphicConstants().grid_dim
    
    def debug_grid(self):
        tag = "grid"
        self.grid_canvas.delete(tag)

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                color = GraphicConstants().red if self.grids[GraphicConstants().current_tab][y][x] else GraphicConstants().dark_green
                
                self.grid_canvas.create_text(
                    x * GraphicConstants().grid_dim + GraphicConstants().grid_dim // 2,
                    y * GraphicConstants().grid_dim + GraphicConstants().grid_dim // 2,
                    fill=color,
                    text=str(self.grids[GraphicConstants().current_tab][y][x]),
                    tags=tag
                )
        
        self.grid_canvas.tag_raise(tag)

