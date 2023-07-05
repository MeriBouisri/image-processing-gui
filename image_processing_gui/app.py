import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

from .frames.menu_frame import MenuFrame
from .frames.console_frame import ConsoleFrame
from .frames.sidebar_frame import SidebarFrame
from .frames.display_frame import DisplayFrame
from .frames.toolbar_frame import ToolbarFrame

from .image_processing.opencv.opencv_sidebar import OpenCVSidebar


from .events import event_constants as events
from .events.event_broker import EventBroker
from .events.event_subscriber import EventSubscriber
from .events.event_publisher import EventPublisher

import sys

import logging



class App:


    def __init__(self):

        # root.mainloop()
        # ==================== INITIALIZE ROOT WINDOW ==================== #
        self.root = tk.Tk()
        
        root_width = self.root.winfo_screenwidth()
        root_height = self.root.winfo_screenheight()

        self.root.title("Image Processing")
        self.root.geometry(f"{root_width}x{root_height}")
        self.root.wm_state('zoomed')
        self.root.resizable(True, True)

        # ==================== INITIALIZE LOGGER ==================== #
        
        self.logger = logging.getLogger(__name__)


        # ==================== INITIALIZE EVENT SYSTEM ==================== #

        self.event_broker = EventBroker()
        self.event_subscriber = EventSubscriber(self.event_broker)
        self.event_publisher = EventPublisher(self.event_broker)


        # ==================== INITIALIZE CONSOLE WIDGET ==================== #

        self.console = ConsoleFrame(master=self.root, event_broker=self.event_broker)

        # ==================== INITIALIZE MENU WIDGET ==================== #

        self.menu = MenuFrame(master=self.root, event_broker=self.event_broker)
        self.root.config(menu=self.menu)

        # ==================== INITIALIZE SIDEBAR WIDGET ==================== #

        self.sidebar = SidebarFrame(master=self.root, event_broker=self.event_broker)
        self.sidebar.add_sidebar('Image Processing', OpenCVSidebar)

        # ==================== INITIALIZE DISPLAY WIDGET ==================== #

        self.display = DisplayFrame(master=self.root, event_broker=self.event_broker)

        # ==================== CONFIGURE LAYOUT  ==================== #

        self.global_grid_config = {'sticky': tk.NSEW, 'padx': 5, 'pady': 5}
        self.global_border_config = {'relief': tk.SOLID, 'borderwidth': 1}

        self.display_layout = {'row': 0, 'column': 1, 'rowspan': 1, 'columnspan': 1}
        self.console_layout = {'row': 1, 'column': 1, 'rowspan': 1, 'columnspan': 1}
        self.sidebar_layout = {'row': 0, 'column': 0, 'rowspan': 2, 'columnspan': 1}

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=5)

        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=1)

        self.sidebar.grid(**self.sidebar_layout, **self.global_grid_config)
        self.display.grid(**self.display_layout, **self.global_grid_config)
        self.console.grid(**self.console_layout, **self.global_grid_config)

        self.sidebar.config(**self.global_border_config)
        self.display.config(**self.global_border_config)
        self.console.config(**self.global_border_config)

        # ========== VISIBILITY ========== #

        self.sidebar_visible = True
        self.console_visible = True

        # ==================== EVENT BINDINGS ==================== #

        self.logger.info("App initialized")

        self.event_subscriber.subscribe(events.MenuEvent.TOGGLE_CONSOLE, self.on_toggle_console)
        self.event_subscriber.subscribe(events.MenuEvent.TOGGLE_SIDEBAR, self.on_toggle_sidebar)

    def on_toggle_console(self, event, state):
        self.console_visible = state

        if not self.console_visible:
            self.console.grid_remove()
            self.console.grid_forget()

        self.update_layout()
    
    def on_toggle_sidebar(self, event, state):
        self.sidebar_visible = state

        if not self.sidebar_visible:
            self.sidebar.grid_remove()
            self.sidebar.grid_forget()
        
        self.update_layout()

    def update_layout(self):
        updated_display_layout = self.display_layout.copy()
        updated_console_layout = self.console_layout.copy()

        if not self.console_visible:
            updated_display_layout['columnspan'] = 2
            updated_display_layout['rowspan'] = 2

        if not self.sidebar_visible: 
            updated_display_layout['columnspan'] = 2
            updated_display_layout['column'] = 0

        # Display always visible
        self.display.grid(**updated_display_layout) # type: ignore

        if self.console_visible:
            updated_console_layout['column'] = updated_display_layout['column']
            updated_console_layout['columnspan'] = updated_display_layout['columnspan']
            self.console.grid(**updated_console_layout) # type: ignore

        if self.sidebar_visible:
            self.sidebar.grid(**self.sidebar_layout) # type: ignore

        
        


