from structure.CommandRunner import CommandRunner

class Command:
    def __init__(self):
        self.requirements = []
    
    # Called when the command is first run
    # should be overridden by the child class
    def initalize(self):
        raise NotImplementedError("Subclasses should implement this!")
    
    # Called every time while the command isn't finished
    # should be overridden by the child class
    def execute(self):
        raise NotImplementedError("Subclasses should implement this!")
    
    # Called when the command is finished or interrupted
    # interrupted is a boolean that is true if the command was interrupted
    # should be overridden by the child class
    def end(self, interrupted):
        raise NotImplementedError("Subclasses should implement this!")
    
    # Called to check if the command is finished
    # should be overridden by the child class
    def is_finished(self):
        raise NotImplementedError("Subclasses should implement this!")
    
    # Adds a requireded subsystem to the command
    def add_requirement(self, subsystem):
        self.requirements.append(subsystem.get_subsystem_name())
    
    # Schedules the command in the command runner
    def schedule(self):
        CommandRunner().schedule_command(self)
    
    # Cancels the command in the command runner
    def cancel(self):
        CommandRunner().cancel_command(self)
