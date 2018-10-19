import sys
import os
import pew
import pew_menu

pew.init()
while True:
    files = [name[:-3] for name in os.listdir()
             if name.endswith('.py') and name != 'main.py']
    selected = pew_menu.menu(files)
    game = files[selected]
    del files
    try:
        __import__(game)
    except pew.GameOver:
        pass
    del sys.modules[game]
