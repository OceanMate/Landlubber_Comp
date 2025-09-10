from structure.commands.Command import Command

class ParallelCommandGroup(Command):
    def __init__(self):
        super().__init__()
        self.commands = []
    
    def add_commands(self, *commands):
        for command in commands:
            self.commands.append(command)
            super().add_cmd_requirements(command)
    
    def initalize(self):        
        # initalize the all commands
        for command in self.commands:
            command.initalize()
        
    
    def execute(self):
        # if there are no commands to execute, return
        if len(self.commands) <= 0:
            return
        
        for command in self.commands:
            command.execute();
            
            if command.is_finished():
                command.end(False);
                self.commands.remove(command)

    
    
    def end(self, interrupted):
        # if the command is interrupted and there are still commands to be executed, end every command
        if interrupted and len(self.commands) != 0:
            for command in self.commands:
                command.end(True)
    
        # remove all commands
        for command in self.commands:
            self.commands.remove(command)
    
    # returns true if all commands have been finished
    def is_finished(self):
        return len(self.commands) <= 0