# KivyAtlasGenerator  
Generates Kivy's .atlas files for spritesheets  

To be used with my other project, KivyTileMapper  
https://github.com/doyousketch2/KivyTileMapper  

First you'll need Python.  Linux and OSX users should be fine.  
Windows users might need to download it from their website  
https://www.python.org/downloads/  

I used v3.4.2 to create this, so version 3 or higher is recommended.  
It's possible it'll run in fine in v2.7x - The code is simple,  
and I think Kivy does OK on either, so whatever's clever, ya know?  

------
Then you'll need Python's package installer, pip.  
Pip should come with Python, but if not...  

- Linux:  
`sudo apt-get update && apt-get install pip pip3`

- OSX:  
`sudo easy_install pip`

- Win:  
if you don't have it, it's probably best to  
download a new version of Python from their website.  

------
**Use pip to install Kivy**

- Linux:  
`pip3 install kivy`

- OSX:  
`python -m pip install kivy`

- Windows:  
`py -m pip install kivy`

------
Alright, once you're certain you have Python and Kivy,  
you can **run the KivyAtlasGenerator**  

- Linux:  
`./main.py`

- OSX:  
`./python -m main.py`

- Win:  
`py -m main.py`
