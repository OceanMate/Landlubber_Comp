from dashboard.GraphicConstants import GraphicConstants

class Widget():
    def __init__(self, canvas, label):
        self.canvas = canvas
        self.label = label
        
        # Important widget dimensions
        self.widget_label_height = 20
        self.widget_offset = 3
    
    def _set_location(self, grid_x, grid_y):
        self.x = grid_x * GraphicConstants().grid_dim
        self.y = grid_y * GraphicConstants().grid_dim + GraphicConstants().tab_bar_height
    
    def _set_dimensions(self, grid_width, grid_height):
        self.width = grid_width * GraphicConstants().grid_dim
        self.height = grid_height * GraphicConstants().grid_dim
    
    def _create_widget_frame(self):
        self.g_background = self.canvas.create_rectangle(
            self.x + self.widget_offset, self.y + self.widget_offset, 
            self.x + self.width - self.widget_offset, self.y + self.height - self.widget_offset,
            fill=GraphicConstants().white,
            outline=GraphicConstants().blue
        )
        
        self.g_label_rect = self.canvas.create_rectangle(
            self.x + self.widget_offset, self.y + self.widget_offset, 
            self.x + self.width - self.widget_offset, self.y + self.widget_label_height + self.widget_offset,
            fill=GraphicConstants().blue,
            outline=""
        )
        
        text_x = self.x + (self.width) / 2
        text_y = self.y + self.widget_label_height / 2 + self.widget_offset
        
        self.g_label_display = self.canvas.create_text(
            text_x, text_y,
            text=self.label,
            fill=GraphicConstants().white,
            anchor="center",
            font=("Arial", 12)
        )
    
    def move_widget(self, grid_x, grid_y):  
        self._set_location(grid_x, grid_y)
              
        self.canvas.move(self.g_background, self.x + self.widget_offset - self.canvas.coords(self.g_background)[0], 
                         self.y + self.widget_offset - self.canvas.coords(self.g_background)[1])
        self.canvas.move(self.g_label_rect, self.x + self.widget_offset- self.canvas.coords(self.g_label_rect)[0], 
                         self.y + self.widget_offset - self.canvas.coords(self.g_label_rect)[1])
        
        text_x = self.x + (self.width) / 2
        text_y = self.y + self.widget_label_height / 2 + self.widget_offset
        self.canvas.move(self.g_label_display, text_x - self.canvas.coords(self.g_label_display)[0], 
                         text_y - self.canvas.coords(self.g_label_display)[1])