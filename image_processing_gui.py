from image_processing_gui.app import App

import sys, os 
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if getattr(sys, 'frozen', False):
    DIRPATH = os.path.dirname(sys.executable)
    sys.path.append(DIRPATH) 
    config_file = DIRPATH+"//outside_folder//config.yml"

if __name__ == "__main__":
    app = App()
    app.root.mainloop()
