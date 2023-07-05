import os
import sys

if getattr(sys, 'frozen', False):
    # If the application is running in a PyInstaller bundle
    currentdir = sys._MEIPASS
else:
    # If the application is running in a normal Python environment
    real_path = os.path.realpath(__file__)
    currentdir = os.path.dirname(real_path)

assets_dir = os.path.join(currentdir, 'assets')

# get data file from spec
start_icon_dir = os.path.join(assets_dir, 'play-circle.png')
pause_icon_dir = os.path.join(assets_dir, 'pause-circle.png')
close_icon_dir = os.path.join(assets_dir, 'stop-circle.png')


image_assets = {
    'play_icon': start_icon_dir,
    'pause_icon': pause_icon_dir,
    'close_icon': close_icon_dir
}