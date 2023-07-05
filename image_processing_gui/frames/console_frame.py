import logging
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from ..console.console_tab import ConsoleTab
from ..console.console_logger import ConsoleLogger
from ..console.console_redirect import ConsoleRedirect


from ..events.event_broker import EventBroker
from ..events.event_publisher import EventPublisher
from ..events.event_subscriber import EventSubscriber
from ..events.event_constants import *


class ConsoleFrame(ttk.Frame):

    logger = logging.getLogger('App.Console')

    def __init__(self, event_broker: EventBroker, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_broker = event_broker
        self.event_subscriber = EventSubscriber(event_broker)
        self.event_publisher = EventPublisher(event_broker)

        # ==================== INITIALIZE CONSOLE CONTAINER ==================== #

        self.config(relief=tk.RAISED, borderwidth=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_propagate(False)
        


        # ==================== INITIALIZE CONSOLE OPTIONS ==================== #

        self.button_frame = ttk.Frame(self)
        self.pack_propagate(False)

        self.clear_text_button = ttk.Button(self.button_frame, 
                                            text='Clear', 
                                            command=self.on_clear_text)
        
        self.save_text_button = ttk.Button(self.button_frame, 
                                           text='Save', 
                                           command=self.on_save_text)
        
        self.close_tab_button = ttk.Button(self.button_frame, 
                                           text='Close', 
                                           command=self.on_close_tab)
        
        self.add_tab_button = ttk.Button(self.button_frame,
                                        text='Add',
                                        command=self.on_add_tab)

        self.clear_text_button.pack(fill=tk.Y, padx=5, pady=5)
        self.save_text_button.pack(fill=tk.Y, padx=5, pady=5)
        self.close_tab_button.pack(fill=tk.Y, padx=5, pady=5)
        self.add_tab_button.pack(fill=tk.Y, padx=5, pady=5)


        # ==================== INITIALIZE CONSOLE TEXT ==================== #

        self.console_notebook = ttk.Notebook(self)
        self.console_notebook.grid_columnconfigure(0, weight=10)
        self.console_notebook.grid_columnconfigure(1, weight=1)
        self.console_notebook.grid_rowconfigure(0, weight=1)
        self.console_notebook.grid_rowconfigure(1, weight=10)

        self.filter_frame = ttk.Frame(self.console_notebook)
        self.filter_frame.grid(row=0, column=1, sticky=tk.NSEW)
    
        self.filter_name = tk.StringVar()
        self.filter_level = tk.StringVar()

        self.filter_name_options = [log_name for log_name in logging.Logger.manager.loggerDict.keys()]
        self.filter_name_options.sort()
        self.filter_name_options.insert(0, '[Show All]')
        self.filter_level_options = logging._levelToName.values()

        self.filter_name_menu = ttk.OptionMenu(self.filter_frame, 
                                          self.filter_name, 
                                          'Log Name', 
                                            command=self.on_log_name_filter,
                                          *self.filter_name_options)
        
        self.log_level_menu = ttk.OptionMenu(self.filter_frame, 
                                           self.filter_level, 
                                           'Log Level', 
                                            command=self.on_log_level_filter,
                                           *self.filter_level_options)
        
        self.log_level_menu.grid(row=0, column=1, sticky='nsew')
        self.filter_name_menu.grid(row=0, column=2, sticky='nsew')

        self.on_add_tab()

        # ==================== WIDGET LAYOUT ==================== #

        self.console_notebook.grid(row=0, column=0, sticky=tk.NSEW)
        self.button_frame.grid(row=0, column=1, sticky=tk.NSEW)

        self.console_notebook.bind('<<NotebookTabChanged>>', self.on_change_tab)



    def get_current_tab(self) -> ConsoleTab | None:
        current_tab = self.console_notebook.select()
        current_tab = self.console_notebook.nametowidget(current_tab)

        if isinstance(current_tab, ConsoleTab):
            return current_tab

        return None

    def on_clear_text(self):
        current_tab = self.get_current_tab()

        if current_tab:
            current_tab.on_clear()
    
    def on_close_tab(self):
        current_tab = self.get_current_tab()

        if current_tab:
            current_tab.on_close()
        

    def on_save_text(self):
        current_tab = self.get_current_tab()

        if current_tab:
            current_tab.on_save()

    def get_current_logger(self) -> ConsoleLogger | None:
        current_tab = self.console_notebook.select()
        current_tab = self.console_notebook.nametowidget(current_tab)

        if isinstance(current_tab, ConsoleLogger):
            return current_tab

        return None

    def on_change_tab(self, event):
        current_tab = self.get_current_tab()

        if isinstance(current_tab, ConsoleLogger):
            self.filter_name.set(current_tab.log_name)
            self.filter_level.set(current_tab.log_level)

    def on_add_tab(self):
        num_tabs = self.console_notebook.index('end')
        tab_name = f'Tab {num_tabs + 1}'

        console_tab = ConsoleLogger(master=self.console_notebook,
                                    event_broker=self.event_broker)
        console_tab.grid(row=1, column=0, sticky=tk.NSEW)
        self.console_notebook.add(console_tab, text=tab_name)

    def on_log_name_filter(self, log_name):
        current_logger = self.get_current_logger()

        if isinstance(current_logger, ConsoleLogger):
            if log_name == '[All]':
                log_name = None

            current_logger.on_log_name_filter(log_name)

    def on_log_level_filter(self, log_level):
        current_logger = self.get_current_logger()

        if isinstance(current_logger, ConsoleLogger):
            current_logger.on_log_level_filter(log_level)