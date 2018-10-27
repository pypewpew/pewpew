Pewmulator
**********

Pewmulator is an emulator for the PewPew library that lets you play the games
writen for the PewPew devices on your computer. It comes in the form of a
Python 3 library that uses PyGame under the hood to implement all necessary
parts of the PewPew library.

Note that the code is then being executed with Python 3 and not CircuitPython,
so there may be some differences. The most obvious difference is the amount of
RAM memory available --- so if you write a game in Pewmulator, chances are it
won't run on PewPew because of lack of memory.

You can get the library from the `github repository
<https://github.com/pewpew-game/pewmulator>`. Just place the ``pew.py`` file
alongside the code of your game, and run your game with Python 3.
