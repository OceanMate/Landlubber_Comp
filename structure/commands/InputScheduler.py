from structure.CommandRunner import CommandRunner

# This class is responsible for scheduling commands based on input states
class InputScheduler:
    # Initializes the InputScheduler with a function that returns a boolean value
    # default links to the CommandRunner's default input loop, but could theoretically be changed
    def __init__(self, scheduleBool):
        self.scheduleBool = scheduleBool
        self.loop = CommandRunner().default_input_loop
    
    # Binds a command to be scheduled when the function boolean is true
    def on_true(self, cmd):
        # Inner class to handle the scheduling of the command, needs to have a run method
        class m_runnable():
            def __init__(m_self): # type: ignore
                m_self.pressed_last = self.scheduleBool()

            def run(m_self): # type: ignore
                pressed = self.scheduleBool()
                if not m_self.pressed_last and pressed:
                    cmd.schedule()
                m_self.pressed_last = pressed

        # adds the runnable to the event loop
        self.loop.bind(m_runnable())
    
    # Binds a command to be scheduled when the function boolean is false
    def on_false(self, cmd):
        # Inner class to handle the scheduling of the command, needs to have a run method
        class m_runnable():            
            def __init__(m_self): # type: ignore
                m_self.pressed_last = self.scheduleBool()

            def run(m_self): # type: ignore
                pressed = self.scheduleBool()
                if m_self.pressed_last and not pressed:
                    cmd.schedule()
                m_self.pressed_last = pressed

        # adds the runnable to the event loop
        self.loop.bind(m_runnable())
    
    # Binds a command to be scheduled while the function boolean is true
    def while_true(self, cmd):
        # Inner class to handle the scheduling of the command, needs to have a run method
        class m_runnable():            
            def __init__(m_self): # type: ignore
                m_self.pressed_last = self.scheduleBool()

            def run(m_self): # type: ignore
                pressed  = self.scheduleBool()
                
                if not m_self.pressed_last and pressed:
                    cmd.schedule()
                elif m_self.pressed_last and not pressed:
                    cmd.cancel()
                    
                m_self.pressed_last = pressed

        # adds the runnable to the event loop
        self.loop.bind(m_runnable())
    
    # Binds a command to be scheduled while the function boolean is false
    def while_false(self, cmd):
        # Inner class to handle the scheduling of the command, needs to have a run method
        class m_runnable():            
            def __init__(m_self): # type: ignore
                m_self.pressed_last = self.scheduleBool()

            def run(m_self): # type: ignore
                pressed = self.scheduleBool()
                
                if m_self.pressed_last and not pressed:
                    cmd.schedule()
                elif not m_self.pressed_last and pressed:
                    cmd.cancel()
                    
                m_self.pressed_last = pressed

        # adds the runnable to the event loop
        self.loop.bind(m_runnable())