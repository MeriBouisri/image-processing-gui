import logging
from typing import MutableSequence, TypeGuard
from queue import Queue, Empty
from abc import ABC, abstractmethod
import cv2
import numpy as np
import heapq
import sortedcontainers
import numpy as np




class ImageProcessor(ABC):
    @property
    @abstractmethod
    def priority(self):
        pass

    @property
    @abstractmethod
    def enabled(self):
        pass

    @abstractmethod
    def process(self, target):
        pass

    @abstractmethod
    def compare_to(self, __value: object) -> bool:
        """
        Compare whether the contents of the processor are the same as another.
        """
        pass

    @abstractmethod
    def serialize(self) -> tuple:
        """
        This method should return a tuple of the following : (serialized_processor, processor.__class__)
        Return the class where the processor is defined is necessary for deserialization afterwards.
        """
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, serialized_processor):
        pass
    

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, ImageProcessor):
            return False
        
        return self.priority < __value.priority
    
    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, ImageProcessor):
            return False
        
        return self.priority > __value.priority
    
    def copy(self):
        serialized_data = self.serialize()[1]
        return self.__class__.deserialize(serialized_data)
    
    def __str__(self):
        return str(self.serialize())


class DummyImageProcessor(ImageProcessor):
    def __init__(self, priority=0, enabled=True):
        self._priority = priority
        self._enabled = enabled

    @property
    def priority(self):
        return self._priority

    @property
    def enabled(self):
        return self._enabled


    def compare_to(self, __value: object) -> bool:
        return isinstance(__value, DummyImageProcessor)
    
    def process(self, target):
        return target
    
    def serialize(self):
        return self.__class__, None
    
    @classmethod
    def deserialize(cls, serialized_processor):
        pass


    

class ImageProcessorFunction(ImageProcessor):

    _supported_attributes = ['enabled', 'priority', 'name', 'callback', 'source_keyword', 'argument_dict']

    def __init__(self, 
                 name=None, 
                 callback=None, 
                 source_keyword=None, 
                 return_index=-1, 
                 enabled=False, 
                 priority=0, 
                 **kwargs):
        """
        Parameters
        ----------
        name : str
            The name of the function. Must be unique.

        callback : function
            The function to be called. Must accept a keyword argument with the name of source_keyword.

        source_keyword : str
            The name of the keyword argument used to pass the image to the callback function.

        return_index : int, optional = -1
            The return_index is used in the case of functions returning a tuple of values. If that is the case,
            overwrite the default value of return_index to specify the position of the returned image.


        enabled : bool, optional = False
            If True, the function will be applied to the image.

        priority : int, optional = 0
            The priority of the function. Functions with higher priority will be applied first.

        """
        self.logger = logging.getLogger(__name__)

        self._enabled = enabled
        self._priority = priority

        self.name = name
        self.callback = callback
        self.source_keyword = source_keyword
        self.return_index = return_index
        self.argument_dict = kwargs

    @property
    def priority(self):
        return self._priority
    
    @priority.setter
    def priority(self, value: int):
        self._priority = value

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    def __hash__(self):
        return hash(self.name)
    
    def compare_to(self, __value: object) -> bool:
        if not isinstance(__value, ImageProcessorFunction):
            return False
        
        other_argument_dict = __value.argument_dict

        for arg in self.argument_dict:
            if arg not in other_argument_dict:
                return False
            
            if self.argument_dict[arg] != other_argument_dict[arg]:
                return False
        
        return True

    def add_argument(self, **kwargs):
        self.argument_dict.update(kwargs)

    def process(self, target):
        if not self.enabled or self.callback is None: 
            return target
        
        process_attempt = 0

        while process_attempt < 1:
            try:
                source_argument = {self.source_keyword: target}

                target = self.callback(**source_argument, **self.argument_dict)

                if isinstance(target, tuple):
                    if self.return_index is not None:
                        return target[self.return_index]
                    
                    return target[0]

                return target

            except cv2.error as e:
                target = cv2.normalize(target, None, 0, 255, cv2.NORM_MINMAX) # type: ignore
                process_attempt += 1

        return target
    
    def serialize(self):
        serialized_processor_data = {}

        for attribute in self._supported_attributes:
            try:
                serialized_processor_data[attribute] = getattr(self, attribute)
            except (AttributeError, KeyError, TypeError) as err:
                continue

        return self.__class__, serialized_processor_data
    
    @classmethod
    def deserialize(cls, serialized_data):
        new_processor = cls()

        for attribute in ImageProcessorFunction._supported_attributes:
            try:
                new_processor.__setattr__(attribute, serialized_data[attribute])
            except KeyError:
                continue

        return new_processor
    
    def __eq__(self, __value: object) -> bool:
        """
        Two ImageProcessorFunction objects are equal if they have the same name attribute.
        """
        if not isinstance(__value, ImageProcessorFunction):
            return False
        
        return self.name == __value.name
    
class ImageProcessorSequence(ImageProcessor, ABC):
    @property
    @abstractmethod
    def processor_sequence(self):
        pass

    @abstractmethod
    def add(self, processor: ImageProcessor):
        pass

    @abstractmethod
    def discard(self, processor: ImageProcessor):
        pass

    @abstractmethod
    def pop(self, processor: ImageProcessor):
        pass

    @abstractmethod
    def clear(self):
        pass

    def process(self, target):
        if len(self.processor_sequence) == 0:
            return target
        
        for processor in self.processor_sequence:
            try:
                target = processor.process(target)
            except Exception as e:
                continue
        return target

    def serialize(self):
        return self.__class__, [processor.serialize() for processor in self.processor_sequence]
    
    @classmethod
    def deserialize(cls, serialized_processor):
        new_processor_sequence = cls()
        
        for serialized_class, serialized_data in serialized_processor:
            new_processor = serialized_class.deserialize(serialized_data)
            new_processor_sequence.add(new_processor)

        return new_processor_sequence
    
    def compare_to(self, __value: object) -> bool:
        if not isinstance(__value, ImageProcessorSequence):
            return False
        
        if __value.processor_sequence is None:
            return False
        
        if len(self.processor_sequence) != len(__value.processor_sequence):
            return False

        for i, processor in enumerate(self.processor_sequence):
            equal = processor.compare_to(__value.processor_sequence[i])
            if not equal:
                return False
        
        return True
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return False
        
        return self.compare_to(__value)
    
    def __len__(self):
        return len(self.processor_sequence)


class ImageProcessorSequenceSet(ImageProcessorSequence):
    """
    A sequence of ImageProcessorFunction objects. The sequence is sorted by priority.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, priority=0, enabled=True):
        self._priority = priority
        self._enabled = enabled
        self._processor_sequence = sortedcontainers.SortedSet()

    @property
    def processor_sequence(self):
        return self._processor_sequence
    
    @property
    def priority(self):
        return self._priority
    
    @property
    def enabled(self):
        return self._enabled

    def add(self, processor: ImageProcessor):
        if processor.enabled:
            self._processor_sequence.add(processor.copy())
            return
        
        self.discard(processor)

    def discard(self, processor: ImageProcessor):
        self._processor_sequence.discard(processor)

    def pop(self, index: int = -1):
        """
        Return and remove the processor at the specified index. If no index is specified, return and remove the last processor.
        If the index is out of range, return None.
        """
        try:
            return self._processor_sequence.pop(index)
        except IndexError:
            pass
    
    def clear(self):
        self._processor_sequence.clear()

class ImageProcessorSequenceList(ImageProcessorSequence):

    logger = logging.getLogger(__name__)

    def __init__(self, priority=0, enabled=True):
        """
        """
        self._priority = priority
        self._enabled = enabled
        self._processor_sequence = sortedcontainers.SortedList()

    @property
    def processor_sequence(self):
        return self._processor_sequence
    
    @property
    def priority(self):
        return self._priority
    
    @property
    def enabled(self):
        return self._enabled

    def add(self, processor: ImageProcessor, allow_consecutive=False):
        """
        Add a processor to the sequence. If the processor is enabled, it is added to the sequence.
        
        Parameters
        ----------
        processor : ImageProcessor
            The processor to add to the sequence.

        allow_consecutive : bool, optional = False
            If True, the same processor can be added to the sequence twice in a row. Set to False by default.
        """

        # Dont allow two of the same processor in a row

        if not processor.enabled:
            return

        if not allow_consecutive:
            if len(self._processor_sequence) > 1:
                if processor == self._processor_sequence[-1]:
                    return

        self._processor_sequence.add(processor.copy())

    def discard(self, processor: ImageProcessor):
        self._processor_sequence.discard(processor)

    def pop(self, index: int = -1):
        """
        Remove and return a processor from the sequence at the specified index. 
        If no index is specified, remove and return the last processor.
        If the index is out of range, return None.
        """
        try:
            return self.processor_sequence.pop(index)
        except IndexError:
            return None
        
    def clear(self):
        self._processor_sequence.clear()