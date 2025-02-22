from jigboard.widgets.Widget import Widget
from jigboard.GraphicConstants import GraphicConstants   

# creates a widget that displays a given string
class BooleanWidget(Widget):
    def __init__(self, canvas, label, name, display_bool):
        super().__init__(canvas, label, name)
        
        self.display_bool = display_bool
        
        grid_width, grid_height = self.get_default_dimensions()
        self._set_dimensions(grid_width, grid_height)
    
    # Get the default dimensions of the widget, approximately the same size no matter the grid dimensions
    def get_default_dimensions(self):
        # Default dimensions of the widget in pixels
        px_height = 100
        px_width = 100
        
        # Convert the default dimensions to grid dimensions
        grid_width = px_width // GraphicConstants().grid_dim
        if px_width % GraphicConstants().grid_dim != 0:
            grid_width += 1
        
        grid_height = px_height // GraphicConstants().grid_dim
        if px_height % GraphicConstants().grid_dim != 0:
            grid_height += 1
        
        return grid_width, grid_height
    
    def create_bool_widget(self, grid_x, grid_y, display_bool):
        # Set the location and dimensions of the widget
        self._set_location(grid_x, grid_y)
        self.display_bool = display_bool
        
        # Create the frame of the widget
        self._create_widget_frame()
        self._make_bool_widget()
    
    # Create the string widget on the canvas
    def _make_bool_widget(self):
        bool_offset = 5
        offset = self.widget_offset + bool_offset
        
        # Create a rectangle under the label
        rect_color = GraphicConstants().dark_green if self.display_bool else GraphicConstants().red
        self.g_bool_rect = self.canvas.create_rectangle(
            self.x + offset, self.y + self.widget_label_height + offset, 
            self.x + self.width - offset, self.y + self.height - offset,
            fill=rect_color, outline=rect_color,
            tags=self.tag
        )
        
    def recreate_widget(self):
        super().recreate_widget()
        self._make_bool_widget()
            
    # Update the text of the widget
    def update_bool(self, display_bool):
        self.display_bool = display_bool
        rect_color = GraphicConstants().dark_green if display_bool else GraphicConstants().red
        self.canvas.itemconfig(self.g_bool_rect, fill=rect_color, outline=rect_color)
