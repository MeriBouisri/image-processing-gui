import logging
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import queue



from ..image_system.image_displayer import ImageDisplayer
from ..image_system.image_reader import ImageReader, StaticImageReader, StaticImageFileReader, DynamicImageReader
from ..image_system.image_processor import ImageProcessor

from ..events.event_constants import *
from ..events.event_broker import EventBroker
from ..events.event_subscriber import EventSubscriber
from ..events.event_publisher import EventPublisher


class ImageCanvas(tk.Canvas):

    MS_DELAY = 200
    
    def __init__(self, master, event_broker: EventBroker, reader: ImageReader = None, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.is_running = False

        self.logger = logging.getLogger(__name__)

        self.event_broker = event_broker
        self.event_publisher = EventPublisher(event_broker)
        self.event_subscriber = EventSubscriber(event_broker)

        self.display_queue = queue.Queue()
        self.displayer = ImageDisplayer(display_queue=self.display_queue, 
                                        reader=reader)
        self.image_item = None

        self.config(relief=tk.SOLID, borderwidth=1)
        self.bind('<Button-3>', self.on_context_menu)

        self.event_subscriber.subscribe(GlobalEvent.PAUSE, self.on_pause)
        self.event_subscriber.subscribe(GlobalEvent.RESUME, self.on_resume)
        # self.event_subscriber.subscribe(DisplayEvent.EYE_TRACKER_MODE, self.on_eye_tracker_mode)

        self._loop_image = False

    

    def is_empty(self):
        return self.displayer.is_empty()

    def set_reader(self, reader: ImageReader):
        self.displayer.set_reader(reader)

        self.event_subscriber.subscribe(ImageProcessingEvent.APPLY_PROCESS, self.on_update_process)
        self.event_subscriber.subscribe(DisplayEvent.CLOSE, self.on_close)
        self.is_running = True
        self.on_update_process()

    # def on_eye_tracker_mode(self, event, processor: ImageProcessor):
    #     eye_tracker = EyeTrackerImageDisplayer(self.event_broker,self.display_queue, self.displayer.reader)
    #     self.displayer = eye_tracker
    #     self.on_update_process()

    def on_select_image(self, event):
        self.event_publisher.publish(DisplayEvent.SELECT, self.reader)

    def set_selectable(self, selectable: bool):
        pass

    def fit_image_to_canvas(self, image):
        self.update_idletasks()
        canvas_width, canvas_height = self.winfo_width(), self.winfo_height()
        
        image_width, image_height = image.size
        new_image_width, new_image_height = image_width, image_height

        if image_width > canvas_width:
            new_image_width = canvas_width
            new_image_height = int(new_image_width * image_height / image_width)

        if new_image_height > canvas_height:
            new_image_height = canvas_height
            new_image_width = int(new_image_height * image_width / image_height)

        return image.resize((new_image_width, new_image_height), Image.ANTIALIAS)

    def display_image(self):
        
        if self.displayer is None:
            return
        
        if not self.is_running:
            return

        self.displayer.display()

        if not self.display_queue.empty():
            image = self.display_queue.get()
            image = self.fit_image_to_canvas(image)
            tk_image = ImageTk.PhotoImage(image)
            self.image_item = self.create_image(0, 0, image=tk_image, anchor=tk.NW)
      
            self.image = tk_image
        
        self.after(self.MS_DELAY, self.display_image)


    def on_context_menu(self, event):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label='Delete', command=self.on_close)

        self.event_publisher.publish(DisplayEvent.PAUSE)

        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def on_close(self, event=''):
        if self.displayer is not None:
            self.displayer.stop()
        self.reader = None
        self.image_item = None
        self.delete('all')

        self.event_subscriber.unsubscribe(DisplayEvent.CLOSE, self.on_close)
        self.event_subscriber.unsubscribe(ImageProcessingEvent.APPLY_PROCESS, self.on_update_process)
        self.set_selectable(False)

    def on_pause(self, event=''):
        self._loop_image = False

    def on_resume(self, event=''):
        self._loop_image = True
        self.on_update_process()

    def on_update_process(self, event='', 
                          processor: ImageProcessor = None, 
                          preprocessor: ImageProcessor = None):
        
        self.processor = processor

        if not self.is_running:
            return
    
        
        if self.displayer is None:
            self.logger.debug('No displayer')
            return
        
        self.displayer.display(processor=processor, preprocessor=preprocessor)

        if not self.display_queue.empty():
            image = self.display_queue.get()

            if image is None:
                return
            
            image = self.fit_image_to_canvas(image)

            if image is None:
                return
            
            tk_image = ImageTk.PhotoImage(image)
            self.create_image(0, 0, image=tk_image, anchor=tk.NW)
            self.image = tk_image

        if isinstance(self.displayer.reader, DynamicImageReader) and self._loop_image:
            self.after(self.MS_DELAY, self.on_update_process, '', self.processor)


class MainImageCanvas(ImageCanvas):
    def __init__(self, master, event_broker: EventBroker, reader: ImageReader = None, *args, **kwargs):
        super().__init__(master=master, event_broker=event_broker, reader=reader, *args, **kwargs)
        # self.set_selectable(True)

    def fit_image_to_canvas(self, image):
        return super().fit_image_to_canvas(image)
    
    def set_selectable(self, selectable: bool = True):
        if selectable:
            self.bind('<Button-1>', self.on_select_image)
        


        else:
            self.unbind('<Button-1>')
    
    def on_select_image(self, event):
        self.config(cursor='fleur')
        self.bind('<B1-Motion>', self.on_move_image)
        self.bind('<ButtonRelease-1>', lambda event : [ 
            self.config(cursor=''), 
            self.unbind('<B1-Motion>')
        ])

    def on_move_image(self, event):

        if self.image_item is None:
            return

        canvas_x, canvas_y = self.coords(self.image_item)

        image_width = self.image.width()
        image_height = self.image.height()

        relmouse_dx = event.x - canvas_x - image_width / 2
        relmouse_dy = event.y - canvas_y - image_height / 2

        self.move(self.image_item, relmouse_dx, relmouse_dy)

    def on_resize_image(self, event=''):
        popup = tk.Toplevel(self)
        popup.title('Resize image')

        width_label = ttk.Label(popup, text='Width')
        height_label = ttk.Label(popup, text='Height')

        width_entry = ttk.Entry(popup)
        height_entry = ttk.Entry(popup)

        width_label.grid(row=0, column=0, sticky=tk.W)
        height_label.grid(row=1, column=0, sticky=tk.W)

        width_entry.grid(row=0, column=1, sticky=tk.E)
        height_entry.grid(row=1, column=1, sticky=tk.E)

        width_entry.insert(0, self.image.width())
        height_entry.insert(0, self.image.height())

        popup.bind('<Return>', self.on_resize)


    def on_resize(self, event=''):
        self.logger.debug(f'Resizing image:{event.data}')

    def on_context_menu(self, event):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label='Delete', command=self.on_close)
        # self.context_menu.add_command(label='Resize', command=self.on_resize_image)

        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
        

class SideImageCanvas(ImageCanvas):
    def __init__(self, master, event_broker: EventBroker, reader: ImageReader = None, *args, **kwargs):
        super().__init__(master=master, event_broker=event_broker, reader=reader, *args, **kwargs)

    def set_selectable(self, is_selectable: bool = True):
        if is_selectable:
            self.bind('<Button-1>', lambda event : self.config(relief=tk.SUNKEN))
            self.bind('<ButtonRelease-1>', lambda event : self.config(relief=tk.RAISED))
            self.bind('<Double-Button-1>', self.on_select_image)

        else:
            self.unbind('<Button-1>')
            self.unbind('<ButtonRelease-1>')
            self.unbind('<Double-Button-1>')

    def on_select_image(self, event):
        if self.is_empty():
            return

        self.event_publisher.publish(DisplayEvent.SELECT, self.displayer.reader)

    def fit_image_to_canvas(self, image):
        self.update_idletasks()
        canvas_width, canvas_height = self.winfo_width(), self.winfo_height()
        return image.resize((canvas_width, canvas_height), Image.ANTIALIAS)

    



    

