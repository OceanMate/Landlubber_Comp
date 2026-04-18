from jigboard.Jigboard import Jigboard
from structure.commands.Command import Command
from Robot.Subsystems.Cameras import Cameras
import time

class SaveImageCmd(Command):
    def __init__(self, cameras : Cameras, save_button, switch_camera_button, crab_button):
        super().__init__()
        self.save_button = save_button
        self.switch_camera_button = switch_camera_button
        self.crab_button = crab_button

        self.cameras = cameras
        self.add_requirement(cameras)
        self.wait_time = 0.5  # Time to display "Image Saved!" message
        self.current_camera = 0
        self.get_image = False
        
    def initialize(self):
        self.save_time = time.time() - self.wait_time*2  # Initialize to allow immediate saving
        print("SaveImageCmd initialized")
    
    def execute(self):
        Jigboard().put_string("Current Cam", f"Cam: {self.current_camera}")
        # Show "image saved!" message on the camera widget when save is successful
        if self.save_time - time.time() < self.wait_time and self.current_camera < len(Jigboard().camera_widgets):
            Jigboard().put_string("Current Cam", f"Image Saved!")
        
        if self.save_button():
            self.get_image = True
        
        if self.crab_button():
            self.cameras.find_crabs_in_image(self.current_camera)
        
        if self.get_image:
            save_successful = self.cameras.save_image(self.current_camera)
            self.get_image = not save_successful
            self.save_time = time.time()
            
        
        if self.switch_camera_button():
            if self.cameras.num_cameras > 0:
                self.current_camera = (self.current_camera + 1) % self.cameras.num_cameras
    
    def end(self, interrupted):
        pass
    
    def is_finished(self):
        return False