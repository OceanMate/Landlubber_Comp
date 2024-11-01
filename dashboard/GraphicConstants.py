
class GraphicConstants:
    _instance = None

    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._start()
        return cls._instance

    def _start(self):
        # Window dimensions
        self.window_height = 720
        self.window_width = 1280
        self.tab_bar_height = 30
        self.grid_dim = 30
        
        # Colors
        self.white = "#FFFFFF"
        self.light_grey = "#f0f0f0"
        self.dark_grey = "#d0d0d0"
        self.black = "#000000"
        self.blue = "#2caad3"
        self.middle_blue = "#d0f0f8"
        self.light_blue = "#e0f7fa"
        self.dark_green = "#006400"
        self.red = "#FF0000"
        