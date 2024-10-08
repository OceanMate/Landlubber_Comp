from structure.Command import Command

def TemplateCommand(Command):
    def initalize(self):
        pass
    
    def execute(self):
        pass
    
    def end(self, interrupted):
        pass
    
    def is_finished(self):
        return True