import logging
import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from .opencv_data import opencv_data
from .opencv_process_panel import OpenCVProcessPanel
from ...image_system.image_processor import ImageProcessorSequenceList, ImageProcessorSequenceSet


from ...frames.sidebar_frame import SidebarTab

from ...events.event_constants import *
from ...events.event_broker import EventBroker
from ...events.event_subscriber import EventSubscriber
from ...events.event_publisher import EventPublisher


class OpenCVSidebar(SidebarTab):

    logger = logging.getLogger(__name__)

    def __init__(self, master, event_broker: EventBroker, *args, **kwargs):
        super().__init__(master=master, event_broker=event_broker, *args, **kwargs)

        self.processor_function_set = ImageProcessorSequenceSet()
        self.preprocessor_list = ImageProcessorSequenceList()

        self.event_publisher = EventPublisher(self.event_broker)
        self.event_subscriber = EventSubscriber(self.event_broker)

        self.columnconfigure(0, weight=1)

        for i, (process_key, process_value) in enumerate(opencv_data.items()):

            # if process_value['status'] == 0:
            #     continue

            process_panel = OpenCVProcessPanel(self, self.event_broker, process_key, process_value)
            self.rowconfigure(i, weight=len(process_panel.winfo_children()) - 1)

            process_panel.grid(row=i, column=0, sticky=tk.NSEW, padx=5, pady=5)



        self.event_subscriber.subscribe(ImageProcessingEvent.UPDATE_PROCESS, self.on_update_process)

        




    def on_update_process(self, event, process):
        self.processor_function_set.add(process)
        self.event_publisher.publish(ImageProcessingEvent.APPLY_PROCESS, 
                                     processor=self.processor_function_set, 
                                     preprocessor=self.preprocessor_list) 
        
        # self.event_publisher.publish(SidebarEvent.TOGGLE_APPLY_BUTTON, state=tk.NORMAL)
        # self.event_publisher.publish(SidebarEvent.TOGGLE_RESET_BUTTON, state=tk.NORMAL)

    def on_apply(self, event=''):
        """
        Return whether the on_revert button should be enabled.
        """
        self.preprocessor_list.add(self.processor_function_set)
        self.reset_all()


    def on_revert(self, event=''):
        if len(self.preprocessor_list) == 0:
            return
        
        self.preprocessor_list.pop()

        self.reset_all()

    def on_reset(self, event=''):
        self.logger.debug('Resetting process')
        self.preprocessor_list.clear()
        self.processor_function_set.clear()
        self.reset_all()


    def on_show(self, event=''):
        self.event_publisher.publish(GlobalEvent.PAUSE)

        self.logger.debug('Saving process')
        self.reset_all()
        self.event_publisher.publish(GlobalEvent.RESUME)

    def reset_all(self):
        for process_panel in self.winfo_children():
            process_panel.reset()

        # self.event_publisher.publish(SidebarEvent.TOGGLE_ALL_BUTTONS, state=tk.DISABLED)
    










    




