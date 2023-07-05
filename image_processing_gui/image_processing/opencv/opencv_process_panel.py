import logging
import tkinter as tk
from tkinter import ttk

from .opencv_data import opencv_data
from ...image_system.image_processor import ImageProcessorFunction

from ...events.event_broker import EventBroker
from ...events.event_subscriber import EventSubscriber
from ...events.event_publisher import EventPublisher
from ...events.event_constants import *


class OpenCVProcessPanel(tk.LabelFrame):
    def __init__(self, master, event_broker: EventBroker, process_key, process_data: dict,  *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.process_data = process_data

        
        self.image_process = ImageProcessorFunction(name=process_key, 
                                                    enabled=False,
                                                    source_keyword=process_data['source_keyword'],
                                                    callback=process_data['function'], 
                                                    priority=process_data['priority'])
        
        try:
            return_index = process_data['return_index']
            self.image_process.return_index = return_index
        except KeyError:
            pass

        self.event_broker = event_broker
        self.event_publisher = EventPublisher(event_broker)
        self.event_subscriber = EventSubscriber(event_broker)

        self.onvalue = False
        self.offvalue = True

        self.checkbox_var = tk.BooleanVar()
        self.checkbox_var.set(self.offvalue)

        self.checkbox = ttk.Checkbutton(self, 
                                        variable=self.checkbox_var,
                                        onvalue=self.onvalue,
                                        offvalue=self.offvalue,
                                        text=self.process_data['title'], 
                                        command=self.on_toggle_checkbox)

        self.config(labelwidget=self.checkbox)
        self.columnconfigure(0, weight=1)

        self.create_widgets()
        self.config_grandchildren_state(tk.DISABLED)

        
        self.event_subscriber.subscribe(RequestEvent.REQUEST_PROCESSOR_UPDATE, self.on_request)

    def on_request(self, event):
        self.event_publisher.publish(ImageProcessingEvent.UPDATE_PROCESS, process=self.image_process)

    def create_widgets(self):

        for i, (process_key, process_data) in enumerate(self.process_data['parameters'].items()):

            widget_type = process_data['widget']

            match widget_type:
                case 'combobox':
                    self.create_combobox(process_data, i)

                case 'slider':
                    self.create_slider(process_data, i)

                case 'spinbox':
                    self.create_spinbox(process_data, i)

                case 'unimplemented':
                    self.create_unimplemented(process_data, i)

                case _:
                    self.logger.error(f'Widget type not found: {widget_type}')

    def create_parameter_frame(self) -> ttk.Frame:
        column_size = 4
        parameter_frame = ttk.Frame(self)

        for i in range(column_size):
            parameter_frame.columnconfigure(i, weight=1)
        
        return parameter_frame

    def create_combobox(self, process_parameter, index=0):
        # ========== ComboBox frame layout ========== #

        parameter_frame = self.create_parameter_frame()

        # ========== Combobox parameter data ========== #

        parameter_title = process_parameter['title']
        parameter_options = list(process_parameter['options'].keys())
        parameter_default = process_parameter['default']

        # ========== Combobox frame widgets ========== #

        parameter_title_label = ttk.Label(parameter_frame, text=parameter_title)

        parameter_combobox = ttk.Combobox(parameter_frame, values=parameter_options)
        parameter_combobox.current(0)

        # Layout the child parameter widgets
        parameter_title_label.grid(row=0, column=0, sticky=tk.NSEW)
        parameter_combobox.grid(row=0, column=1, columnspan=2, sticky=tk.NSEW, padx=5)

        # Layout the parent parameter frame
        parameter_frame.grid(row=index, column=0, sticky=tk.NSEW, pady=1)

        # ========== Combobox event bindings ========== #

        combobox_command = lambda event : self.on_combobox_action(event.widget.get(), process_parameter)
        parameter_combobox.bind('<<ComboboxSelected>>', combobox_command)

        self.on_combobox_action(parameter_combobox.get(), process_parameter)

    def create_slider(self, process_parameters, index=0):
        # ========== Slider frame ========== #

        parameter_frame = self.create_parameter_frame()

        # ========== Slider parameter data ========== #
        
        parameter_title = process_parameters['title']
        parameter_default = process_parameters['default']
        parameter_max = process_parameters['max']
        parameter_min = process_parameters['min']

        # ========== Slider frame widgets ========== #

        slider_variable = tk.IntVar(value=parameter_default)

        parameter_title_label = ttk.Label(parameter_frame, text=parameter_title)
        parameter_value_label = ttk.Label(parameter_frame, textvariable=slider_variable)
        parameter_slider = ttk.Scale(parameter_frame, 
                                     from_=parameter_min, 
                                     to=parameter_max, 
                                     orient=tk.HORIZONTAL,
                                     variable=slider_variable)
        
        parameter_slider.bind('<Button-1>', lambda event: self.event_publisher.publish(GlobalEvent.PAUSE))
        parameter_slider.bind('<ButtonRelease-1>', lambda event: self.event_publisher.publish(GlobalEvent.RESUME))
        
        parameter_slider.config(command= lambda value : [
            slider_variable.set(int(float(value))), 
            self.on_slider_action(slider_variable.get(), process_parameters)
            ]
        )

        # Layout the child parameter widgets
        parameter_title_label.grid(row=0, column=0, sticky=tk.NSEW)
        parameter_slider.grid(row=0, column=1, columnspan=2, sticky=tk.NSEW)
        parameter_value_label.grid(row=0, column=3, sticky=tk.NSEW)

        # Layout the parent parameter frame
        parameter_frame.grid(row=index, column=0, sticky=tk.NSEW, padx=2, pady=2)

        self.on_slider_action(parameter_default, process_parameters)
    
    def create_spinbox(self, process_parameters, index=0):
        # ========== Spinbox frame ========== #

        parameter_frame = self.create_parameter_frame()

        # ========== Spinbox parameter data ========== #
        
        parameter_title = process_parameters['title']
        parameter_default = process_parameters['default']
        parameter_max = process_parameters['max']
        parameter_min = process_parameters['min']

        # ========== Spinbox frame widgets ========== #

        spinbox_variable = tk.IntVar(value=parameter_default)

        parameter_title_label = ttk.Label(parameter_frame, text=parameter_title)
        parameter_spinbox = ttk.Spinbox(parameter_frame, 
                                        from_=parameter_min, 
                                        to=parameter_max, 
                                        textvariable=spinbox_variable,
                                        command= lambda : 
                                            self.on_spinbox_action(value=spinbox_variable.get(),
                                                                   process_parameter=process_parameters))
        
        parameter_spinbox.bind('<Button-1>', lambda event:self.event_publisher.publish(GlobalEvent.PAUSE))
        parameter_spinbox.bind('<ButtonRelease-1>', lambda event:self.event_publisher.publish(GlobalEvent.RESUME))
        # Layout the child parameter widgets
        parameter_title_label.grid(row=0, column=0, sticky=tk.NSEW)
        parameter_spinbox.grid(row=0, column=1, columnspan=2, sticky=tk.NSEW)

        # Layout the parent parameter frame
        parameter_frame.grid(row=index, column=0, sticky=tk.NSEW, padx=2, pady=2)

    def create_unimplemented(self, process_parameters, index=0):
        parameter_keyword = process_parameters['keyword']
        parameter_default = process_parameters['default']
        
        self.image_process.add_argument(**{parameter_keyword: parameter_default})

    def on_spinbox_action(self, value, process_parameter):
 
        try:
            value = int(value)
        except ValueError:
            value = process_parameter['default']

        if value > process_parameter['max']: value = process_parameter['max']
        elif value < process_parameter['min']: value = process_parameter['min']

        parameter_keyword = process_parameter['keyword']
        self.image_process.add_argument(**{parameter_keyword: value})
        self.event_publisher.publish(ImageProcessingEvent.UPDATE_PROCESS, process=self.image_process)


    def on_combobox_action(self, selection, process_parameter):

        parameter_value = process_parameter['options'][selection]
        parameter_keyword = process_parameter['keyword']
        
        self.image_process.add_argument(**{parameter_keyword: parameter_value})
        self.event_publisher.publish(ImageProcessingEvent.UPDATE_PROCESS, process=self.image_process)
 
    
    def on_slider_action(self, value, process_parameter):
        parameter_keyword = process_parameter['keyword']
        self.image_process.add_argument(**{parameter_keyword: value})

        self.event_publisher.publish(ImageProcessingEvent.UPDATE_PROCESS, process=self.image_process)

    def on_toggle_checkbox(self):
        self.image_process.enabled = self.checkbox.instate(['selected'])
        
        if self.image_process.enabled:
            self.config_grandchildren_state(tk.NORMAL)
        else:
            self.config_grandchildren_state(tk.DISABLED)

        self.event_publisher.publish(ImageProcessingEvent.UPDATE_PROCESS, process=self.image_process)

    def config_grandchildren_state(self, state):

        for parameter_frame in self.winfo_children():
            for parameter_widget in parameter_frame.winfo_children():
                parameter_widget.config(state=state) # type: ignore

    def reset(self):
        self.checkbox_var.set(self.offvalue)
        self.config_grandchildren_state(tk.DISABLED)
        self.image_process.enabled = False
        self.event_publisher.publish(ImageProcessingEvent.UPDATE_PROCESS, process=self.image_process)
    




