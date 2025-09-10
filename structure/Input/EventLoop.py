# EventLoop Class to manage the execution of actions in a loop.
class EventLoop:
    def __init__(self):
        self.m_bindings = []

    def bind(self, action):
        self.m_bindings.append(action)

    def poll(self):
        # Execute all bound actions
        for action in self.m_bindings:
            # Assuming action has a run method
            action.run()

    def clear(self):
        self.m_bindings.clear()
  
