from structure.commands.Command import Command

class TemplateCommand(Command):
    def __init__(self):
        super().__init__()
        
    def initialize(self):
        pass
    
    def execute(self):
        pass
    
    def end(self, interrupted):
        pass
    
    def is_finished(self):
        return True