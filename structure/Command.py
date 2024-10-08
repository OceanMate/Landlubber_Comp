from structure.CommandRunner import CommandRunner

class Command:
    # Called when the command is first run
    # should be overridden by the child class
    def initalize(self):
        pass
    
    # Called every time while the command isn't finished
    # should be overridden by the child class
    def execute(self):
        pass
    
    # Called when the command is finished or interrupted
    # interrupted is a boolean that is true if the command was interrupted
    # should be overridden by the child class
    def end(self, interrupted):
        pass
    
    # Called to check if the command is finished
    # should be overridden by the child class
    def is_finished(self):
        return True
    
    def schedule(self):
        CommandRunner().add_command(self)
