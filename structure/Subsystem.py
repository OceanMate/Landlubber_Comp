from structure.CommandRunner import CommandRunner

class Subsystem():
    # Initializes the Subsystem and adds it to the CommandRunner's possible requirements
    # Child classes should call this in their constructors
    def __init__(self):
        CommandRunner().subsystem_periodics.append(self.periodic)

    # Creates a default command for the subsystem 
    # scheduled if no other command that requires the subsystem is running
    def default_command(self, command):
        class_name = self.get_subsystem_name()

        # Adds the subsystem to the command's requirements if not already there
        if class_name not in command.requirements:
            command.add_requirement(self)
        
        CommandRunner().add_default_command(command) 
    
    def periodic(self):
        pass
    
    # Returns the name of the child subsystem
    def get_subsystem_name(self):
        return self.__class__.__name__