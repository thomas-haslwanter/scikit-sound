============
scikit-sound
============

*scikit-sound* contains functions for working with sound 

Dependencies
------------
numpy, scipy

Homepage
--------
http://work.thaslwanter.at/sksound/html/

:Author:  Thomas Haslwanter
:Date:    Oct-07-2024
:Ver:     0.2.15
:Licence: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)
:Copyright:
    |copy| 2024, Thomas Haslwanter, all rights reserved.

.. |copy|   unicode:: U+000A9 .. COPYRIGHT SIGN

Installation
------------
You can install scikit-sound with

    pip install scikit-sound

and upgrade to a new version with

    pip install scikit-sound -U

Sound Processing Utilities
==========================

- sounds.Sound ... class, with methods
    * generate_sound
    * get_info
    * play
    * read_sound
    * summary
    * write_wav

Misc Other Utilities
====================

- misc ... GUI routines for standard file- and directory-handling
   * askquestion
   * get_dir
   * get_file
   * progressbar
   * save_file
