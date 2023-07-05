from abc import ABC, abstractmethod

class ConsoleTab(ABC):

    @abstractmethod
    def on_save(self):
        pass
    
    @abstractmethod
    def on_clear(self):
        pass

    @abstractmethod
    def on_close(self):
        pass