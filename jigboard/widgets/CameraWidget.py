import cv2
import time
from jigboard.widgets.Widget import Widget
from jigboard.GraphicConstants import GraphicConstants
from PIL import Image, ImageTk
from transmission.CameraComs import CameraComs
from Debug import Debug


# creates a widget that displays a given string
class CameraWidget(Widget):
    def __init__(self, canvas, label, name, camera_id):
        super().__init__(canvas, label, name)
        
        # Set the default dimensions of the widget
        grid_width, grid_height = self.get_default_dimensions()
        self._set_dimensions(grid_width, grid_height)
        self.camera_id = camera_id
        
        self.time_since_update = time.time()
        self.camera_coms = CameraComs()  # Reuse the CameraComs instance
        self.last_frame_time = None  # Initialize for FPS calculation
        self.fps_text = None  # Initialize FPS text object
    
    # Get the default dimensions of the widget, approximately the same size no matter the grid dimensions
    def get_default_dimensions(self):
        # Default dimensions of the widget in pixels
        px_height = 240 + self.widget_label_height
        px_width = 320
        
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
        
        self.fps_text = self.canvas.create_text(
            self.x + self.width - 10, self.y + 5,  # Position at the top-right corner
            text="FPS: 0",
            fill="green",
            anchor="ne",
            font=self.font,
            tags=self.tag
        )
        if not Debug.displayCameraFPS:
            self.canvas.itemconfig(self.fps_text, state='hidden')
        
    def update_image(self):
        if self.camera_coms.is_frame_displayed(self.camera_id):
            # If the frame is already displayed, skip updating
            return
        
        frame = self.camera_coms.get_camera_frame(self.camera_id)  # Reuse the instance
        
        # If the image is not found, display the error message
        if frame is None:
            if abs(time.time() - self.time_since_update) > 3:  # Simplify time comparison
                self.canvas.itemconfig(self.error_text, state='normal')
            return
        
        # Reset the time since update if we receive a valid frame
        self.time_since_update = time.time()
        self.canvas.itemconfig(self.error_text, state='hidden')
        
        # Convert and resize the frame efficiently
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img = img.resize((self.max_width, self.max_height), Image.Resampling.LANCZOS)
        
        # Update the image label
        imgtk = ImageTk.PhotoImage(img)
        self.image_label_obj = imgtk  # Keep a reference to avoid garbage collection
        self.canvas.itemconfig(self.image_label, image=self.image_label_obj)

        # Calculate and display FPS
        current_time = time.time()
        if self.last_frame_time is not None and Debug.displayCameraFPS:
            fps = 1 / (current_time - self.last_frame_time)
            self.canvas.itemconfig(self.fps_text, text=f"FPS: {fps:.2f}") # type: ignore
        self.last_frame_time = current_time

    # Override the recreate_widget method to recreate the string widget
    def recreate_widget(self):
        super().recreate_widget()
        self._make_camera_widget()