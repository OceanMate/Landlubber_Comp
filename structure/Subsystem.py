from structure.CommandRunner import CommandRunner

class Subsystem:

    # Creates a default command for the subsystem 
    # scheduled if no other command that requires the subsystem is running
    def defaultCommand(self, command):
        class_name = self.__class__.__name__

        # Adds the subsystem to the command's requirements if not already there
        if class_name not in command.requirements:
            command.add_requirement(self)
        
        CommandRunner().add_default_command(command) 
    
    # Returns the name of the child subsystem
    def get_subsystem_name(self):
        return self.__class__.__name__