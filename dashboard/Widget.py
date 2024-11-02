from cProfile import label
from hmac import new
from os import remove
from dashboard.GraphicConstants import GraphicConstants
import tkinter.font as tkfont

from dashboard.GridManager import GridManager


class Widget():
    def __init__(self, canvas, label):
        # Important widget variables
        self.widget_label_height = 20
        self.widget_offset = 3
        self.font = tkfont.Font(family="Arial", size=12)
        
        self.label = label
        
        self.canvas = canvas
        
        # Need to remove special characters from the label for use in code
        tag_label = ''.join(e for e in self.label if e.isalnum())
        # Extremely important for the widget, used to identify the all the components of a widget on the canvas
        self.tag = "widget_label" + str(tag_label)
        
        self.gridmanager = GridManager()

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
            font=("Arial", 12),
            tags=self.tag
        )
        
    # Resize the text to fit in the widget
    def resize_text(self, text):
        # Calculate the width of the text
        text_width = self.font.measure(text)
        
        if (text_width > self.width - 2 * self.widget_offset - 5):
            # If the text is too long, cut off the text with "..."
            max_width = self.width - 2 * self.widget_offset - 5
            while (self.font.measure(text + "...") > max_width and len(text) > 0):
                text = text[:-1]
            text += "..."
        
        return text
    
    # Move the widget to a new grid location
    def move_widget(self, grid_x, grid_y): 
        self.gridmanager.remove_rectangle(self.grid_x, self.grid_y, self.grid_width, self.grid_height)
        
        # Calculate the change in x and y
        current_x = self.x
        current_y = self.y
        
        # Moves all items in the tag by the delta x and delta y
        if(self.gridmanager.can_place_rectangle(grid_x, grid_y, self.grid_width, self.grid_height)):
            self._set_location(grid_x, grid_y)
        else:
            new_grid_loc = self.gridmanager.find_next_available_space(self.grid_width, self.grid_height)
            self._set_location(new_grid_loc[0], new_grid_loc[1])
        
        delta_x = self.x - current_x
        delta_y = self.y - current_y
        
        self.canvas.move(self.tag, delta_x, delta_y)
        
        self.gridmanager.place_rectangle(self.grid_x, self.grid_y, self.grid_width, self.grid_height)
        
    # Check if the widget is pressed
    def am_i_pressed(self, x, y):
        # Check if the x and y coordinates are within the widget
        in_x = self.x <= x <= self.x + self.width
        in_y = self.y <= y <= self.y + self.height
        return in_x and in_y
    
    # Check if the widget is pressed on the edge
    def am_i_pressed_on_edge(self, x, y):
        edge_threshold = 5  # Define how close to the edge the press should be to count as on the edge
        on_left_edge = self.x <= x <= self.x + edge_threshold
        on_right_edge = self.x + self.width - edge_threshold <= x <= self.x + self.width
        on_top_edge = self.y <= y <= self.y + edge_threshold
        on_bottom_edge = self.y + self.height - edge_threshold <= y <= self.y + self.height
        
        return on_left_edge or on_right_edge or on_top_edge or on_bottom_edge
    
    def recreate_widget(self):
        self.canvas.delete(self.tag)
        self._create_widget_frame()
    
    def resize_widget(self, grid_width, grid_height):
        if self.gridmanager.can_place_rectangle(self.grid_x, self.grid_y, grid_width, grid_height):
            self.gridmanager.remove_rectangle(self.grid_x, self.grid_y, self.grid_width, self.grid_height)
            
            print("Resizing widget to: " + str(grid_width) + " x " + str(grid_height))
            
            # Set the new dimensions
            self._set_dimensions(grid_width, grid_height)
            
            # Move the widget to the new location
            self.move_widget(self.grid_x, self.grid_y)
            
            # Delete the old widget frame
            self.canvas.delete(self.tag)
            
            # Create the new widget frame
            self._create_widget_frame()
            
            self.gridmanager.place_rectangle(self.grid_x, self.grid_y, self.grid_width, self.grid_height)
