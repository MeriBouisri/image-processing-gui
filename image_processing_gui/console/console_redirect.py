import sys
import io

import tkinter as tk
from tkinter import ttk

class ConsoleRedirect(io.TextIOWrapper):
    def __init__(self, text_widget, autoscroll=True, stream_tag='stdout'):
        super().__init__(sys.stdout.buffer, encoding='utf-8')

        self.text_widget = text_widget
        self.autoscroll = autoscroll
        self.stream_tag = stream_tag

    def write(self, string):
        if self.autoscroll:
            self.text_widget.see(tk.END)

        self.text_widget.insert(tk.END, string, self.stream_tag)

    def flush(self):
        super().flush()

    def close(self):
        super().close()