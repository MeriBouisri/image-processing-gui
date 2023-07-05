import logging
import tkinter as tk
from tkinter import ttk
from queue import Queue

from ..image_system.image_reader import ImageReader, StaticImageReader, StaticImageFileReader, DynamicImageReader

from .image_canvas import ImageCanvas, MainImageCanvas, SideImageCanvas

from .toolbar_frame import ToolbarFrame

from ..events.event_constants import *
from ..events.event_broker import EventBroker
from ..events.event_subscriber import EventSubscriber
from ..events.event_publisher import EventPublisher

class ReaderManager:

    MAX_READER_LIST = 3

    logger = logging.getLogger(__name__)

    def __init__(self, event_broker: EventBroker):
        self.main_reader = None
        self.reader_list = []

        self.event_broker = event_broker
        self.event_publisher = EventPublisher(event_broker)
        self.event_subscriber = EventSubscriber(event_broker)

        # self.event_subscriber.subscribe(DisplayEvent.SELECT, self.on_select)

    def add_reader(self, reader: ImageReader):
        if not self.main_reader:
            self.main_reader = reader
            return

        if len(self.reader_list) < self.MAX_READER_LIST:
            self.reader_list.append(reader)
            return
        
        self.logger.warning(f'Reader list is full. Delete an image canvas to add a new reader.')

    def remove_reader(self, reader: ImageReader):
        if self.main_reader == reader:
            self.main_reader = None
            return

        if reader in self.reader_list:
            self.reader_list.remove(reader)
            return

        self.logger.warning(f'Reader not found.')





    def get_reader_at_index(self, index: int):
        try:
            return self.reader_list[index]
        except IndexError:
            return None

    def set_main_reader(self, reader: ImageReader):
        try:
            new_reader_index = self.reader_list.index(reader)
            new_reader = self.reader_list.pop(new_reader_index)
            previous_reader = self.main_reader
            self.main_reader = new_reader
            self.reader_list.insert(new_reader_index, previous_reader)

        except ValueError:
            self.logger.warning(f'Unable to find reader in reader list.')

        except IndexError:
            self.logger.warning(f'Unable to insert more readers. Delete a canvas to proceed.')

    

class DisplayFrame(ttk.Frame):

    logger = logging.getLogger(__name__)

    def __init__(self, master, event_broker: EventBroker, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.reader_manager = ReaderManager(event_broker=event_broker)

        # ==================== Event System ==================== #

        self.event_broker = event_broker
        self.event_subscriber = EventSubscriber(self.event_broker)
        self.event_publisher = EventPublisher(self.event_broker)

        # ==================== Widgets ==================== #

        self.config(relief=tk.SOLID, borderwidth=2)
        self.grid_propagate(False)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=150)
        
        # ========== Toolbar Frame ========== #

        self.toolbar = ToolbarFrame(self, self.event_broker)

        # ========== Display Frames ========== #

        self.main_display = ttk.Frame(self)
        self.side_display = ttk.Frame(self)

        self.main_display.config(relief=tk.SOLID, borderwidth=1)
        self.side_display.config(relief=tk.SOLID, borderwidth=1)

        self.main_display.columnconfigure(0, weight=1)
        self.main_display.rowconfigure(0, weight=1)
        self.main_display.grid_propagate(False)

        self.side_display.columnconfigure(0, weight=1)
        self.side_display.rowconfigure(0, weight=1)
        self.side_display.rowconfigure(1, weight=1)
        self.side_display.rowconfigure(2, weight=1)
        self.side_display.grid_propagate(False)

        # ==================== Empty Image Canvas ==================== #

        self.main_display_layout = {'row': 1, 'column': 0, 'columnspan': 1}
        self.side_display_layout = {'row': 1, 'column': 1, 'columnspan': 1}

        self.main_canvas = MainImageCanvas(self.main_display, self.event_broker)

        self.side_canvas_1 = SideImageCanvas(self.side_display, self.event_broker)
        self.side_canvas_2 = SideImageCanvas(self.side_display, self.event_broker)
        self.side_canvas_3 = SideImageCanvas(self.side_display, self.event_broker)

        self.main_canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.side_canvas_1.grid(row=0, column=0, sticky=tk.NSEW)
        self.side_canvas_2.grid(row=1, column=0, sticky=tk.NSEW)
        self.side_canvas_3.grid(row=2, column=0, sticky=tk.NSEW)
        
        # ========== Grid Layout ========== #

        self.toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
        self.main_display.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
        self.side_display.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)

        # ==================== Event Bindings ==================== #

        self.event_subscriber.subscribe(MenuEvent.OPEN_IMAGE, self.on_open_image)
        self.event_subscriber.subscribe(MenuEvent.OPEN_WEBCAM, self.on_open_webcam)

        self.event_subscriber.subscribe(ToolbarEvent.CLOSE, self.on_close)
        self.event_subscriber.subscribe(ToolbarEvent.PLAY, self.on_play)
        self.event_subscriber.subscribe(ToolbarEvent.PAUSE, self.on_pause)

        self.event_subscriber.subscribe(DisplayEvent.CLOSE, self.on_close_display)
        self.event_subscriber.subscribe(DisplayEvent.SELECT, self.on_select_display)
        # self.event_subscriber.subscribe(DisplayEvent.EYE_TRACKER_MODE, self.on_eye_tracker_mode)

        self.event_subscriber.subscribe(MenuEvent.TOGGLE_SIDE_DISPLAY, self.on_toggle_side_display)
        

    def on_close(self, event):
        for child in self.main_display.winfo_children():
            if isinstance(child, ImageCanvas):
                child.on_close(event)
        
    def on_play(self, event):
        for child in self.main_display.winfo_children():
            if isinstance(child, ImageCanvas):
                child.is_running = True

        self.event_publisher.publish(RequestEvent.REQUEST_PROCESSOR_UPDATE)

    def on_pause(self, event):
        for child in self.main_display.winfo_children():
            if isinstance(child, ImageCanvas):
                child.is_running = False


    def on_open_image(self, event, filename):

        self.logger.info(f'Opening image : {filename}')

        image_reader = StaticImageFileReader(filename)
        self.event_publisher.publish(DisplayEvent.START)
        
        if self.main_canvas.is_empty():
            self.main_canvas.set_reader(image_reader)
            self.reader_manager.add_reader(image_reader)
            return
        
        for side_canvas in self.side_display.winfo_children():
            if isinstance(side_canvas, ImageCanvas):
                if side_canvas.is_empty():
                    side_canvas.set_reader(image_reader)
                    self.reader_manager.add_reader(image_reader)
                    side_canvas.set_selectable(True)
                    return
                
                
    def on_open_webcam(self, event):
        self.logger.info('Opening webcam')

        webcam_reader = DynamicImageReader()
        self.event_publisher.publish(DisplayEvent.START)
        

        if self.main_canvas.is_empty():
            self.main_canvas.set_reader(webcam_reader)
            self.reader_manager.add_reader(webcam_reader)
            return
        
        for side_canvas in self.side_display.winfo_children():
            if isinstance(side_canvas, ImageCanvas):
                if side_canvas.is_empty():
                    side_canvas.set_reader(webcam_reader)
                    self.reader_manager.add_reader(webcam_reader)
                    side_canvas.set_selectable(True)
                    return
                
    def on_toggle_side_display(self, event, state: bool):
        main_display_layout = self.main_display_layout.copy()

        if state:
            self.side_display.grid()
            main_display_layout['columnspan'] = 1 

        else:
            for side_canvas in self.side_display.winfo_children():
                if isinstance(side_canvas, ImageCanvas):
                    side_canvas.set_selectable(False)

            self.side_display.grid_remove()
            main_display_layout['columnspan'] = 2

        self.main_display.grid(**main_display_layout)

                
    
    def update_display_layout(self):
        self.main_canvas.set_reader(self.reader_manager.main_reader)

        for i, side_canvas in enumerate(self.side_display.winfo_children()):
            if isinstance(side_canvas, ImageCanvas):
                reader = self.reader_manager.get_reader_at_index(i)
                
                if reader is None:
                    side_canvas.set_selectable(False)
                    continue

                side_canvas.set_reader(reader)
        

    def on_select_display(self, event, reader: ImageReader):
        self.reader_manager.set_main_reader(reader)
        self.update_display_layout()

    def on_close_display(self, event):
        self.main_canvas.on_close(event)
        self.side_canvas_1.on_close(event)
        self.side_canvas_2.on_close(event)
        self.side_canvas_3.on_close(event)




        



