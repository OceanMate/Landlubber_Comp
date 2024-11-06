from dashboard.Dashboard import Dashboard


class DashboardTab:
    def __init__(self, tab_name):
        self.tab_name = tab_name
        Dashboard().add_tab(tab_name)
    
    def put_string(self, label, text):
        Dashboard().put_string(label, text, self.tab_name)
    
    def put_boolean(self, label, boolean):
        Dashboard().put_boolean(label, boolean, self.tab_name)
    
    def put_button(self, label, command):
        Dashboard().put_button(label, command, self.tab_name)

