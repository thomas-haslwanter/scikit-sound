scikit-sound - Documentation
============================

*scikit-sound* is a library for working with sound files.

It is hosted under https://github.com/thomas-haslwanter/scikit-sound, and
contains only one module: :py:mod:`sounds` . This module has two classes for working
with sounds:

    - :py:class:`sounds.Sound` ... reading working with sounds.
    - :py:class:`sounds.FFMPEG_info` ... handling the FFMPEG installation required for working with MP3-files etc.

The class *Sounds* lets you

    - :py:meth:`sounds.Sound.read_sound`  read in sounds from sound-files (WAV, etc).
    - :py:meth:`sounds.Sound.generate_sound` generate sounds from numpy arrays.
    - :py:meth:`sounds.Sound.play` play sounds
    - :py:meth:`sounds.Sound.get_info` show the corresponding information (sample rate, number of channels, etc.) 
    - :py:meth:`sounds.Sound.write_wav` write out sounds.

The class *FFMPEG_info* handles the detection of FFMPEG, and the
config-information for Python:

    The Python standard libraries and *scipy* provide good support for
    working with WAV files. If you also want to work with other file formats
    (MP3, AAC, etc), the easiest way is to install the open-source software
    *FFMPEG* on your computer. You can obtain *FFMPEG* for free from
    http://ffmpeg.org

    For more information, please check the help on the method *Sounds.sound()*

Installation
------------

The simplest way to install *sksound* is 

>>> pip install scikit-sound

For upgrading to the latest version of *sksound*, you have to type

>>> pip install scikit-sound -U

However, you can also install from the source files. To do this, just go to
the root directory of the package, and type

>>> python setup.py install

**Note**: After *sksound* is installed, I typically import it in
*Python* with:

>>> import sksound

Dependencies
^^^^^^^^^^^^
numpy, scipy, easygui, appdirs, pygame

Testing
-------

The easiest way to test the package is with *unittest*. Open a terminal,
and type (on the command-line!):

>>> cd [_your_installation_dir_]\sksound\tests
>>> python -m unittest

Modules
-------

.. toctree::
   :maxdepth: 2

   sounds


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. note::
    | *Author:*     Thomas Haslwanter
    | *Version:*    0.1.6
    | *Date:*       March 2017
    | *email:*      thomas.haslwanter@fh-linz.at
    | *Copyright (c):*      2017, Thomas Haslwanter. All rights reserved.
    | *Licence:*    This work is licensed under the `BSD 2-Clause License <http://opensource.org/licenses/BSD-2-Clause>`_

