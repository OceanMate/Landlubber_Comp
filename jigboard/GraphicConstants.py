from pathlib import Path

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
        self.bottom_bar_height = 70
        self.network_data_width = 300
        
        # Colors
        self.white = "#FFFFFF"
        self.light_grey = "#f0f0f0"
        self.dark_grey = "#d0d0d0"
        self.black = "#000000"
        self.blue = "#2caad3"
        self.middle_blue = "#d0f0f8"
        self.light_blue = "#e0f7fa"
        self.light_green = "#90EE90"
        self.green = "#008000"
        self.dark_green = "#006400"
        self.light_red = "#FFB6C1"
        self.red = "#FF0000"
        self.orange = "#FFA500"
        
        # Font
        self.font = "Cascadia Code"
        self.bottom_bar_font = "Ocr A Extended"
        
        # Tabs
        self.default_tab = "Jigboard"
        # Technically not a constant, but it's easier to access it this way
        self.current_tab = "Jigboard"

    
    # Get the path of an asset in the assets folder
    def get_asset_path(self, path: str) -> Path:
        return Path(__file__).parent / "assets" / path
