from typing import Callable

# This class is responsible for scheduling commands based on input states
class InputScheduler:
    # Initializes the InputScheduler with a function that returns a boolean value
    # default links to the CommandRunner's default input loop, but could theoretically be changed
    def __init__(self, scheduleBool):
        from structure.CommandRunner import CommandRunner

        self.scheduleBool = scheduleBool
        self.loop = CommandRunner().default_input_loop
    
    def set_loop(self, loop):
        self.loop = loop
    
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
    
    def non_cmd_on_true(self, func):
        # Inner class to handle the scheduling of the command, needs to have a run method
        class m_runnable():
            def __init__(m_self): # type: ignore
                m_self.pressed_last = self.scheduleBool()
            
            def run(m_self): # type: ignore
                pressed = self.scheduleBool()
                if not m_self.pressed_last and pressed:
                    func()
                m_self.pressed_last = pressed
        
        self.loop.bind(m_runnable())

    def non_cmd_on_false(self, func):
        class m_runnable():
            def __init__(m_self): # type: ignore
                m_self.pressed_last = self.scheduleBool()
            
            def run(m_self): # type: ignore
                pressed = self.scheduleBool()
                if m_self.pressed_last and not pressed:
                    func()
                m_self.pressed_last = pressed
        
        self.loop.bind(m_runnable())

    def non_cmd_while_true(self, func):
        class m_runnable():
            def run(m_self): # type: ignore
                if self.scheduleBool():
                    func()
        
        self.loop.bind(m_runnable())

    def non_cmd_while_false(self, func):
        class m_runnable():        
            def run(m_self): # type: ignore
                if not self.scheduleBool():
                    func()
        
        self.loop.bind(m_runnable())

    # a goofy way of getting a boolean that is true when the button is pressed
    def get_on_true(self) -> Callable:
        class m_runnable():
            def __init__(m_self): # type: ignore
                m_self.pressed_last = self.scheduleBool()
            
            def run(m_self): # type: ignore
                pressed = self.scheduleBool()
                if not m_self.pressed_last and pressed:
                    m_self.pressed_last = pressed
                    return True
                m_self.pressed_last = pressed
                return False
        
        runnable = m_runnable()
        return runnable.run

    def get_on_false(self) -> Callable:
        class m_runnable():
            def __init__(m_self): # type: ignore
                m_self.pressed_last = self.scheduleBool()
            
            def run(m_self): # type: ignore
                pressed = self.scheduleBool()
                if m_self.pressed_last and not pressed:
                    m_self.pressed_last = pressed
                    return True
                m_self.pressed_last = pressed
                return False
        
        runnable = m_runnable()
        return runnable.run

    def get_while_true(self) -> Callable:
        return self.scheduleBool

    def get_while_false(self) -> Callable:
        return lambda: not self.scheduleBool()