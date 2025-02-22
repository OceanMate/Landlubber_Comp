import cv2
import time
from jigboard.widgets.Widget import Widget
from jigboard.GraphicConstants import GraphicConstants
from PIL import Image, ImageTk
from transmission.CameraComs import CameraComs


# creates a widget that displays a given string
class CameraWidget(Widget):
    def __init__(self, canvas, label, name, camera_id):
        super().__init__(canvas, label, name)
        
        # Set the default dimensions of the widget
        grid_width, grid_height = self.get_default_dimensions()
        self._set_dimensions(grid_width, grid_height)
        self.camera_id = camera_id
        
        self.time_since_update = time.time()
    
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
        self.image_label_obj = None  # Initialize the image label object
        
        self.max_width = int(self.width - self.widget_offset * 2)
        self.max_height = int(self.height - self.widget_offset * 2 - self.widget_label_height)
        
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
        frame = CameraComs().get_camera_frame(self.camera_id)
        
        # If the image is not found, display the error message
        if frame is None:
            if abs(self.time_since_update - time.time()) > 3:
                self.canvas.itemconfig(self.error_text, state='normal')
            return
        
        # Reset the time since update if we receive a valid frame
        self.time_since_update = time.time()
        self.canvas.itemconfig(self.error_text, state='hidden')
        
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Resize the image to fit in the widget          
        img = img.resize((self.max_width, self.max_height), Image.Resampling.LANCZOS)
        imgtk = ImageTk.PhotoImage(img)
        self.image_label_obj = imgtk  # Keep a reference to avoid garbage collection
        self.canvas.itemconfig(self.image_label, image=self.image_label_obj)

    # Override the recreate_widget method to recreate the string widget
    def recreate_widget(self):
        super().recreate_widget()
        self._make_camera_widget()