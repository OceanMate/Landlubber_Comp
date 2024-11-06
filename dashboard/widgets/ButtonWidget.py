from dashboard.widgets.Widget import Widget
from dashboard.GraphicConstants import GraphicConstants

class ButtonWidget(Widget):
    def __init__(self, canvas, label, command):
        super().__init__(canvas, label)
        self.command = command
        grid_width, grid_height = self.get_default_dimensions()
        self._set_dimensions(grid_width, grid_height)
        self.button_tag = "button" + self.tag

    # Get the default dimensions of the widget, approximately the same size no matter the grid dimensions
    def get_default_dimensions(self):
        # Default dimensions of the widget in pixels
        px_height = 50
        px_width = 100
        
        # Convert the default dimensions to grid dimensions
        grid_width = px_width // GraphicConstants().grid_dim
        if px_width % GraphicConstants().grid_dim != 0:
            grid_width += 1
        
        grid_height = px_height // GraphicConstants().grid_dim
        if px_height % GraphicConstants().grid_dim != 0:
            grid_height += 1
        
        return grid_width, grid_height

    # Create the button widget on the canvas
    def create_button_widget(self, grid_x, grid_y):
        # Set the location and dimensions of the widget
        self._set_location(grid_x, grid_y)
        
        # Create the frame of the widget
        self._create_widget_frame()
        
        # Create the button rectangle
        button_offset = 5
        offset = self.widget_offset + button_offset
        
        self.g_button_rect = self.canvas.create_rectangle(
            self.x + offset, self.y + self.widget_label_height + offset, 
            self.x + self.width - offset, self.y + self.height - offset,
            fill=GraphicConstants().light_grey, outline=GraphicConstants().light_grey,
            tags=(self.tag, self.button_tag)
        )
        
        # Create the button text
        text_x = self.x + self.width / 2
        text_y = self.y + (self.height + self.widget_label_height) / 2
        
        self.g_button_text = self.canvas.create_text(
            text_x, text_y,
            text=self.label,
            fill=GraphicConstants().blue,
            anchor="center",
            font=self.font,
            tags=(self.tag, self.button_tag)
        )
        
        # Bind the click event to the button
        self.canvas.tag_bind(self.button_tag, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.button_tag, "<ButtonRelease-1>", self.on_release)

    # Handle the button click event
    def on_click(self, event):
        self.canvas.itemconfig(self.g_button_rect, fill=GraphicConstants().dark_grey, outline=GraphicConstants().dark_grey)
        self.command()

    def on_release(self, event):
        self.canvas.itemconfig(self.g_button_rect, fill=GraphicConstants().light_grey, outline=GraphicConstants().light_grey)
    
    # Need to override the is_pressed method to account for the button
    def is_pressed(self, x, y):
        # Check if the x and y coordinates are within the widget but outside the button rectangle
        in_widget_x = self.x <= x <= self.x + self.width
        in_widget_y = self.y <= y <= self.y + self.height
        in_button_x = self.x + self.widget_offset + 5 <= x <= self.x + self.width - self.widget_offset - 5
        in_button_y = self.y + self.widget_label_height + self.widget_offset + 5 <= y <= self.y + self.height - self.widget_offset - 5
        
        return in_widget_x and in_widget_y and not (in_button_x and in_button_y)

    def recreate_widget(self):
        super().recreate_widget()
        self.create_button_widget(self.grid_x, self.grid_y)
            
    def resize_widget(self, grid_x, grid_y, edge_bools):        
        super().resize_widget(grid_x, grid_y, edge_bools)
        self.create_button_widget(self.grid_x, self.grid_y)
