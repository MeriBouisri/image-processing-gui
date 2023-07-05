import logging
import cv2
import threading
import multiprocessing
from .image_reader import ImageReader

from .image_processor import ImageProcessor, DummyImageProcessor

from ..events.event_constants import *
from ..events.event_broker import EventBroker
from ..events.event_subscriber import EventSubscriber
from ..events.event_publisher import EventPublisher

import queue

import numpy as np

from PIL import Image, ImageTk


class ImageDisplayer:

    def __init__(self, display_queue: queue.Queue, reader: ImageReader = None):
        self.logger = logging.getLogger(__name__)

        self.display_queue = display_queue

        self.reader = reader
        self.previous_processor = None
        self.previous_preprocessor = None

    def set_reader(self, reader: ImageReader):
        self.reader = reader


    def is_empty(self):
        return self.reader is None

    def stop(self):
        if not self.is_empty():
            self.reader.stop()

    def pause(self):
        if not self.is_empty():
            self.reader.pause()


    def display(self, processor = None, preprocessor = None) -> Image:

        if self.reader is None:
            return None
        
        if not self.reader.ready():
            return None
        
        image = self.reader.read()

        if image is None:
            return None
        
        # ========== Calling pre-processors ========== #

        if preprocessor is not None:
            image = preprocessor.process(image)
            self.previous_preprocessor = preprocessor

        else:
            if self.previous_preprocessor is not None:
                image = self.previous_preprocessor.process(image)

        # ========== Calling main processor ========== #
        
        if processor is not None:
            self.previous_processor = processor

        else:
            if self.previous_processor is not None:
                processor = self.previous_processor
            else:
                processor = DummyImageProcessor()

        # ========== Processing image ========== #

        image = processor.process(image) # type: ignore

        if image is None:
            return None
        
        
        cv_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)

        self.display_queue.put(pil_image)

class EyeTrackerImageDisplayer(ImageDisplayer):
    def __init__(self, display_queue: queue.Queue, reader: ImageReader = None):
        super().__init__(display_queue, reader)

        self.previous_processor = DummyImageProcessor()

    

# class ImageDisplayer:

#     logger = logging.getLogger(__name__)

#     def __init__(self, display_queue: queue.Queue, reader: Reader):
#         self.reader = reader

#         self.display_queue = display_queue
#         self.last_processor = None
#         self.last_preprocessor = None

#     def stop(self):
#         self.reader.stop()

#     def display(self, processor = None, preprocessor = None) -> Image:
#         if self.reader.ready():
#             image = self.reader.read()

#             if image is None:
#                 return None
            
#             if processor is None:
#                 if self.last_processor is None:
#                     processor = DummyImageProcessor()
#                 else:
#                     processor = self.last_processor

#             if preprocessor is not None:
#                 image = preprocessor.process(image)
#                 self.last_preprocessor = preprocessor
        
#             else:
#                 if self.last_preprocessor is not None:
#                     image = self.last_preprocessor.process(image)
                
            
#             image = processor.process(image) # type: ignore
#             self.last_processor = processor

#             if image is None:
#                 self.logger.error("Unable to process image")
#                 return None
            
#             cv_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             cv_image = Image.fromarray(cv_image)

#             self.display_queue.put(cv_image)