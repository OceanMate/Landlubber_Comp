from structure.CommandRunner import CommandRunner
from structure.Command import Command

class Subsystem:
    def __init__(self, name):
        self.name = name

    def defaultCommand(self, command):
        CommandRunner().add_default_command(command) 