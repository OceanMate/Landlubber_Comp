class CommandRunner:
    _instance = None

    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.commands = []
        self.default_commands = []
        self.enabled = False
    
    def run_commands(self):
        
        return
    
    def add_command(self, command):
        self.commands.append(command)
    
    def add_default_command(self, command):
        self.default_commands.append(command)
        
    def turn_off(self):
        self.enabled = False
    
    def turn_on(self):
        self.enabled = True
