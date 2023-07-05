import logging

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


from .console_tab import ConsoleTab
from ..events.event_constants import *
from ..events.event_broker import EventBroker
from ..events.event_subscriber import EventSubscriber
from ..events.event_publisher import EventPublisher


class ConsoleLogHandler(logging.Handler):
    def __init__(self, output_widget):
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s - line %(lineno)d, in %(funcName)s',
                           datefmt='%H:%M:%S'))
        self.output_widget = output_widget
        self.output_widget.config(state='disabled')
        

    def emit(self, record):
        self.output_widget.config(state='normal')
        self.output_widget.insert(tk.END, self.format(record) + "\n")
        self.output_widget.see(tk.END)
        self.output_widget.config(state='disabled')




class ConsoleLogger(ConsoleTab, tk.Text):

    log_initialdir = '.'

    def __init__(self, event_broker: EventBroker, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing console logger...")

        self.event_broker = event_broker
        self.event_subscriber = EventSubscriber(event_broker)
        self.event_publisher = EventPublisher(event_broker)

        self.log_name = '[Show All]'
        self.log_level = 'DEBUG'

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)

        self.filter_frame = ttk.Frame(self)

        self.filter_frame.grid_columnconfigure(0, weight=10)
        self.filter_frame.grid_columnconfigure(1, weight=1)
        self.filter_frame.grid_columnconfigure(2, weight=1)
        self.filter_frame.grid_rowconfigure(0, weight=1)

        # ========== Configure Text Widget ========== #

        self.config(state='disabled')
        self.config(font=("consolas", 10), wrap='word')

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.config(yscrollcommand=self.scrollbar.set)

        self.grid(row=1, column=0, columnspan=2, sticky='nsew')


        # ========== Configure Logging Handler ========== #

        self.log_handler = ConsoleLogHandler(self)
        logging.getLogger().addHandler(self.log_handler)

        self.logger.info("Console logger initialized successfully.")

    def on_log_name_filter(self, filter_name):
        self.log_name = filter_name
        self.logger.info(f"Setting log name filter to {filter_name}")
        self.log_handler.filters.clear()
        filter = logging.Filter(filter_name)
        self.log_handler.addFilter(filter)

    def on_log_level_filter(self, level):
        self.log_level = level
        self.logger.info(f"Setting log level to {level}")
        logging.getLogger().setLevel(level)

    def on_save(self):
        self.logger.info('Saving log file...')
        
        file_path = filedialog.asksaveasfilename(defaultextension='.log', 
                                                 initialdir=self.log_initialdir)
        if not file_path:
            self.logger.info('Log file save cancelled.')
            return False
        
        try:
            with open(file_path, 'w') as file:
                file.write(self.get('1.0', tk.END))

            self.logger.info(f"Log file saved to {file_path}")

        except Exception as err:
            self.logger.error(f"Error saving log file: {err}")
            return False

        return True

    def on_clear(self):
        self.config(state='normal')
        self.delete('1.0', tk.END)
        self.config(state='disabled')

    def on_close(self):
        logging.getLogger().removeHandler(self.log_handler)
        self.log_handler.close()
        self.destroy()

