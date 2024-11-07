from tkinter import Canvas

import tkinter.font as tkfont
from dashboard.GraphicConstants import GraphicConstants


class TabBar:
    def __init__(self, window, tabs):
        self.window = window
        self.tabs = tabs
        
        # Dictionary to map tags to tab names
        self.tags_to_tabs = {}
        
        self.next_tab_x = 20
    
    # Generate the tab bar at the top of the window (currently unused)
    def generate_tab_bar(self):
        # Create the tab bar canvas
        self.tab_bar_canvas = Canvas(
            self.window,
            bg = GraphicConstants().blue,
            height = GraphicConstants().tab_bar_height,
            width = GraphicConstants().window_width,
            relief = "ridge"
        )
        
        self.tab_bar_canvas.place(x=0, y=0, anchor="nw")
        
        # Add the default tab and set it as the current tab
        self.add_tab(GraphicConstants().default_tab)
        self.set_current_tab(GraphicConstants().default_tab)
        
        # Make the tab bar switch tabs when clicked
        self.tab_bar_canvas.bind("<Button-1>", self._on_tab_click)
    
    # Add a tab to the tab bar
    def add_tab(self, tab_name):
        # Create a dictionary to store widgets for the tab
        self.tabs[tab_name] = {}
        
        tab_font = tkfont.Font(family=GraphicConstants().font, size=16)
        
        # Remove special characters from the tab name for use as tags
        tag_name = self.get_tag_name(tab_name)
        self.tags_to_tabs[tag_name] = tab_name

        # Create the tab name on the tab bar
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
    
    # Set the current tab to the given tab name
    def set_current_tab(self, tab_name):
        # Hide all widgets in the previous tab
        for widget in self.tabs[GraphicConstants().current_tab].values():
            widget.hide()
            
        # Remove the underline from the previous tab
        previous_tag_name = self.get_tag_name(GraphicConstants().current_tab)
        self.tab_bar_canvas.itemconfig(previous_tag_name, font=(GraphicConstants().font, 16))
        
        # Set the current tab to the given tab name
        GraphicConstants().current_tab = tab_name
        
        # Add an underline to the current tab
        tag_name = self.get_tag_name(tab_name)
        self.tab_bar_canvas.itemconfig(tag_name, font=(GraphicConstants().font, 16, 'underline'))
        
        # Show all widgets in the current tab
        for widget in self.tabs[tab_name].values():
            widget.show()
    
    # Get the tag name of a tab name
    def get_tag_name(self, tab_name):
        # Remove special characters from the tab name for use as tags
        return ''.join(char for char in tab_name if char.isalnum())
        
    
    # Resize the tab bar to fit the window
    def resize_tab_bar(self):
        self.tab_bar_canvas.config(width=GraphicConstants().window_width)
    
    # Function to call when a tab is clicked. Switches the current tab to the clicked tab
    def _on_tab_click(self, event):
        clicked_tab = self.get_tab_at_position(event.x, event.y)
        
        # Checks if there is a value in clicked_tab, then sets the current tab to the clicked tab
        if clicked_tab:
            self.set_current_tab(clicked_tab)

    # Get the tab at the given position
    def get_tab_at_position(self, x, y):
        # Finds each item that overlaps the given position
        items = self.tab_bar_canvas.find_overlapping(x, y, x, y)
        if items:
            # Get the tag name of the first item that overlaps the given position
            tag_name = self.tab_bar_canvas.gettags(items[0])[0]
            return self.tags_to_tabs[tag_name]
        return None
