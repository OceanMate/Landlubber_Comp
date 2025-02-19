from jigboard.widgets.Widget import Widget
from jigboard.GraphicConstants import GraphicConstants
from PIL import Image, ImageTk
from transmission.CameraComs import CameraComs


# creates a widget that displays a given string
class CameraWidget(Widget):
    def __init__(self, canvas, label, camera_id):
        super().__init__(canvas, label)
        
        # Set the default dimensions of the widget
        grid_width, grid_height = self.get_default_dimensions()
        self._set_dimensions(grid_width, grid_height)
        self.camera_id = camera_id
    
    # Get the default dimensions of the widget, approximately the same size no matter the grid dimensions
    def get_default_dimensions(self):
        # Default dimensions of the widget in pixels
        px_height = 300
        px_width = 350
        
        # Convert the default dimensions to grid dimensions
        grid_width = px_width // GraphicConstants().grid_dim
        if px_width % GraphicConstants().grid_dim != 0:
            grid_width += 1
        
        grid_height = px_height // GraphicConstants().grid_dim
        if px_height % GraphicConstants().grid_dim != 0:
            grid_height += 1
        
        return grid_width, grid_height
    
    # Create the string widget on the canvas
    def create_camera_widget(self, grid_x, grid_y):                
        # Set the location and dimensions of the widget
        self._set_location(grid_x, grid_y)
        
        # Create the frame of the widget
        self._create_widget_frame()
        self._make_camera_widget()
    
    def _make_camera_widget(self):
        image_x = self.x + self.width / 2
        image_y = self.y + self.widget_label_height + (self.height - self.widget_label_height) / 2
        
        self.image_label = self.canvas.create_image(image_x, image_y, anchor='center', tags=self.tag)
        
        self.max_width = self.width - self.widget_offset * 2
        self.max_height = self.height - self.widget_offset * 2 - self.widget_label_height
        
        error_message = "Camera image not found"
        display_message = self.resize_text(error_message)
        
        # Create the error message text
        self.error_text = self.canvas.create_text(
            image_x, image_y,
            text=display_message,
            fill="red",
            anchor="center",
            font=self.font,
            tags=self.tag
        )
        
        self.canvas.itemconfig(self.error_text, state='hidden')
        
    def update_image(self):
        img = CameraComs().get_camera_image(self.camera_id)
        
        # If the image is not found, display the error message
        if img is None:
            self.canvas.itemconfig(self.error_text, state='normal')
            return
        self.canvas.itemconfig(self.error_text, state='hidden')
        
        # Resize the image to fit in the widget
        if self.max_width and self.max_height:
            img.thumbnail((self.max_width, self.max_height), Image.Resampling.LANCZOS) # type: ignore
        
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.itemconfig(self.image_label, image=imgtk)
        
    # Override the recreate_widget method to recreate the string widget
    def recreate_widget(self):
        super().recreate_widget()
        self._make_camera_widget()