import logging
import tkinter as tk
from tkinter import ttk

from ..events.event_constants import *
from ..events.event_broker import EventBroker
from ..events.event_subscriber import EventSubscriber
from ..events.event_publisher import EventPublisher


class PopupFrame(tk.Toplevel):
    def __init__(self, master, event_broker: EventBroker, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.event_broker = event_broker
        self.event_subscriber = EventSubscriber(self.event_broker)
        self.event_publisher = EventPublisher(self.event_broker)

        self.logger = logging.getLogger(__name__)

        self.title('Popup')
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.destroy)


class EntryPopup(PopupFrame):
    def __init__(self, master, event_broker: EventBroker, *args, **kwargs):
        super().__init__(master, event_broker, *args, **kwargs)

        self.entry_frame = ttk.Frame(self)
        self.entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.entry = ttk.Entry(self.entry_frame)
        self.entry.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ok_button = ttk.Button(self.button_frame, text='OK', command=self.on_ok)
        self.cancel_button = ttk.Button(self.button_frame, text='Cancel', command=self.on_cancel)

        self.ok_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.cancel_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
