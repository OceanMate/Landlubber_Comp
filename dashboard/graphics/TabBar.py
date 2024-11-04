from tkinter import Canvas

import tkinter.font as tkfont
from dashboard.GraphicConstants import GraphicConstants


class TabBar:
    def __init__(self, window, tabs):
        self.window = window
        self.tabs = tabs
        self.tags_to_tabs = {}
        
        self.next_tab_x = 20
    
    # Generate the tab bar at the top of the window (currently unused)
    def generate_tab_bar(self):
        self.tab_bar_canvas = Canvas(
            self.window,
            bg = GraphicConstants().blue,
            height = GraphicConstants().tab_bar_height,
            width = GraphicConstants().window_width,
            relief = "ridge"
        )
        
        self.tab_bar_canvas.place(x=0, y=0, anchor="nw")
        
        self.add_tab(GraphicConstants().default_tab)
        self.set_current_tab(GraphicConstants().default_tab)
    
    def add_tab(self, tab_name):
        self.tabs[tab_name] = {}
        
        tab_font = tkfont.Font(family=GraphicConstants().font, size=16)
        
        tag_name = ''.join(char for char in tab_name if char.isalnum())
        self.tags_to_tabs[tag_name] = tab_name

        self.tab_bar_canvas.create_text(
            self.next_tab_x,
            GraphicConstants().tab_bar_height / 2,
            text=tab_name,
            font=tab_font,
            fill=GraphicConstants().white,
            anchor="w",
            tags=tag_name
        )
        
        # Measure the width of the actual tab name and add padding
        self.next_tab_x += tab_font.measure(tab_name) + 20
    
    def set_current_tab(self, tab_name):
        for widget in self.tabs[GraphicConstants().current_tab].values():
            widget.hide()
        
        GraphicConstants().current_tab = tab_name
        
        for tab in self.tabs.keys():
            tag_name = ''.join(char for char in tab if char.isalnum())
            self.tab_bar_canvas.itemconfig(tag_name, font=(GraphicConstants().font, 16))
        
        tag_name = ''.join(char for char in tab_name if char.isalnum())
        self.tab_bar_canvas.itemconfig(tag_name, font=(GraphicConstants().font, 16, 'underline'))
        
        for widget in self.tabs[tab_name].values():
            widget.show()
        
                
    def resize_tab_bar(self):
        self.tab_bar_canvas.config(width=GraphicConstants().window_width)

    def get_tab_at_position(self, x, y):
        items = self.tab_bar_canvas.find_overlapping(x, y, x, y)
        if items:
            tag_name = self.tab_bar_canvas.gettags(items[0])[0]
            return self.tags_to_tabs[tag_name]
        return None
