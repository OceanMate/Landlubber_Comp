from dashboard.GraphicConstants import GraphicConstants

class Widget():
    def __init__(self, canvas, label):
        # Important widget dimensions
        self.widget_label_height = 20
        self.widget_offset = 3
        
        self.label = label
        
        self.canvas = canvas
        
        # Need to remove special characters from the label for use in code
        tag_label = ''.join(e for e in self.label if e.isalnum())
        # Extremely important for the widget, used to identify the all the components of a widget on the canvas
        self.tag = "widget_label" + str(tag_label)

    # Set the location of the widget on the canvas given the grid coordinates
    def _set_location(self, grid_x, grid_y):
        self.x = grid_x * GraphicConstants().grid_dim
        self.y = grid_y * GraphicConstants().grid_dim
    
    # Set the dimensions of the widget given the grid dimensions
    def _set_dimensions(self, grid_width, grid_height):
        self.width = grid_width * GraphicConstants().grid_dim
        self.height = grid_height * GraphicConstants().grid_dim
    
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
        
        # Create the widget label text
        self.g_label_display = self.canvas.create_text(
            text_x, text_y,
            text=self.label,
            fill=GraphicConstants().white,
            anchor="center",
            font=("Arial", 12),
            tags=self.tag
        )
    
    # Move the widget to a new grid location
    def move_widget(self, grid_x, grid_y): 
        # Calculate the change in x and y
        current_x = self.x
        current_y = self.y
        
        self._set_location(grid_x, grid_y)
        
        delta_x = self.x - current_x
        delta_y = self.y - current_y
        
        # Moves all items in the tag by the delta x and delta y
        self.canvas.move(self.tag, delta_x, delta_y)