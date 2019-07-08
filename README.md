# DZquery
a simple query tool with a dank HUD for the game DayZ

Usage:

run the compiled .exe and join a server.

Compiling:

1. have your poke around the code and config as much as you'd like
2. install python 3.7
3. run the "compile.bat" 

Notes:

-Currently only optimized for 1920x1080p displays (feel free to edit the values in the config to make it fit your display though)
-The loading of all necessary libraries takes a while. Read the console prompt
-Does not work when the game is in fullscreen-mode. Use borderless windowed. I will not start messing with Direct3d drivers and memory

config:


    "updateRate": The rate in seconds the server is queried (TYPE: INT) (this setting is updated in runtime, you can change it when the code i s running and it will apply on the next cycle)
    "PfromTop": How many pixels from the top of the display the overlay is placed (TYPE: STRING)
    "PfromSide": How many pixels from the LEFT side of the display the overlay is placed (TYPE: STRING)
    "TextColour": Colour of the overlay text(TYPE: STRING)
    "BGColour": Colour of the background. Doesnt really change much, but bleeds a bit, so black is the best to use for most "TextColour" options
    
    
