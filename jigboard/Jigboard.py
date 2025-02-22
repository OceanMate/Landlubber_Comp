import sys
from tkinter import PhotoImage, Tk
import ctypes
from typing import Callable

from jigboard.graphics.BottomBar import BottomBar
from jigboard.graphics.NetworkData import NetworkData
from jigboard.graphics.TabBar import TabBar
from jigboard.graphics.GridGraphics import GridGraphics
from jigboard.GraphicConstants import GraphicConstants

from jigboard.widgets.BooleanWidget import BooleanWidget
from jigboard.widgets.StringWidget import StringWidget
from jigboard.widgets.ButtonWidget import ButtonWidget
from jigboard.widgets.CameraWidget import CameraWidget

from structure.Input.EventLoop import EventLoop
from structure.Input.KeyboardInput import KeyboardInput
from structure.RobotState import RobotState

from transmission.ComsThread import ComsThread
from transmission.CameraComs import CameraComs


class Jigboard:
    _instance = None

    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._start()
        return cls._instance
    
    def _start(self):  
        # Widget Dictionary and lists
        self.tabs = {}
        self.camera_widgets = []
             
        # Create window
        self.window = Tk()
        self.window.geometry(str(GraphicConstants().window_width) + "x" + str(GraphicConstants().window_height))
        self.window.configure(bg = "#FFFFFF")
        self.window.title("Jigboard")

        def on_closing():
            self.enable = False
        
        # Make the program exit when the window is closed
        self.window.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Set the icon and ID for the window
        appID = "Jigboard"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appID)
        # set task bar icon
        icon = PhotoImage( file = GraphicConstants().get_asset_path("Rabbit_logo.png"))
        self.window.iconphoto(True, icon)
        # set upper left icon
        self.window.iconbitmap(GraphicConstants().get_asset_path("Rabbit_logo.ico"))
        
        # Generate the various components of the dashboard
        self.tab_bar = TabBar(self.window, self.tabs)
        self.tab_bar.generate_tab_bar()
        
        self.grid_graphics = GridGraphics()
        self.grid_graphics.init(self.window, self.tabs)
        self.grid_graphics.generate_grid()
        
        self.bottom_bar = BottomBar(self.window)
        self.bottom_bar.create_bottom_bar()
        
        self.network_data = NetworkData()
        self.network_data.init(self.window)
        
        # Setup hotkeys for the dashboard
        self._setup_hotkeys()
        
        # Enable the dashboard
        self.enable = True
                
    # Setup hotkeys for the dashboard 
    def _setup_hotkeys(self):
        # Event loop for the dashboard for hotkeys, need this to manage the keyboardListener thread
        self.hotkeys_loop = EventLoop()
        
        # Hotkey to disable the robot
        def on_enter():
            if RobotState().is_teleop_enabled():
                RobotState().disable_robot()
                self.bottom_bar.update_enable_button(is_enabling=False)
        
        # Create the hotkey for the enter key
        enter_hotkey = KeyboardInput("enter")
        # Set the function to run when the hotkey is pressed
        enter_hotkey.non_cmd_on_true(func=on_enter)
        # Set the loop for the hotkey to be the dashboard loop
        enter_hotkey.set_loop(loop=self.hotkeys_loop)     
    
    def _create_or_update_widget(self, label, widget_class, create_func, update_func, *args, tab):
        if self.grid_graphics is None:
            return
        
        widget_label = tab + label
        
        # Check if the tab exists, if not create it
        if widget_label not in self.tabs[tab].keys():
            self.tabs[tab][widget_label] = widget_class(self.grid_graphics.grid_canvas, widget_label, *args)
            
            # Get the default dimensions of the widget
            widget_grid_width, widget_grid_height = self.tabs[tab][widget_label].get_default_dimensions()
            
            # Place the widget on the grid
            loc = self.grid_graphics.find_next_available_space(widget_grid_width, widget_grid_height, tab)
            self.grid_graphics.place_rectangle(loc[0], loc[1], widget_grid_width, widget_grid_height, tab)
            
            # Create the widget on the canvas
            create_func(self.tabs[tab][widget_label], loc[0], loc[1])
            
            # Hide the widget if it is not on the current tab
            if tab != GraphicConstants().current_tab:
                self.tabs[tab][widget_label].hide()
        else:
            # Update the widget
            update_func(self.tabs[tab][widget_label], *args)
        
        return self.tabs[tab][widget_label]
    
    def put_data(self, label: str, data, tab=GraphicConstants().default_tab):
        if type(data) == bool or type(data) == tuple:
            return self.put_boolean(label, data, tab)
        if type(data) == str:
            return self.put_string(label, data, tab)
        if type(data) ==Callable:
            return self.put_button(label, data, tab)
        if type(data) == int:
            return self.put_camera(label, data, tab)
        
        print("Data type not supported, please use a boolean, string, callable or int")

    def put_string(self, label: str, text: str, tab=GraphicConstants().default_tab):
        self._create_or_update_widget(
            label, StringWidget,
            lambda widget, x, y: widget.create_string_widget(x, y, text),
            lambda widget, text: widget.update_text(text),
            text, tab=tab
        )

    def put_boolean(self, label: str, boolean: bool, tab=GraphicConstants().default_tab):
        self._create_or_update_widget(
            label, BooleanWidget,
            lambda widget, x, y: widget.create_bool_widget(x, y, boolean),
            lambda widget, boolean: widget.update_bool(boolean),
            boolean, tab=tab
        )

    def put_button(self, label: str, command: Callable, tab=GraphicConstants().default_tab):
        self._create_or_update_widget(
            label, ButtonWidget,
            lambda widget, x, y: widget.create_button_widget(x, y),
            lambda widget, command: setattr(widget, 'command', command),
            command, tab=tab
        )

    def put_camera(self, label: str, camera_id: int, tab=GraphicConstants().default_tab):
        cam_widget = self._create_or_update_widget(
            label, CameraWidget,
            lambda widget, x, y: widget.create_camera_widget(x, y),
            lambda widget, camera_id: setattr(widget, 'camera_id', camera_id),
            camera_id, tab=tab
        )
        
        self.camera_widgets.append(cam_widget)

    def put_all_camera_widgets(self, tab = GraphicConstants().default_tab):
        # Create a camera widget for each camera
        for camera_id in range(CameraComs().get_num_of_cameras()):
            self.put_camera("Camera " + str(camera_id), camera_id, tab)
    
    # Function that should be called periodicly to update the dashboard
    def update(self):
        # Debug the grid
        # self.grid_graphics.debug_grid()
        
        # Check if the window has been resized, and resize all the widgets if it has        
        if GraphicConstants().window_width != self.window.winfo_width() or GraphicConstants().window_height != self.window.winfo_height():
            self._remake_window()
        
        if self.network_data.enabled:
            self.network_data.draw_network_data()
        
        for camera_widget in self.camera_widgets:
            camera_widget.update_image()
        
        # Update the window, use this instead of mainloop to allow for other functions to be called (non-blocking)
        self.window.update()
        
        # Update the connection status in the bottom bar
        self.bottom_bar.update_comms_text(ComsThread().connected)
        
        # Check hotkeys
        self.hotkeys_loop.poll()
        
        # Check if the dashboard has been disabled, and close the window if it has
        if not self.enable:
            self._close()
    
    # Remake the whole window to reflect changes in the window size
    def _remake_window(self):
        GraphicConstants().window_width = self.window.winfo_width()
        GraphicConstants().window_height = self.window.winfo_height()
        
        # recreate all the canvases
        self.tab_bar.resize_tab_bar()
        self.grid_graphics.resize_grid()
        self.bottom_bar.resize_bottom_bar()
        
        if self.network_data.enabled:
            self.network_data.resize_network_data()
        
        # replace all the widgets on the grid and show/hide them as needed
        for tab in self.tabs.keys():
            for widget in self.tabs[tab].values():
                self.grid_graphics.place_rectangle(widget.grid_x, widget.grid_y, widget.grid_width, widget.grid_height, tab)
                
                if tab != GraphicConstants().current_tab:
                    widget.hide()
                else:
                    widget.show()
        
        # Move all widgets that are out of bounds to the next available space
        out_of_bound_widgets = {}
        
        # Check if the widget is out of bounds and add it to the list
        for tab in self.tabs.keys():
            out_of_bound_widgets[tab] = []
            
            for widget in self.tabs[tab].values():
                if self.grid_graphics.is_out_of_bounds(widget.grid_x, widget.grid_y, widget.grid_width, widget.grid_height):
                    self.grid_graphics.remove_rectangle(widget.grid_x, widget.grid_y, widget.grid_width, widget.grid_height, tab)
                    out_of_bound_widgets[tab].append(widget)

        # Move all widgets in the out of bounds list to the next available space
        for tab in out_of_bound_widgets.keys():
            for widget in out_of_bound_widgets[tab]:
                new_x, new_y = self.grid_graphics.find_next_available_space(widget.grid_width, widget.grid_height, tab)
                widget.move_widget(new_x, new_y)
                
                if tab != GraphicConstants().current_tab:
                    widget.hide()
    
    # Close the window and exit the program
    def _close(self):
        self.window.destroy()
        sys.exit(0)
    
    # Add a tab to the dashboard. Creates a new tab and grid for the tab
    def _add_tab(self, tab_name):
        if tab_name not in self.tabs.keys():
            self.tab_bar.add_tab(tab_name)
            self.grid_graphics.create_new_tab_grid(tab_name)