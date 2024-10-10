from structure.CommandRunner import CommandRunner
#from structure.commands.Command import Command

class Subsystem:
    def __init__(self, name):
        self.name = name

    # Creates a default command for the subsystem 
    # scheduled if no other command that requires the subsystem is running
    def defaultCommand(self, command):

        # Adds the subsystem to the command's requirements if not already there
        if self.name not in command.requirements:
            command.add_requirement(self.name)
        
        CommandRunner().add_default_command(command) 