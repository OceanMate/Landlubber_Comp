from jigboard.Jigboard import Jigboard

# Creates a tab on the dashboard to put widgets on
class JigboardTab:
    def __init__(self, tab_name):
        self.tab_name = tab_name
        Jigboard().add_tab(tab_name)
    
    def put_string(self, label, text):
        Jigboard().put_string(label, text, self.tab_name)
    
    def put_boolean(self, label, boolean):
        Jigboard().put_boolean(label, boolean, self.tab_name)
    
    def put_button(self, label, command):
        Jigboard().put_button(label, command, self.tab_name)

