import logging
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from ..events.event_constants import *
from ..events.event_broker import EventBroker
from ..events.event_subscriber import EventSubscriber
from ..events.event_publisher import EventPublisher



class MenuFrame(tk.Menu):

    logger = logging.getLogger(__name__)

    initialdir = '.'


    def __init__(self, master, event_broker: EventBroker, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)


        self.event_subscriber = EventSubscriber(event_broker)
        self.event_publisher = EventPublisher(event_broker)

        # ==================== FILE MENU ====================

        self.file_menu = tk.Menu(self, tearoff=False)
        self.file_menu.add_command(label="Open File", command=self.handle_open_file)
        self.file_menu.add_command(label='Open Webcam', command=self.handle_open_webcam)
        self.file_menu.add_command(label="Save", command=self.handle_save)
        self.file_menu.add_command(label="Save As", command=self.handle_save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.handle_exit)
        self.add_cascade(label="File", menu=self.file_menu)

        # ==================== EDIT MENU ====================

        self.edit_menu = tk.Menu(self, tearoff=False)
        self.edit_menu.add_command(label="Undo", command=self.handle_undo)
        self.edit_menu.add_command(label="Redo", command=self.handle_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Resize", command=self.handle_resize)
        self.add_cascade(label="Edit", menu=self.edit_menu)

        # ==================== VIEW MENU ====================

        self.sidebar_state = tk.BooleanVar(value=True)
        self.console_state = tk.BooleanVar(value=True)
        self.side_display_state = tk.BooleanVar(value=True)
        
        self.view_menu = tk.Menu(self, tearoff=False)

        self.view_menu.add_checkbutton(label='Sidebar',
                                       variable=self.sidebar_state,
                                       command=self.handle_toggle_sidebar)
        
        self.view_menu.add_checkbutton(label='Console', 
                                       variable=self.console_state,
                                       command=self.handle_toggle_console)
        
        self.view_menu.add_checkbutton(label='Side Display',
                                        variable=self.side_display_state,
                                        command=self.handle_toggle_side_display)
                                       
        
        self.add_cascade(label="View", menu=self.view_menu)

        # ==================== HELP MENU ====================

        self.help_menu = tk.Menu(self, tearoff=False)
        self.help_menu.add_command(label="About", command=self.handle_about)
        self.add_cascade(label="Help", menu=self.help_menu)

        # ==================== DISABLE COMMANDS ====================

        # For commands that havent been implemented yet
        self.disable_commands()

        self.logger.info('MenuWidget initialized')


    def disable_commands(self):
        self.file_menu.entryconfig('Save', state='disabled')
        self.file_menu.entryconfig('Save As', state='disabled')
        self.edit_menu.entryconfig('Undo', state='disabled')
        self.edit_menu.entryconfig('Redo', state='disabled')
        self.edit_menu.entryconfig('Resize', state='disabled')
        self.help_menu.entryconfig('About', state='disabled')

    
    def handle_open_file(self):
        filename = filedialog.askopenfilename(initialdir=self.initialdir, 
                                              title='Select a file',
                                              filetypes=(('png files', '*.png'),
                                                         ('all files', '*.*')))

        if not filename:
            return

        self.event_publisher.publish(MenuEvent.OPEN_IMAGE, filename=filename)


    def handle_open_webcam(self):
        self.event_publisher.publish(MenuEvent.OPEN_WEBCAM)


    def handle_save_as(self):
        raise NotImplementedError('Save As not implemented yet')
    
    def handle_save(self):
        raise NotImplementedError('Save not implemented yet')
    
    def handle_undo(self):
        raise NotImplementedError('Undo not implemented yet')
    
    def handle_redo(self):
        raise NotImplementedError('Redo not implemented yet')
    
    def handle_resize(self):
        raise NotImplementedError('Resize not implemented yet')
    
    def handle_exit(self):
        self.event_publisher.publish(MenuEvent.EXIT)

    def handle_toggle_sidebar(self):
        self.event_publisher.publish(MenuEvent.TOGGLE_SIDEBAR, self.sidebar_state.get())
    
    def handle_toggle_console(self):
        self.event_publisher.publish(MenuEvent.TOGGLE_CONSOLE, self.console_state.get())

    def handle_toggle_side_display(self):
        self.event_publisher.publish(MenuEvent.TOGGLE_SIDE_DISPLAY, self.side_display_state.get())
    
    def handle_about(self):
        raise NotImplementedError('About not implemented yet')




