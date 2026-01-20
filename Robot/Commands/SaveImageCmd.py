from jigboard.Jigboard import Jigboard
from structure.commands.Command import Command
from Robot.Subsystems.Cameras import Cameras

class SaveImageCmd(Command):
    def __init__(self, cameras : Cameras, save_button, switch_camera_button):
        super().__init__()
        self.save_button = save_button
        self.switch_camera_button = switch_camera_button
        
        self.cameras = cameras
        self.current_camera = 0
        self.get_image = False
        
    def initalize(self):
        pass
    
    def execute(self):
        Jigboard().put_string("Current Cam", f"Cam: {self.current_camera}")
        
        if self.save_button():
            self.get_image = True
        
        if self.get_image:
            self.get_image = not self.cameras.save_image(self.current_camera)
        
        if self.switch_camera_button():
            if self.cameras.num_cameras > 0:
                self.current_camera = (self.current_camera + 1) % self.cameras.num_cameras
    
    def end(self, interrupted):
        pass
    
    def is_finished(self):
        return False