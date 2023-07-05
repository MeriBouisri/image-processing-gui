import logging
from abc import ABC, abstractmethod
import cv2
import threading
import queue
import time


class ImageReader(ABC):

    @property
    @abstractmethod
    def is_ready(self):
        pass

    @property
    @abstractmethod
    def source(self):
        pass

    def ready(self):
        return self.is_ready

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def pause(self):
        pass

class StaticImageReader(ImageReader):
    """
    Read image from direct source. (e.g. numpy array)
    """
    
    logger = logging.getLogger(__name__)

    def __init__(self, source):
        self._source = source
        self._is_ready = True

    @property
    def is_ready(self):
        return self._is_ready
    
    @is_ready.setter
    def is_ready(self, value):
        self._is_ready = value

    
    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, value):
        self._source = value

    def read(self):
        if self._is_ready:
            return self.source

    def stop(self):
        self._is_ready = False

    def pause(self):
        self._is_ready = False
    
class StaticImageFileReader(StaticImageReader):
    """
    Read image from filename source.
    """
    
    logger = logging.getLogger(__name__)

    def __init__(self, source):
        try:
            self._source = cv2.imread(source)
        except Exception as e:
            self.logger.error(f"Unable to read image from source: {source}")
            self.logger.error(e)
            self._is_ready = False
            return
        
        self._is_ready = True


class DynamicImageReader(ImageReader):
    """
    Read image from a video source (dynamic as in, the current image is constantly changing)
    """

    logger = logging.getLogger(__name__)

    def __init__(self, source=0):
        self._is_ready = False
        self._source = cv2.VideoCapture(source)

        if not self.source.isOpened():
            self.logger.error(f"Unable to read from source: {source}")
            return None

        self._is_ready = True

    @property
    def is_ready(self):
        return self._is_ready
    
    @is_ready.setter
    def is_ready(self, value):
        self._is_ready = value

    
    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, value):
        self._source = value

    def read(self):
        if self._is_ready:
            ret, frame = self._source.read()

            if ret:
                return frame

    def stop(self):
        self._is_ready = False
        self._source.release()

    def pause(self):
        self._is_ready = False

