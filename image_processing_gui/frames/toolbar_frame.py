import logging
import tkinter as tk
from tkinter import ttk
import os
import sys

from ..assets_dictionary import image_assets

from ..events.event_constants import *
from ..events.event_broker import EventBroker
from ..events.event_publisher import EventPublisher
from ..events.event_subscriber import EventSubscriber

class ToolbarFrame(ttk.Frame):
    def __init__(self, master, event_broker: EventBroker, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        # if getattr(sys, 'frozen', False):
        #     # If the application is running in a PyInstaller bundle
        #     currentdir = sys._MEIPASS
        # else:
        #     # If the application is running in a normal Python environment
        #     currentdir = os.path.join(os.getcwd(), __file__)

        # assets_dir = os.path.join(currentdir, 'assets')

        # # get data file from spec
        # start_icon_dir = os.path.join(assets_dir, 'play-circle.png')
        # pause_icon_dir = os.path.join(assets_dir, 'pause-circle.png')
        # close_icon_dir = os.path.join(assets_dir, 'stop-circle.png')


        self.logger = logging.getLogger(__name__)

        self.config(relief=tk.SOLID, borderwidth=2)

        self.start_icon = tk.PhotoImage(file=image_assets['play_icon'])
        self.stop_icon = tk.PhotoImage(file=image_assets['pause_icon'])
        self.close_icon = tk.PhotoImage(file=image_assets['close_icon'])

        # put image on frame

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=100)

        self.rowconfigure(0, weight=1)

        self.play_button = ttk.Button(self, image=self.start_icon, command=self.on_play)
        self.pause_button = ttk.Button(self, image=self.stop_icon, command=self.on_pause)
        self.close_button = ttk.Button(self, image=self.close_icon, command=self.on_close)

        self.play_button.grid(row=0, column=0, sticky=tk.NSEW)
        self.pause_button.grid(row=0, column=1, sticky=tk.NSEW)
        self.close_button.grid(row=0, column=2, sticky=tk.NSEW)

        self.event_broker = event_broker
        self.event_subscriber = EventSubscriber(self.event_broker)
        self.event_publisher = EventPublisher(self.event_broker)

        self.event_subscriber.subscribe(DisplayEvent.START, self.on_start)

        self.set_button_state(tk.DISABLED)

    def set_button_state(self, state):
        self.play_button.config(state=state)
        self.pause_button.config(state=state)
        self.close_button.config(state=state)

    def on_start(self, event=''):
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.close_button.config(state=tk.NORMAL)

        self.logger.debug('Start button clicked')

    def on_play(self, event=''):
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)

        self.event_publisher.publish(DisplayEvent.PLAY)

    def on_pause(self, event=''):
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

        self.event_publisher.publish(DisplayEvent.PAUSE)

    def on_close(self, event=''):
        self.logger.debug('Closing display')
        self.set_button_state(tk.DISABLED)
        self.event_publisher.publish(DisplayEvent.CLOSE)
