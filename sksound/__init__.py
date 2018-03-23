'''
"scikit-sound" contains functions for working with sound signals

Dependencies
------------
numpy, scipy, easygui, json, appdirs, sounddevice

Homepage
--------
http://work.thaslwanter.at/sksound/html/

Copyright (c) 2018 Thomas Haslwanter <thomas.haslwanter@fh-linz.at>

'''

import importlib

__author__ = "Thomas Haslwanter <thomas.haslwanter@fh-linz.at"
__license__ = "BSD 2-Clause License"
__version__ = "0.2.1"

__all__ = ['sounds']

for _m in __all__:
    importlib.import_module('.'+_m, package='sksound')
    
