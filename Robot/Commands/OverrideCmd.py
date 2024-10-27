from structure.commands.Command import Command

class OverrideCmd(Command):
    def __init__(self, linear_motors):
        super().__init__()
        super().add_requirement(linear_motors)
        
    def initalize(self):
        print("Overriding")
    
    def execute(self):
        pass
    
    def end(self, interrupted):
        pass
    
    def is_finished(self):
        return True