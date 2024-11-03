
from dashboard.widgets.Widget import Widget
from dashboard.GraphicConstants import GraphicConstants

# creates a widget that displays a given string
class StringWidget(Widget):
    def __init__(self, canvas, label):

        super().__init__(canvas, label)
    
    # Get the default dimensions of the widget, approximately the same size no matter the grid dimensions
    def get_default_dimensions(self):
        # Default dimensions of the widget in pixels
        px_height = 100
        px_width = 250
        
        # Convert the default dimensions to grid dimensions
        grid_width = px_width // GraphicConstants().grid_dim
        if px_width % GraphicConstants().grid_dim != 0:
            grid_width += 1
        
        grid_height = px_height // GraphicConstants().grid_dim
        if px_height % GraphicConstants().grid_dim != 0:
            grid_height += 1
        
        return grid_width, grid_height
    
    # Create the string widget on the canvas
    def create_string_widget(self, grid_x, grid_y, display_text):        
        grid_width, grid_height = self.get_default_dimensions()
        
        # Set the location and dimensions of the widget
        self._set_location(grid_x, grid_y)
        self._set_dimensions(grid_width, grid_height)
        
        # Create the frame of the widget
        self._create_widget_frame()
        
        # find the center of the widget for the text
        text_x = self.x + (self.width) / 2
        text_y = self.y + self.widget_label_height + (self.height - self.widget_label_height) / 2
        
        # Resize the text to fit in the widget
        display_text = self.resize_text(display_text)
        
        # Create the display text of the widget, stores the graphic object for use in updating the text
        self.g_display_text = self.canvas.create_text(
            text_x, 
            text_y,
            text=display_text,
            fill=GraphicConstants().black,
            anchor="center",
            font=self.font,
            tags=self.tag
        )
        
        # Create the line under the text for added pazazz
        self.g_text_line = self.canvas.create_line(
            self.x + self.width * (1 / 16) + self.widget_offset, 
            text_y + 10,
            self.x + self.width * (15 / 16) - self.widget_offset, 
            text_y + 10,
            fill=GraphicConstants().light_grey,
            width=1,
            tags=self.tag
        )
    
    def recreate_widget(self):
        p_text = self.canvas.itemcget(self.g_display_text, "text")
        super().recreate_widget()
        self.create_string_widget(self.grid_x, self.grid_y, p_text)
            
    # Update the text of the widget
    def update_text(self, display_text):
        display_text = self.resize_text(display_text)
        self.canvas.itemconfig(self.g_display_text, text=display_text)
        
    
    