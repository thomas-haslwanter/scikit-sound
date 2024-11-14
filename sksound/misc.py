"""
Miscellaneous user interface utilities for

    - selecting files or directories.
      If nothing or a non-existing file/direcoty is selected, the return is
      "None". Otherwise the file/directory is returned.
    - waitbar

"""

# author: Thomas Haslwanter
# date: Nov-2024


import os
# import matplotlib.pyplot as plt
# plt.switch_backend('agg')

import sys

import tkinter
import tkinter.filedialog as tkf
from tkinter import messagebox
from pathlib import Path
import numpy as np
from collections.abc import Generator


def progressbar(it:np.ndarray|range, prefix:str="", size:int=60)->Generator:
    """
    Shows a progress-bar on the commandline.
    This has the advantage that you don't need to bother with windows
    managers. Nifty coding!

    Parameters
    ----------
    it : index variable (integer)
    prefix : Text preceding the progress-bar
    size : Length of progress-bar

    Examples
    --------
    >>> import time
    >>> for ii in progressbar(range(50), 'Computing ', 25):
    >>>    #print(ii)
    >>>    time.sleep(0.05)

    """

    count = len(it)

    def _show(_i):
        # Helper function to print the desired information line.

        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x),
                                               _i, count))
#        sys.stdout.flush()

    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()


def get_file(filter_spec:str='*', dialog_title:str='Select File: ',
             default_name:str='') -> os.PathLike|None|str:
    """
    Selecting an existing file.

    Parameters
    ----------
    filter_spec: File filters
    dialog_title: Window title
    default_name: Can be a directory AND filename

    Returns
    -------
    filename :  selected existing file (partent + name)
                If no file is selected, 'None' is returned

    Examples
    --------
    >>> my_file = skinematics.ui.getfile('*.py', 'Testing file-selection', 'c:\\temp\\test.py')

    """

    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected_file = Path(tkf.askopenfilename(initialfile=default_name,
            title=dialog_title, filetypes=[('all files','*'), ('Select',
                filter_spec)]))

    # Close the Tk-window manager again
    root.destroy()

    if not os.path.exists(selected_file):
        return None
    else:
        return selected_file


def save_file(filter_spec:str='*', dialog_title:str='Save File: ',
              default_name:str='') -> os.PathLike|None:
    """
    Selecting an existing or new file:

    Parameters
    ----------
    filter_spec : string
        File filters.
    dialog_title : string
        Window title.
    default_name : string
        Can be a directory AND filename.

    Returns
    -------
    selected_file : Selected file (parent + name)

    Examples
    --------
    >>> selected_file = skinematics.ui.savefile('*.py', 'Testing file-selection', 'c:\\temp\\test.py')

    """

    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected_file = tkf.asksaveasfile(mode='w',
                                title=dialog_title,
                                initialfile=default_name,
                                filetypes=[('Save as', filter_spec)])

    # Close the Tk-window manager again
    root.destroy()

    return Path(selected_file.name)


def get_dir(dialog_title:str='Select Directory',
            default_name:str='.')->os.PathLike|None:
    """ Select a directory

    Parameters
    ----------
    dialog_title : Window title
    default_name : Can be a directory AND filename

    Returns
    -------
    directory : Selected directory

    Examples
    --------
    >>> myDir = skinematics.ui.getdir('c:\\temp', 'Pick your directory')

    """

    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    directory = tkf.askdirectory(initialdir=default_name, title=dialog_title)

    # Close the Tk-window manager again
    root.destroy()

    if not os.path.exists(directory):
        return None
    else:
        return Path(directory)


def askquestion (dialog_title:str='Interactive Selection',
                 Question:str='Are we done yet?')->bool:
    """ Ask the user a yes/no question

    Parameters
    ----------
    dialog_title : Window title
    Question : Question to the user

    Returns
    -------
    yes_no : Selected answer

    Examples
    --------
    >>> my_wish = sksound.misc.askquestion('Work or Play', 'Do you want to go home?')

    """

    root = tkinter.Tk()
    root.withdraw()

    # On some systems, this dialog remains in the back
    # To overcome that, move it up. Unfortunately, this somehow also makes the
    # "root" visible again :(
    # To be fixed sometime ...
    to_top = tkinter.Toplevel(root)
    yes_no = messagebox.askyesno(title=dialog_title,
                                 message=Question, master=to_top)

    # Close the Tk-window manager again
    root.destroy()

    return yes_no


if __name__ == "__main__":
    # Test functions

    result = askquestion(dialog_title='Interactive choice',
                        Question='Are we done yet?')
    print('You have selected {0}'.format(result))


    import time
    for ii in progressbar(range(100), 'Computing ', 25):
        #print(ii)
        time.sleep(0.05)


    selected_get = get_file('*.eps', 'Testing file-selection', r'c:\temp\test.eps')
    if not selected_get:
        print('No file selected')
    else:
        print(f'File: {str(selected_get.name)}')
        print(f'Path: {str(selected_get.parent)}')
    selected_save = save_file('*.txt', 'Testing saving-selection', r'c:\temp\test.txt')

    my_dir = get_dir()
    print(f'Folder: {str(my_dir)}')

    """

    root = tkinter.Tk()
    app = Demo1(root, sys._getframe())
    root.mainloop()

    """
