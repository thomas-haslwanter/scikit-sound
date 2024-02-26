'''
"scikit-sound" contains functions for working with sound signals

Dependencies
------------
numpy, scipy, json, appdirs, sounddevice

Homepage
--------
http://work.thaslwanter.at/sksound/html/

Copyright (c) 2023 Thomas Haslwanter <thomas.haslwanter@fh-ooe.at>

'''

import importlib

__author__ = "Thomas Haslwanter <thomas.haslwanter@fh-linz.at"
__license__ = "BSD 2-Clause License"
__version__ = "0.2.13"

__all__ = ['misc', 'sounds']

for _m in __all__:
    importlib.import_module('.'+_m, package='sksound')
    
