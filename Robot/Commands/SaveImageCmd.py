import os
import cv2
import random  # Import random module
from jigboard.Jigboard import Jigboard
from structure.commands.Command import Command
from transmission.CameraComs import CameraComs

class SaveImageCmd(Command):
    def __init__(self, save_button, switch_camera_button):
        super().__init__()
        self.save_button = save_button
        self.switch_camera_button = switch_camera_button
        
        self.camera_coms = CameraComs()
        self.current_camera = 0
        self.get_image = False
        self.image_counter = 0  # Add an image counter
        
    def initalize(self):
        pass
    
    def execute(self):
        Jigboard().put_string("Current Image Camera", str(self.current_camera))
        
        if self.save_button():
            self.get_image = True
        
        if self.get_image:
            frame = self.camera_coms.get_camera_frame(self.current_camera, is_displaying=False)

            if frame is not None:
                # Generate a random 6-digit integer
                random_number = random.randint(100000, 999999)
                
                # Save the frame as a PNG in the 'images' folder within the current repo
                images_folder = os.path.join(os.path.dirname(__file__), "..", "..", "images")
                os.makedirs(images_folder, exist_ok=True)
                file_path = os.path.join(images_folder, f"camera_{self.current_camera}_image_{self.image_counter}_{random_number}.png")
                cv2.imwrite(file_path, frame)
                print(f"Saved frame to {file_path}")
                self.image_counter += 1  # Increment the image counter
                self.get_image = False
        
        if self.switch_camera_button():
            if self.camera_coms.num_cameras > 0:
                self.current_camera = (self.current_camera + 1) % self.camera_coms.num_cameras
            print(f"Switched to camera {self.current_camera}")
    
    def end(self, interrupted):
        pass
    
    def is_finished(self):
        return False