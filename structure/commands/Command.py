from structure.CommandRunner import CommandRunner

class Command:
    # Child Classes should call this in their constructors
    def __init__(self):
        # Initializes the requirements dictionary. A dictionary of boolean values
        self.requirements = {}
    
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
    def is_finished(self) -> bool:
        return True
    
    # Adds a requireded subsystem to the command
    def add_requirement(self, subsystem):
        self.requirements[subsystem.get_subsystem_name()] = True
    
    # adds another commands requirmets to this command
    def add_cmd_requirements(self, cmd):
        for key in cmd.requirements.keys():
            self.requirements[key] = True

    def is_confliting(self, command):
        # Check if the command has conflicting requirements
        for key in self.requirements.keys():
            # If the command has a requirement that this command also requires, then they conflict
            if key in command.requirements.keys():
                return True
        return False
    
    # Schedules the command in the command runner
    def schedule(self):
        CommandRunner().schedule_command(self)
    
    # Cancels the command in the command runner
    def cancel(self):
        CommandRunner().cancel_command(self)
