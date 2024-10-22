
class EventLoop:
    def __init__(self):
        self.m_bindings = []

    def bind(self, action):
        self.m_bindings.append(action)


    def poll(self):
        for action in self.m_bindings:
            action.run()


    def clear(self):
        self.m_bindings.clear()
  
