import logging
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk

from ..events.event_constants import *
from ..events.event_broker import EventBroker
from ..events.event_subscriber import EventSubscriber
from ..events.event_publisher import EventPublisher


class SidebarTab(ttk.Frame, ABC):
    def __init__(self, master, event_broker: EventBroker, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.event_broker = event_broker

        

    @abstractmethod
    def on_apply(self, event=''):
        pass

    @abstractmethod
    def on_revert(self, event=''):
        pass

    @abstractmethod
    def on_reset(self, event=''):
        pass

    @abstractmethod
    def on_show(self, event=''):
        pass




class SidebarFrame(ttk.Frame):

    logger = logging.getLogger(__name__)


    def __init__(self, master, event_broker: EventBroker, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.event_broker = event_broker
        self.event_publisher = EventPublisher(event_broker)
        self.event_subscriber = EventSubscriber(event_broker)
        

        # ==================== INITIALIZE SIDEBAR ==================== #

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid_propagate(False)
        
        # ==================== INITIALIZE MAIN FRAME ==================== #

        self.sidebar_notebook = ttk.Notebook(self)
        self.sidebar_notebook.columnconfigure(0, weight=1)
        self.sidebar_notebook.rowconfigure(0, weight=1)
        
        # ==================== INITIALIZE BUTTON FRAME ==================== #

        self.button_frame = ttk.Frame(self)
        self.button_frame.config(relief=tk.RAISED, borderwidth=2)
        
        self.apply_button = ttk.Button(self.button_frame, text='Apply', command=self.on_apply)
        self.revert_button = ttk.Button(self.button_frame, text='Revert', command=self.on_revert)
        self.reset_button = ttk.Button(self.button_frame, text='Reset', command=self.on_reset)
        self.show_button = ttk.Button(self.button_frame, text='Show', command=self.on_show)

        self.apply_button.pack(side=tk.LEFT)
        self.revert_button.pack(side=tk.LEFT)
        self.reset_button.pack(side=tk.LEFT)
        self.show_button.pack(side=tk.LEFT)

        # ==================== GRID LAYOUT ==================== #

        self.sidebar_notebook.grid(row=0, column=0, sticky=tk.NSEW)
        self.button_frame.grid(row=1, column=0, sticky=tk.NSEW)

        # self.event_subscriber.subscribe(SidebarEvent.TOGGLE_APPLY_BUTTON, lambda event, state: self.apply_button.config(state=state))
        # self.event_subscriber.subscribe(SidebarEvent.TOGGLE_REVERT_BUTTON, lambda event, state: self.revert_button.config(state=state))
        # self.event_subscriber.subscribe(SidebarEvent.TOGGLE_RESET_BUTTON, lambda event, state: self.reset_button.config(state=state))
        # self.event_subscriber.subscribe(SidebarEvent.TOGGLE_SHOW_BUTTON, lambda event, state: self.show_button.config(state=state))

        # self.event_subscriber.subscribe(SidebarEvent.TOGGLE_ALL_BUTTONS, lambda event, state: self.set_button_state(state))

        # self.set_button_state(tk.DISABLED)



    def set_button_state(self, state):
        self.apply_button.config(state=state)
        self.revert_button.config(state=state)
        self.show_button.config(state=state)

    def add_sidebar(self, title: str, sidebar_class: type):
        try:
            if not issubclass(sidebar_class, SidebarTab):
                raise TypeError(f'Class {sidebar_class} is not a subclass of SidebarTab')
            
            sidebar = sidebar_class(master=self.sidebar_notebook, event_broker=self.event_broker)
            sidebar.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.sidebar_notebook.add(sidebar, text=title)

        except TypeError as err:
            self.logger.error(err)
            self.logger.error(err)

    # def enable_eye_tracker_mode(self):
    #     self.set_button_state(tk.DISABLED)

    #     self.event_publisher.publish(SidebarEvent.ENABLE_EYE_MODE, True)

    def get_current_sidebar(self):
        current_sidebar = self.sidebar_notebook.select()
        current_sidebar = self.sidebar_notebook.nametowidget(current_sidebar)

        if isinstance(current_sidebar, SidebarTab):
            return current_sidebar
        
        return None

    
    def on_apply(self):
        current_sidebar = self.get_current_sidebar()

        if current_sidebar:
            current_sidebar.on_apply()

    def on_revert(self):
        current_sidebar = self.get_current_sidebar()

        if current_sidebar:
            current_sidebar.on_revert()


    def on_reset(self):
        current_sidebar = self.get_current_sidebar()

        if current_sidebar:
            current_sidebar.on_reset()

    def on_show(self):
        current_sidebar = self.get_current_sidebar()

        if current_sidebar:
            current_sidebar.on_show()



