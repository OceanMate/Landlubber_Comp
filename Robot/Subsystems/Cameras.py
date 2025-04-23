import os
import cv2
import random
from jigboard.Jigboard import Jigboard
from structure.Subsystem import Subsystem
from transmission.CameraComs import CameraComs

class Cameras(Subsystem):
    def __init__(self):
        super().__init__()
        
        self.camera_coms = CameraComs()
        self.num_cameras = self.camera_coms.camera_limit
        
        for i in range(self.num_cameras):
            Jigboard().put_camera("Camera {}".format(i), i)
        
        self.image_counter = 0  # Add an image counter

        
    def save_image(self, camera_index) -> bool:
        frame = self.camera_coms.get_camera_frame(camera_index, is_displaying=False)
        if frame is None:
            return False
        
        # Generate a random 6-digit integer
        random_number = random.randint(100000, 999999)
        
        # Save the frame as a PNG in the 'images' folder within the current repo
        images_folder = os.path.join(os.path.dirname(__file__), "..", "..", "images")
        os.makedirs(images_folder, exist_ok=True)
        file_path = os.path.join(images_folder, f"camera_{camera_index}_image_{self.image_counter}_{random_number}.png")
        cv2.imwrite(file_path, frame)
        print(f"Saved frame to {file_path}")
        self.image_counter += 1  # Increment the image counter
        return True
    
    def periodic(self):
        pass
