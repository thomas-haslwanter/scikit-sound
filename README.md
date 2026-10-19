![Title](images/scikit_sound.png)
============

scikit-sound
============

*scikit-sound* contains functions for working with sound

Dependencies
------------

numpy, scipy

Homepage
--------

<http://work.thaslwanter.at/sksound/html/>

Author: Thomas Haslwanter Date: 19-10-2026 Ver: 0.3.3 Licence: BSD
3-Clause License (<http://opensource.org/licenses/BSD-3-Clause>)
Copyright (c) 2026, Thomas Haslwanter All rights reserved.

Installation
------------

You can install scikit-sound with

> pip install scikit-sound

and upgrade to a new version with

> pip install scikit-sound -U

Sound Processing Utilities
==========================

- sounds.Sound ... class, with methods
  - generate_sound
  - get_info
  - play
  - read_sound
  - summary
  - write_wav

Misc Other Utilities
====================

- misc ... GUI routines for standard file- and directory-handling
  - askquestion
  - get_dir
  - get_file
  - progressbar
  - save_file

Set FFMPEG-path by hand
=======================

This can be done with `sksound.sounds.FFMPEG_info().set()`
