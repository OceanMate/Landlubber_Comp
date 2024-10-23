from structure.CommandRunner import CommandRunner


class InputScheduler:
    def __init__(self, scheduleBool):
        self.scheduleBool = scheduleBool
        self.loop = CommandRunner().default_input_loop
    
    def on_true(self, cmd):
        class m_runnable():            
            def __init__(m_self): # type: ignore
                m_self.pressed_last = self.scheduleBool()

            def run(m_self): # type: ignore
                pressed = self.scheduleBool()
                if not m_self.pressed_last and pressed:
                    cmd.schedule()
                m_self.pressed_last = pressed

        self.loop.bind(m_runnable())
    
    def on_false(self, cmd):
        class m_runnable():            
            def __init__(m_self): # type: ignore
                m_self.pressed_last = self.scheduleBool()

            def run(m_self): # type: ignore
                pressed = self.scheduleBool()
                if m_self.pressed_last and not pressed:
                    cmd.schedule()
                m_self.pressed_last = pressed

        self.loop.bind(m_runnable())
    
    def while_true(self, cmd):
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

        self.loop.bind(m_runnable())
    
    def while_false(self, cmd):
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

        self.loop.bind(m_runnable())