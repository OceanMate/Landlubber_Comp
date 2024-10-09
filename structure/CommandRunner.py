class CommandRunner:
    _instance = None

    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.commands = []
        self.default_commands = []
        self.commands_to_schedule = []
        self.commands_to_cancel = []
        self.in_run_loop = False
        self.enabled = False
    
    def run_commands(self):
        
        self.in_run_loop = True
        # Loops through each command to execute and end it if it's finished
        for command in self.commands:
            # If the robot is disabled, this ends and removes each command
            if not self.enabled:
                command.end(True)
                self.commands.remove(command)
                continue
            
            command.execute()

            # If the command is finished, end and remove it
            if command.is_finished():
                command.end(False)
                self.commands.remove(command)
                
        self.in_run_loop = False
        
        if not self.enabled:
            return
        
        # Schedules and cancels commands that were added during the run loop
        for command in self.commands_to_schedule:
            self.schedule_command(command)
        
        for command in self.commands_to_cancel:
            self.cancel_command(command)
            
        self.commands_to_schedule = []
        self.commands_to_cancel = []
        
        # If there are no commands that require a subsystem
        # schedules that subsystem's default command
        for default_command in self.default_commands:
            not_conflicting = True
            for subsystem_reg in default_command.requirements:
                for command in self.commands:
                    if subsystem_reg in command.requirements:
                        not_conflicting = False
            
            if not_conflicting:
                default_command.initalize()
                self.commands.append(default_command)

            
        
    # Schedules the given command to run
    def schedule_command(self, command):
        if self.in_run_loop:
            self.commands_to_schedule.append(command)
            return
        
        # Interrupts any already scheduled commands that require the same subsystem
        for req in command.requirements:
            for c in self.commands:
                if req in c.requirements:
                    c.end(True)
                    self.commands.remove(c)
        
        command.initalize()
        self.commands.append(command)
    
    def add_default_command(self, command):
        for req in command.requirements:
            for c in self.default_commands:
                if req in c.requirements:
                    print("Error: Default command conflicts with another default command")
                    return
                    
        self.default_commands.append(command)
    
    # Cancels the given command if loop isn't running
    # Otherwise, adds it to the list of commands to cancel
    def cancel_command(self, command):
        if self.in_run_loop:
            self.commands_to_cancel.append(command)
            return
        
        if command in self.commands:
            command.end(True)
            self.commands.remove(command)
        
    def turn_off(self):
        self.enabled = False
    
    def turn_on(self):
        self.enabled = True
