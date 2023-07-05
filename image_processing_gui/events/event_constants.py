import os

EVT_DUMMY = 'DUMMY_EVENT|HELLO_WORLD'

separator = '|'

event = {
    'add': 'ADD', 
    'apply': 'APPLY', 
    'available': 'AVAILABLE', 
    'clear': 'CLEAR', 
    'close': 'CLOSE', 
    'delete': 'DELETE', 
    'exit': 'EXIT', 
    'global': 'GLOBAL',
    'open': 'OPEN', 
    'pause': 'PAUSE', 
    'play': 'PLAY', 
    'redo': 'REDO', 
    'remove': 'REMOVE', 
    'revert': 'REVERT', 
    'resume': 'RESUME', 
    'reset': 'RESET', 
    'save': 'SAVE', 
    'select': 'SELECT', 
    'show': 'SHOW',
    'start': 'START', 
    'stop': 'STOP', 
    'toggle': 'TOGGLE', 
    'undo': 'UNDO', 
    'update': 'UPDATE',
    'enable': 'ENABLE',
    'display': 'DISPLAY'
}


widget = {
    'sidebar': 'SIDEBAR',
    'console': 'CONSOLE',
    'display': 'DISPLAY',
    'side_display': 'SIDE_DISPLAY',
    'main_display': 'MAIN_DISPLAY',
    'image_canvas': 'IMAGE_CANVAS',
    'menu': 'MENU',
    'toolbar': 'TOOLBAR',
    'none': 'NONE',
    'global': 'GLOBAL'
}

image_processing = {
    'displayer': 'DISPLAYER',
    'processor': 'PROCESSOR',
    'reader': 'READER',
}

settings = {
    'logger_redirect': 'LOGGER_REDIRECT',
    'stdout_redirect': 'STDOUT_REDIRECT'
}



misc = {
    'file': 'FILE',
    'image': 'IMAGE',
    'webcam': 'WEBCAM',
    'tab': 'TAB',
    'data': 'DATA',
    'request': 'REQUEST',
    'all': 'ALL',
    'global': 'GLOBAL',
    'eye_tracker_mode': 'EYE_TRACKER_MODE'
}



class MenuEvent:
    """
    Anatomy of an event string :

    [SOURCE] | [ACTION] | [TARGET]
    """
    OPEN_IMAGE = separator.join([widget['menu'], event['open'], misc['image']])
    OPEN_WEBCAM = separator.join([widget['menu'], event['open'], misc['webcam']])
    SAVE_FILE = separator.join([widget['menu'], event['save'], misc['file']])

    UNDO = separator.join([widget['menu'], event['undo']])
    REDO = separator.join([widget['menu'], event['redo']])

    TOGGLE_SIDEBAR = separator.join([widget['menu'], event['toggle'], widget['sidebar']])
    TOGGLE_CONSOLE = separator.join([widget['menu'], event['toggle'], widget['console']])
    TOGGLE_SIDE_DISPLAY = separator.join([widget['menu'], event['toggle'], widget['side_display']])

    EXIT = separator.join([widget['menu'], event['exit']])

class SettingsEvent:
    """
    Anatomy of an event string :

    [SOURCE] | [ACTION] | [TARGET]
    """
    TOGGLE_LOG_REDIRECT = separator.join([widget['menu'], event['toggle'], settings['logger_redirect']])

class SidebarEvent:
    APPLY_PROCESS = separator.join([widget['sidebar'], event['apply'], image_processing['processor']])
    REVERT_PROCESS = separator.join([widget['sidebar'], event['revert'], image_processing['processor']])
    RESET_PROCESS = separator.join([widget['sidebar'], event['update'], image_processing['processor']])
    UNDO_PROCESS = separator.join([widget['sidebar'], event['undo'], image_processing['processor']])
    SAVE_PROCESS = separator.join([widget['sidebar'], event['save'], image_processing['processor']])

    TOGGLE_APPLY_BUTTON = separator.join([widget['sidebar'], event['toggle'], event['apply']])
    TOGGLE_REVERT_BUTTON = separator.join([widget['sidebar'], event['toggle'], event['revert']])
    TOGGLE_RESET_BUTTON = separator.join([widget['sidebar'], event['toggle'], event['reset']])
    TOGGLE_SHOW_BUTTON = separator.join([widget['sidebar'], event['toggle'], event['show']])
    TOGGLE_ALL_BUTTONS = separator.join([widget['sidebar'], event['toggle'], event['global']])


    UPDATE_PROCESS = separator.join([widget['sidebar'], event['update'], image_processing['processor']])

class ConsoleEvent:
    """
    Anatomy of an event string :
    
    [SOURCE] | [ACTION] | [TARGET]
    """
    CLOSE = separator.join([widget['console'], event['close']])
    CLEAR = separator.join([widget['console'], event['clear']])
    ADD = separator.join([widget['console'], event['add']])



class DisplayEvent:
    """
    Anatomy of an event string :
    
    [SOURCE] | [ACTION] | [TARGET]
    """
    AVAILABLE = separator.join([widget['display'], event['available']])
    CLOSE = separator.join([widget['display'], event['close']])
    PAUSE = separator.join([widget['display'], event['pause']])
    PLAY = separator.join([widget['display'], event['play']])
    START = separator.join([widget['display'], event['start']])
    SELECT = separator.join([widget['display'], event['select']])

    DISPLAY_IMAGE = separator.join([widget['display'], event['display'], misc['image']])
    EYE_TRACKER_MODE = separator.join([widget['display'], event['display'], misc['eye_tracker_mode']])

class GlobalEvent:
    """
    """
    PAUSE = separator.join([event['global'], event['pause']])
    RESUME = separator.join([event['global'], event['resume']])
    EXIT = separator.join([event['global'], event['exit']])

class SideDisplayEvent:
    """
    Anatomy of an event string :
    
    [SOURCE] | [ACTION] | [TARGET]
    """
    SELECT = separator.join([widget['side_display'], event['select']])
    ADD = separator.join([widget['side_display'], event['add']])

class ImageCanvasEvent:
    """
    Anatomy of an event string :
    
    [SOURCE] | [ACTION] | [TARGET]
    """
    SELECT = separator.join([widget['image_canvas'], event['select']])
    DELETE = separator.join([widget['image_canvas'], event['delete']])
    ADD = separator.join([widget['image_canvas'], event['add']])


class ImageProcessingEvent:
    START_PROCESS = separator.join([image_processing['processor'], event['start']])
    STOP_PROCESS = separator.join([image_processing['processor'], event['stop']])
    UPDATE_PROCESS = separator.join([image_processing['processor'], event['update']])
    APPLY_PROCESS = separator.join([image_processing['processor'], event['apply']])

class ToolbarEvent:
    PLAY = separator.join([widget['toolbar'], event['play']])
    PAUSE = separator.join([widget['toolbar'], event['pause']])
    CLOSE = separator.join([widget['toolbar'], event['close']])

    TOGGLE_PLAY_BUTTON = separator.join([widget['toolbar'], event['toggle'], event['play']])
    TOGGLE_PAUSE_BUTTON = separator.join([widget['toolbar'], event['toggle'], event['pause']])
    TOGGLE_CLOSE_BUTTON = separator.join([widget['toolbar'], event['toggle'], event['close']])
    TOGGLE_ALL_BUTTONS = separator.join([widget['toolbar'], event['toggle'], event['global']])



class RequestEvent:
    REQUEST_PROCESSOR_UPDATE = separator.join([misc['request'], image_processing['processor'], event['update']])


