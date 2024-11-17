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
        # Store the tabs dictionary and window for use in the grid
        self.window = window
        self.tabs = tabs
        
        # Initialize the grids dictionary, there should be a grid for each tab
        self.grids = {}
        
    # Generate the grid on the canvas which the widgets will be placed on
    def generate_grid(self):
        # Calculate the height of the grid
        px_grid_height = GraphicConstants().window_height - GraphicConstants().tab_bar_height - GraphicConstants().bottom_bar_height
        
        self.grid_width, self.grid_height = self.convert_pixel_to_grid(GraphicConstants().window_width, px_grid_height)
        
        # Create the grid for the default tab
        self.create_new_tab_grid(GraphicConstants().default_tab)
        
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
        
        # Create the logo image on the canvas
        self.background_image = self.grid_canvas.create_image(logo_x, logo_y, image=self.rabbit_logo, anchor="nw")
        
        # Draw the grid on the canvas
        self.draw_grid()

        # Bind the left mouse click, release, and move events to the canvas
        self.grid_canvas.bind("<Button-1>", self._on_mouse_click)
        self.grid_canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
        self.grid_canvas.bind("<Motion>", self._on_mouse_move)
    
    def resize_grid(self):
        # Resize the canvas to fit the new window dimensions
        self.grid_canvas.config(width=GraphicConstants().window_width)
        px_grid_height = GraphicConstants().window_height - GraphicConstants().tab_bar_height - GraphicConstants().bottom_bar_height
        self.grid_canvas.config(height=px_grid_height)
        
        # Calculate the new grid dimensions
        self.grid_width, self.grid_height = self.convert_pixel_to_grid(GraphicConstants().window_width, px_grid_height)
        
        # Create the grid for each tab at new dimensions
        for tab in self.tabs:
            self.create_new_tab_grid(tab)
        
        # Calculate the position to place the image in the center of the grid
        logo_x = (GraphicConstants().window_width - self.rabbit_logo.width()) // 2
        logo_y = (px_grid_height - self.rabbit_logo.height()) // 2
        
        # Delete the previous image if it exists
        if self.background_image is not None:
            self.grid_canvas.delete(self.background_image)
        
        # Create the logo image on the canvas
        self.background_image = self.grid_canvas.create_image(logo_x, logo_y, image=self.rabbit_logo, anchor="nw")
        
        # Redraw the grid
        self.draw_grid()
    
    # Create a new tab grid for a new tab (should be run every time a new tab is created)
    def create_new_tab_grid(self, tab):
        self.grids[tab] = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    # Draw the grid on the canvas
    def draw_grid(self):
        # Calculate the height of the grid
        px_grid_height = GraphicConstants().window_height - GraphicConstants().tab_bar_height - GraphicConstants().bottom_bar_height
        
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
        # Starts a timer when the mouse is clicked to see how long the mouse is held down
        self.clk_start_time = time.time()
        
        self.widget_pressed = ""
        self.is_moving = False
        self.is_resizing = False
        current_tab = GraphicConstants().current_tab
        
        # Check if the mouse is on a widget
        for widget in self.tabs[current_tab].values():
            if(widget.is_point_inside(event.x, event.y)):
                # store the widget that is being pressed
                self.widget_pressed = widget.label
                
                # store the offset of the mouse from the top left corner of the widget
                self.x_offset = event.x - widget.x
                self.y_offset = event.y - widget.y
                
                # Check if the mouse is on the edge of the widget
                self.edge_bools = widget.is_point_near_edge(event.x, event.y)
                if True in self.edge_bools:
                    self.is_resizing = True
                else:
                    self.is_moving = True
    
    # TODO make move widget based of previous mouse location
    def _on_mouse_release(self, event):
        current_tab = GraphicConstants().current_tab

        # Check if the widget is being resized
        if self.is_resizing:
            grid_x, grid_y = self.convert_pixel_to_grid(event.x, event.y)
            
            # constrain the grid_x and grid_y to the grid
            grid_x = max(0, grid_x)
            grid_y = max(0, grid_y)
            grid_x = min(grid_x, self.grid_width)
            grid_y = min(grid_y, self.grid_height)
            
            self.tabs[GraphicConstants().current_tab][self.widget_pressed].resize_widget(grid_x, grid_y, self.edge_bools)
            
            self.is_resizing = False
            
            # Ends the function early if the widget is being resized (prevents the widget from also being moved) 
            return

        
        # Check if the widget is being moved
        # User needs to hold down the mouse for at least 0.2 seconds to move the widget
        if time.time() - self.clk_start_time > 0.2 and self.is_moving:
            grid_x, grid_y = self.convert_pixel_to_grid(event.x, event.y)
            
            # Adjust the grid_x and grid_y based on the offset of the first click on the widget
            grid_x = grid_x - self.x_offset // GraphicConstants().grid_dim
            grid_y = grid_y - self.y_offset // GraphicConstants().grid_dim
            
            # constrain the grid_x and grid_y to the grid
            grid_x = max(0, grid_x)
            grid_y = max(0, grid_y)
            grid_x = min(grid_x, self.grid_width - self.tabs[current_tab][self.widget_pressed].grid_width)
            grid_y = min(grid_y, self.grid_height - self.tabs[current_tab][self.widget_pressed].grid_height)
            
            self.tabs[GraphicConstants().current_tab][self.widget_pressed].move_widget(grid_x, grid_y)
            
            self.is_moving = False

    # Runs when the mouse is moved
    def _on_mouse_move(self, event):
        current_tab = GraphicConstants().current_tab
        cursor_set = False
        
        # Check if the mouse is on the edge of a widget, and set the cursor accordingly
        for widget in self.tabs[current_tab].values():
            # Check if the mouse is inside the widget
            if widget.is_point_inside(event.x, event.y):
                
                # sets up a list of booleans for each edge of the widget
                edge_bools = widget.is_point_near_edge(event.x, event.y)
                
                # If any of the edges are True, set the cursor to the appropriate cursor
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
        
        # Reset cursor to default if the mouse is not on the edge of a widget
        if not cursor_set:
            self.grid_canvas.config(cursor="")
        
        # make the widget follow the mouse if the widget is being moved
        if self.is_moving:
            self.tabs[current_tab][self.widget_pressed].move_widget_unrestricted(event.x - self.x_offset, event.y - self.y_offset)
            # bring the widget to the front of the canvas
            self.tabs[current_tab][self.widget_pressed].show()
            
    # Check if a rectangle of rect_width x rect_height can be placed at x, y
    def can_place_rectangle(self, x, y, rect_width, rect_height, widget_tab):
        # Check if the rectangle is larger than the grid
        if x + rect_width > self.grid_width or y + rect_height > self.grid_height:
            return False
        
        # Check if the rectangle overlaps with any other widgets
        for i in range(y, y + rect_height):
            for j in range(x, x + rect_width):
                # Check if the rectangle is out of bounds or overlaps with another widget
                if i < 0 or j < 0 or i >= self.grid_height or j >= self.grid_width or self.grids[widget_tab][i][j] != 0:
                    return False
        return True

    # "Place" a rectangle of rect_width x rect_height at x, y (set all values in the rectangle to 1 not actually place anything)
    def place_rectangle(self, x, y, rect_width, rect_height, widget_tab):
        for i in range(y, y + rect_height):
            for j in range(x, x + rect_width):
                # Check if the rectangle is in bounds
                if 0 <= i < self.grid_height and 0 <= j < self.grid_width:
                    self.grids[widget_tab][i][j] = 1
    
    # Remove a rectangle of rect_width x rect_height at x, y (set all values in the rectangle to 0)
    def remove_rectangle(self, x, y, rect_width, rect_height, widget_tab):
        for i in range(y, y + rect_height):
            for j in range(x, x + rect_width):
                # Check if the rectangle is in bounds
                if 0 <= i < self.grid_height and 0 <= j < self.grid_width:
                    self.grids[widget_tab][i][j] = 0

    # Find the next available space to place a rectangle of rect_width x rect_height
    def find_next_available_space(self, rect_width, rect_height, widget_tab):        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.can_place_rectangle(x, y, rect_width, rect_height, widget_tab):
                    return (x, y) # Tuple of the x and y coordinates
        return (-1 - rect_width, -1 - rect_height) # Move the widget off the screen if there is no available space
    
    # Check if the rectangle is out of bounds
    def is_out_of_bounds(self, x, y, rect_width, rect_height):
        return x < 0 or y < 0 or x + rect_width > self.grid_width or y + rect_height > self.grid_height
    
    # Convert pixel coordinates to grid coordinates
    def convert_pixel_to_grid(self, x, y):
        return x // GraphicConstants().grid_dim, y // GraphicConstants().grid_dim
    
    # Debug the grid by displaying the values of the grid on the canvas
    def debug_grid(self):
        tag = "grid"
        self.grid_canvas.delete(tag)

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                # Set the color of the text based on the value of the grid (red for 1, green for 0)
                color = GraphicConstants().red if self.grids[GraphicConstants().current_tab][y][x] else GraphicConstants().dark_green
                
                self.grid_canvas.create_text(
                    x * GraphicConstants().grid_dim + GraphicConstants().grid_dim // 2,
                    y * GraphicConstants().grid_dim + GraphicConstants().grid_dim // 2,
                    fill=color,
                    text=str(self.grids[GraphicConstants().current_tab][y][x]),
                    tags=tag
                )
        
        # Raise the grid to the top of the canvas so it isn't behind the widgets
        self.grid_canvas.tag_raise(tag)

