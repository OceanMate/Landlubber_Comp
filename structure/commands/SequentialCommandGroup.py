from structure.commands.Command import Command

class SequentialCommandGroup(Command):
    def __init__(self):
        super().__init__()
        self.commands = []
        self.current_command = -1
    
    def add_commands(self, *commands):
        for command in commands:
            self.commands.append(command)
            super().add_cmd_requirements(command)
    
    def initalize(self):
        self.current_command = 0
        
        # initalize the first command
        if len(self.commands) > 0:
            self.commands[self.current_command].initalize()
        
    
    def execute(self):
        # if there are no commands to execute, return
        if len(self.commands) <= 0:
            return
        
        currentCommand = self.commands[self.current_command]

        currentCommand.execute();
        
        # if the current command is finished, end it and move to the next command
        if currentCommand.is_finished():
            currentCommand.end(False);
            self.current_command += 1
            if self.current_command < len(self.commands):
                self.commands[self.current_command].initalize()
            
        
    
    def end(self, interrupted):
        # if the command is interrupted and there are still commands to be executed, end the current command
        if interrupted and len(self.commands) != 0:
            if self.current_command > -1 and self.current_command < len(self.commands):
                self.commands[self.current_command].end(True)
    
        # stop all commands
        self.current_command = -1;
    
    # returns true if all commands have been finished
    def is_finished(self):
        return self.current_command >= len(self.commands)