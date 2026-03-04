from structure.commands.Command import Command

class InstantCommand(Command):
    def __init__(self, function):
        super().__init__()
        self.function = function
    
    def initialize(self):
        self.function()
    
    def execute(self):
        return
    
    def end(self, interrupted):
        return
    
    def is_finished(self):
        return True