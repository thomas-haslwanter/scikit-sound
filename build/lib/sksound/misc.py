"""
Miscellaneous user interface utilities for

    - selecting files or directories.
      If nothing or a non-existing file/direcoty is selected, the return is "0". 
      Otherwise the file/directory is returned.
    - waitbar

"""

# author: Thomas Haslwanter; date: April-2021


import os
# import matplotlib.pyplot as plt
# plt.switch_backend('agg')

import sys

import tkinter 
import tkinter.filedialog as tkf
from tkinter import messagebox
    
    
def progressbar(it, prefix = "", size = 60):
    """
    Shows a progress-bar on the commandline.
    This has the advantage that you don't need to bother with windows
    managers. Nifty coding!
    
    Parameters
    ----------
    it : integer array
        index variable
    prefix : string
        Text preceding the progress-bar
    size : integer
        Length of progress-bar

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
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
#        sys.stdout.flush()
    
    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()
    
    
def get_file(FilterSpec='*', DialogTitle='Select File: ', DefaultName=''):
    """
    Selecting an existing file.
    
    Parameters
    ----------
    FilterSpec : query-string
        File filters
    DialogTitle : string
        Window title
    DefaultName : string
        Can be a directory AND filename
    
    Returns
    -------
    filename :  string
        selected existing file
    pathname:   string
        selected path
    
    Examples
    --------
    >>> (myFile, myPath) = skinematics.ui.getfile('*.py', 'Testing file-selection', 'c:\\temp\\test.py')
    
    """
    
    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    fullInFile = tkf.askopenfilename(initialfile=DefaultName,
            title=DialogTitle, filetypes=[('all files','*'), ('Select',
                FilterSpec)])
    
    # Close the Tk-window manager again
    root.destroy()
    
    if not os.path.exists(fullInFile):
        return (0, 0)
    else:
        print('Selection: ' + fullInFile)
        dirName = os.path.dirname(fullInFile)
        fileName = os.path.basename(fullInFile)
        return (fileName, dirName)
        
    
def save_file(FilterSpec='*',DialogTitle='Save File: ', DefaultName=''):
    """
    Selecting an existing or new file:
    
    Parameters
    ----------
    FilterSpec : string
        File filters.
    DialogTitle : string
        Window title.
    DefaultName : string
        Can be a directory AND filename.
    

    Returns
    -------
    filename : string
        Selected file.
    pathname : string
        Selecte path.
    

    Examples
    --------
    >>> (myFile, myPath) = skinematics.ui.savefile('*.py', 'Testing file-selection', 'c:\\temp\\test.py')

    """
    
    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    outFile = tkf.asksaveasfile(mode='w', title=DialogTitle, initialfile=DefaultName, filetypes=[('Save as', FilterSpec)])
    
    # Close the Tk-window manager again
    root.destroy()
    
    if outFile == None:
        (fileName, dirName) = (0,0)
    else:
        fullOutFile = outFile.name
        print('Selection: ' + fullOutFile)
        dirName = os.path.dirname(fullOutFile)
        fileName = os.path.basename(fullOutFile)
        
    return (fileName, dirName)


def get_dir(DialogTitle='Select Directory', DefaultName='.'):
    """ Select a directory
    
    Parameters
    ----------
    DialogTitle : string
        Window title
    DefaultName : string
        Can be a directory AND filename

    
    Returns
    -------
    directory : string
        Selected directory.

    
    Examples
    --------
    >>> myDir = skinematics.ui.getdir('c:\\temp', 'Pick your directory')
    
    """
    
    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    fullDir = tkf.askdirectory(initialdir=DefaultName, title=DialogTitle)
    
    # Close the Tk-window manager again
    root.destroy()
    
    if not os.path.exists(fullDir):
        return 0
    else:
        print('Selection: ' + fullDir)
        return fullDir

    
def askquestion (DialogTitle='Interactive Selection', Question='Are we done yet?'):
    """ Ask the user a yes/no question
    
    Parameters
    ----------
    DialogTitle : string
        Window title
    Question : string
        Question to the user

    
    Returns
    -------
    yes_no : boolean
        Selected answer.

    
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
    yes_no = messagebox.askyesno(title=DialogTitle, message=Question, master=to_top)
    
    # Close the Tk-window manager again
    root.destroy()
    
    return yes_no


if __name__ == "__main__":   
    # Test functions
    
    """
    result = askquestion(DialogTitle='Interactive choice', 
                        Question='Are we done yet?')
    print('You have selected {0}'.format(result))
    
    
    import time
    for ii in progressbar(range(50), 'Computing ', 25):
        #print(ii)
        time.sleep(0.05)
        

    (myFile, myPath) = get_file('*.eps', 'Testing file-selection', r'c:\temp\test.eps')
    if myFile == 0:          
        print(0)
    else:
        print('File: %s, Path: %s' % (myFile, myPath))
    (myFile, myPath) = save_file('*.txt', 'Testing saving-selection', r'c:\temp\test.txt')
        
    myDir = get_dir()
    print(myDir)

    
    root = tkinter.Tk()
    app = Demo1(root, sys._getframe())
    root.mainloop()

    """
