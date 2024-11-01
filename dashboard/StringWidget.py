
from dashboard.Widget import Widget
from dashboard.GraphicConstants import GraphicConstants


class StringWidget(Widget):
    def __init__(self, canvas, label):
        super().__init__(canvas, label)
    
    def get_default_dimensions(self):
        px_height = 100
        px_width = 250
                
        grid_width = px_width // GraphicConstants().grid_dim
        if px_width % GraphicConstants().grid_dim != 0:
            grid_width += 1
        
        grid_height = px_height // GraphicConstants().grid_dim
        if px_height % GraphicConstants().grid_dim != 0:
            grid_height += 1
        
        return grid_width, grid_height
    
    def create_string_widget(self, grid_x, grid_y, display_text):        
        grid_width, grid_height = self.get_default_dimensions()
        
        self._set_location(grid_x, grid_y)
        self._set_dimensions(grid_width, grid_height)
        self._create_widget_frame()
        
        text_x = self.x + (self.width) / 2
        text_y = self.y + self.widget_label_height + (self.height - self.widget_label_height) / 2
        
        self.g_display_text = self.canvas.create_text(
            text_x, 
            text_y,
            text=display_text,
            fill=GraphicConstants().black,
            anchor="center",
            font=("Arial", 12)
        )
        
        self.g_text_line = self.canvas.create_line(
            self.x + self.width * (1 / 16) + self.widget_offset, 
            text_y + 10,
            self.x + self.width * (15 / 16) - self.widget_offset, 
            text_y + 10,
            fill=GraphicConstants().light_grey,
            width=1
        )
    
    def update_text(self, display_text):
        self.canvas.itemconfig(self.g_display_text, text=display_text)
    
    def move_widget(self, grid_x, grid_y):
        self._set_location(grid_x, grid_y)
        
        text_x = self.x + (self.width) / 2
        text_y = self.y + self.widget_label_height + (self.height - self.widget_label_height) / 2
        
        self.canvas.move(self.g_display_text, text_x - self.canvas.coords(self.g_display_text)[0], 
                         text_y - self.canvas.coords(self.g_display_text)[1])
        
        self.canvas.move(self.g_text_line, self.x + self.widget_offset - self.canvas.coords(self.g_background)[0], 
                         self.y + self.widget_offset - self.canvas.coords(self.g_background)[1])
        
        super().move_widget(grid_x, grid_y)    