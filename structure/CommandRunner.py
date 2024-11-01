from dashboard.Dashboard import Dashboard
from structure.Input.EventLoop import EventLoop

class CommandRunner:
    _instance = None

    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._start()
        return cls._instance
    
    # Private method that acts as an initializer
    def _start(self):
        # arrays to hold commands
        self.commands = []
        self.default_commands = []
        self.commands_to_schedule = []
        self.commands_to_cancel = []
        
        # subsystem periodics that get run every loop
        self.subsystem_periodics = []
        
        # booleans to change the state of the command runner
        self.in_run_loop = False
        self.enabled = False
        self.canceled_commands = False
        
        # The default input loop for inputs to schedule commands
        self.default_input_loop = EventLoop()
        
        self.possible_requirements = []
            
    def run_commands(self):
        if self.canceled_commands and not self.enabled:
            return
        
        # Polls the input loop for any new commands to schedule
        self.default_input_loop.poll()
        
        # Runs the periodic functions of each subsystem
        for periodic in self.subsystem_periodics:
            periodic()
        
        self.in_run_loop = True
        # Loops through each command to execute and end it if it's finished
        for command in self.commands:
            # If the robot is disabled, this ends and removes each command
            if not self.enabled:
                command.end(True)
                self.commands.remove(command)
                continue
            
            Dashboard().put_string("Command", command.__class__.__name__, 0, 0)
            command.execute()

            # If the command is finished, end and remove it
            if command.is_finished():
                command.end(False)
                self.commands.remove(command)
                
        self.in_run_loop = False
        
        # Prevents the scheduling of commands if the robot is disabled (needs to be here so it can end the commands)
        if not self.enabled:
            self.canceled_commands = True
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
            for command in self.commands:
                if default_command.is_confliting(command):
                    not_conflicting = False
                    break
            
            if not_conflicting:
                default_command.initalize()
                self.commands.append(default_command)

            
        
    # Schedules the given command to run
    def schedule_command(self, command):
        if self.in_run_loop:
            self.commands_to_schedule.append(command)
            return
        
        # Interrupts any already scheduled commands that require the same subsystem
        for cmd in self.commands:
            if command.is_confliting(cmd):
                self.cancel_command(cmd)
        
        command.initalize()
        self.commands.append(command)
    
    # adds a default command to the list of default commands
    def add_default_command(self, command):
        for cmd in self.default_commands:
            if command.is_confliting(cmd):
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
        self.canceled_commands = False
        self.enabled = True