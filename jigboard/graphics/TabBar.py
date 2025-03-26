from tkinter import Canvas

import tkinter.font as tkfont
from jigboard.GraphicConstants import GraphicConstants
from jigboard.graphics.GridGraphics import GridGraphics
from jigboard.graphics.NetworkData import NetworkData



class TabBar:
    def __init__(self, window, tabs):
        self.window = window
        self.tabs = tabs
        
        # Dictionary to map tags to tab names
        self.tags_to_tabs = {}
        
        # stores the x position of the next tab, 20 for the first tab
        self.next_tab_x = 20 + GraphicConstants().tab_bar_height
    
    # Generate the tab bar at the top of the window 
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
        
        # Network Data Tab
        self.tab_bar_canvas.create_rectangle(
            2, 2, GraphicConstants().tab_bar_height - 1, GraphicConstants().tab_bar_height - 1,  # Coordinates for the rectangle
            fill=GraphicConstants().white,
            outline=GraphicConstants().blue,
            tags="network"
        )
        # Add a symbol (e.g., a "+" sign) inside the rectangle
        self.tab_bar_canvas.create_text(
            GraphicConstants().tab_bar_height / 2,
            GraphicConstants().tab_bar_height / 2,
            text=">>",
            font=tkfont.Font(family=GraphicConstants().font, size=16),
            fill=GraphicConstants().blue,
            tags="network_symbol"
        )
        
        self.network_data_active = False
        
        # Add the default tab and set it as the current tab
        self.add_tab(GraphicConstants().default_tab)
        self.set_current_tab(GraphicConstants().default_tab)
        
        # Make the tab bar switch tabs when clicked
        self.tab_bar_canvas.bind("<Button-1>", self._on_click)
    
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
        
        # Move all widgets that are out of bounds to the next available space
        for widget in self.tabs[tab_name].values():
            if GridGraphics().is_out_of_bounds(widget.grid_x, widget.grid_y, widget.grid_width, widget.grid_height):
                new_x, new_y = GridGraphics().find_next_available_space(widget.grid_width, widget.grid_height, tab_name)
                widget.move_widget(new_x, new_y)
            
    # Get the tag name of a tab name
    def get_tag_name(self, tab_name):
        # Remove special characters from the tab name for use as tags
        return ''.join(char for char in tab_name if char.isalnum())
    
    def network_data_clicked(self):
        self.network_data_active = not self.network_data_active
        if self.network_data_active:
            NetworkData().generate_grid()
            # Change the network symbol to point down
            self.tab_bar_canvas.itemconfig("network_symbol", text="<<")
        else:
            GridGraphics().grid_canvas.itemconfig("network", state="hidden")
            NetworkData().destroy_grid()
            # Change the network symbol to point right
            self.tab_bar_canvas.itemconfig("network_symbol", text=">>")
    
    # Resize the tab bar to fit the window
    def resize_tab_bar(self):
        self.tab_bar_canvas.config(width=GraphicConstants().window_width)
    
    # Function to call when a tab is clicked. Switches the current tab to the clicked tab
    def _on_click(self, event):
        clicked_tab = self.get_tab_at_position(event.x, event.y)
        
        # Checks if there is a value in clicked_tab, then sets the current tab to the clicked tab
        if clicked_tab:
            self.set_current_tab(clicked_tab)
            return
        
        # Checks if the network tab is clicked, then sets the current tab to the network tab
        if self.is_network_clicked(event.x, event.y):
            self.network_data_clicked()

    # Get the tab at the given position
    def get_tab_at_position(self, x, y):
        # Finds each item that overlaps the given position
        items = self.tab_bar_canvas.find_overlapping(x, y, x, y)

        if items:
            # Get the tag name of the first item that overlaps the given position
            try:
                tag_name = self.tab_bar_canvas.gettags(items[0])[0]
                return self.tags_to_tabs[tag_name]
            except KeyError:
                return None
        return None
    
    def is_network_clicked(self, x, y):
        items = self.tab_bar_canvas.find_overlapping(x, y, x, y)
        if items:
            tag_name = self.tab_bar_canvas.gettags(items[0])[0]
            return tag_name == "network"
        return False
