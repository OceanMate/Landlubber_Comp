from dashboard.GraphicConstants import GraphicConstants
import tkinter.font as tkfont

from dashboard.graphics.GridGraphics import GridGraphics


class Widget():
    def __init__(self, canvas, label):
        # Important widget variables
        self.widget_label_height = 20
        self.widget_offset = 3
        
        # Set the font for the widget
        self.font = tkfont.Font(family=GraphicConstants().font, size=12)
        
        self.label = label
        # Set the canvas the widget is on
        self.canvas = canvas
        
        # Need to remove special characters from the label for use in code
        tag_label = ''.join(e for e in self.label if e.isalnum())
        # Extremely important for the widget, used to identify the all the components of a widget on the canvas
        self.tag = "widget_tag_" + str(tag_label)
        
        # grabs the grid manager for use in placing and removing widgets
        self.gridmanager = GridGraphics()

    # Set the location of the widget on the canvas given the grid coordinates
    def _set_location(self, grid_x, grid_y):
        self.x = grid_x * GraphicConstants().grid_dim
        self.y = grid_y * GraphicConstants().grid_dim
        self.grid_x = grid_x
        self.grid_y = grid_y
    
    # Set the dimensions of the widget given the grid dimensions
    def _set_dimensions(self, grid_width, grid_height):
        self.width = grid_width * GraphicConstants().grid_dim
        self.height = grid_height * GraphicConstants().grid_dim
        self.grid_width = grid_width
        self.grid_height = grid_height
    
    # Create the frame of the widget
    def _create_widget_frame(self):        
        # Create the widget frame rectangle
        self.canvas.create_rectangle(
            self.x + self.widget_offset, self.y + self.widget_offset, 
            self.x + self.width - self.widget_offset, self.y + self.height - self.widget_offset,
            fill=GraphicConstants().white,
            outline=GraphicConstants().blue,
            tags=self.tag
        )
        
        # Create the widget label rectangle
        self.canvas.create_rectangle(
            self.x + self.widget_offset, self.y + self.widget_offset, 
            self.x + self.width - self.widget_offset, self.y + self.widget_label_height + self.widget_offset,
            fill=GraphicConstants().blue,
            outline="",
            tags=self.tag
        )
        
        # find the center of the widget for the label text
        text_x = self.x + (self.width) / 2
        text_y = self.y + self.widget_label_height / 2 + self.widget_offset
        
        display_label = self.resize_text(self.label)
        
        # Create the widget label text
        self.g_label_display = self.canvas.create_text(
            text_x, text_y,
            text=display_label,
            fill=GraphicConstants().white,
            anchor="center",
            font=self.font,
            tags=self.tag
        )
        
    # Resize the text to fit in the widget
    def resize_text(self, text):
        # Calculate the width of the text
        text_width = self.font.measure(text)
        
        # If the text is too long, cut off the text with "..."
        if (text_width > self.width - 2 * self.widget_offset - 5):
            max_width = self.width - 2 * self.widget_offset - 5
            while (self.font.measure(text + "...") > max_width and len(text) > 0):
                text = text[:-1]
            text += "..."
        
        return text
    
    # Move the widget to a new grid location
    def move_widget(self, grid_x, grid_y): 
        opperating_tab = GraphicConstants().current_tab
        
        # Remove the widget from the grid
        self.gridmanager.remove_rectangle(self.grid_x, self.grid_y, self.grid_width, self.grid_height, opperating_tab)
        
        # Calculate the change in x and y
        current_x = self.x
        current_y = self.y
        
        # Moves all items in the tag by the delta x and delta y
        if self.gridmanager.can_place_rectangle(grid_x, grid_y, self.grid_width, self.grid_height, opperating_tab):
            self._set_location(grid_x, grid_y)
        else:
            new_grid_loc = self.gridmanager.find_next_available_space(self.grid_width, self.grid_height, opperating_tab)
            self._set_location(new_grid_loc[0], new_grid_loc[1])
        
        # Calculate the change in x and y
        delta_x = self.x - current_x
        delta_y = self.y - current_y
        
        # Move the widget to the new location
        self.canvas.move(self.tag, delta_x, delta_y)
        
        # Place the widget back on the grid
        self.gridmanager.place_rectangle(self.grid_x, self.grid_y, self.grid_width, self.grid_height, opperating_tab)

    # Check if the widget is pressed
    def is_point_inside(self, x, y):
        # Check if the x and y coordinates are within the widget
        in_x = self.x <= x <= self.x + self.width
        in_y = self.y <= y <= self.y + self.height
        return in_x and in_y
    
    # Check if the widget is pressed on the edge
    def is_point_near_edge(self, x, y):
        edge_threshold = 6  # Define how close to the edge the press should be to count as on the edge
        
        on_left_edge = self.x <= x <= self.x + edge_threshold
        on_right_edge = self.x + self.width - edge_threshold <= x <= self.x + self.width
        on_top_edge = self.y <= y <= self.y + edge_threshold
        on_bottom_edge = self.y + self.height - edge_threshold <= y <= self.y + self.height
        
        # Return a tuple of all the edge checks
        return (on_left_edge, on_right_edge, on_top_edge, on_bottom_edge)
    
    # Recreate the widget to reflect changes in variables
    def recreate_widget(self):
        self.canvas.delete(self.tag)
        self._create_widget_frame()
    
    # Resize the widget based on the edges being resized
    def resize_widget(self, grid_x, grid_y, edge_bools):
        operating_tab = GraphicConstants().current_tab
        
        # Determine which edges are being resized
        on_left_edge, on_right_edge, on_top_edge, on_bottom_edge = edge_bools
        
        # Remove the current widget from the grid
        self.gridmanager.remove_rectangle(self.grid_x, self.grid_y, self.grid_width, self.grid_height, operating_tab)
        
        # Adjust the position and dimensions based on the edges being resized
        if on_left_edge:
            new_width = self.grid_width + (self.grid_x - grid_x)
            new_x = grid_x
        elif on_right_edge:
            new_width = grid_x - self.grid_x + 1
            new_x = self.grid_x
        else:
            new_width = self.grid_width
            new_x = self.grid_x
        
        if on_top_edge:
            new_height = self.grid_height + (self.grid_y - grid_y)
            new_y = grid_y
        elif on_bottom_edge:
            new_height = grid_y - self.grid_y + 1
            new_y = self.grid_y
        else:
            new_height = self.grid_height
            new_y = self.grid_y
        
        # Ensure the new dimensions are valid
        if new_width <= 0 or new_height <= 0 or not self.gridmanager.can_place_rectangle(new_x, new_y, new_width, new_height, operating_tab):
            # Revert to original dimensions and location if invalid
            new_width = self.grid_width
            new_height = self.grid_height
            new_x = self.grid_x
            new_y = self.grid_y
        
        # Set the new location and dimensions
        self._set_location(new_x, new_y)
        self._set_dimensions(new_width, new_height)
        
        # Place the resized widget back on the grid
        self.gridmanager.place_rectangle(self.grid_x, self.grid_y, self.grid_width, self.grid_height, operating_tab)
        
        # Recreate the widget to reflect the new size
        self.recreate_widget()
            
    
    def hide(self):
        self.canvas.itemconfigure(self.tag, state='hidden')

    def show(self):
        self.canvas.tag_raise(self.tag)
        self.canvas.itemconfigure(self.tag, state='normal')
