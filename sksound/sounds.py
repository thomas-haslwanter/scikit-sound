"""
Python module to read, play, and write sound data.
For flexibility, FFMPEG is used for non-WAV files.

If you re-set the location of FFMPEG, please run the following code:

>>> ffmpeg = FFMPEG_info()
>>> ffmpeg.set()

You can obtain it for free from
    http://ffmpeg.org

Mac users using Anaconda should follow the instructions on

        https://anaconda.org/soft-matter/ffmpeg

    Otherwise, the tips under

        https://github.com/fluent-ffmpeg/node-fluent-ffmpeg/wiki/Installing-ffmpeg-on-Mac-OS-X

    seemed to work. Binaries are also available from

        - http://www.evermeet.cx/ffmpeg/ffmpeg-4.1.1.7z
        - http://www.evermeet.cx/ffplay/ffplay-4.1.1.7z

Note that FFMPEG must be installed externally, not as a Python package!!
Please install ffmpeg/ffplay in the following directory:

    - Windows:  "C:\\\\Program Files\\\\ffmpeg\\\\bin\\\\"
    - Mac:  	"/usr/local/bin/" (is already included in the default paths of the Mac terminal.)
    - Linux:	"/usr/bin/"

Compatible with Python >=3.5

"""

# Author: thomas haslwanter
# Date:   March-2021


# "ffmpeg" has to be installed externally, into the location listed below
# You can obtain it for free from http://ffmpeg.org

import numpy as np

from scipy.io.wavfile import read, write
import tempfile
import subprocess
import json
import time

import appdirs

# The following construct is required since I want to run the module as a script
# inside the sksound-directory
import os
import sys
file_dir = os.path.dirname(__file__)
if file_dir not in sys.path:
    sys.path.insert(0, file_dir)
    
import misc

from sksound import misc

# On Win playing sound works automatically
# For the other packages you need the module "pygame"

if sys.platform=='win32':
    import winsound
elif sys.platform == 'linux':
    import pygame


class NoFFMPEG_Error(Exception):
    pass


class FFMPEG_info:
    """

    Class for storing the config-info for FFMPEG.

    If first checks if FFMPEG is installed. FFMPEG is necessary to
    read MP3-files etc. Once checked, the corresponding information
    is saved in "ffmpeg.json", under "/FFMPEG_info/sksound/":

    FFMPEG_info properties:
        - config_file : JSON-file, with the config-information
        - ffmpeg : Commandline location of the command "ffmpeg"
        - ffplay : Commandline location of the command "ffplay"


    """

    def __init__(self):
        """Set the name of the config-file, and the properties
        "ffmpeg" and "ffplay" of the FFMPEG_info object"""
        
        app_name = 'FFMPEG_info'
        app_author = 'sksound'
        
        # The package "appdirs" allows an OS-independent implementation
        user_data_dir = appdirs.user_data_dir(app_name, app_author)
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)
        self.config_file =  os.path.join(user_data_dir, 'ffmpeg.json')
        
        if not os.path.exists(self.config_file):
            
            # Check if it is in the system path
            try:
                completed_process = subprocess.run('ffmpeg')
                completed_process = subprocess.run('ffplay')
                self.ffmpeg = 'ffmpeg'
                self.ffplay = 'ffplay'
            except FileNotFoundError:
                self.set()
        else:
            with open(self.config_file, 'r') as in_file:
                info = json.load(in_file)
                self.ffmpeg = info['ffmpeg']
                self.ffplay = info['ffplay']
        
                
    def set(self):
        """
        Set the config-filename, and write the FFMPEG_info
        properties "ffmpeg" and "ffplay" to that config-file.

        If FFMPEG is not installed, these are set to "None".
        """
        
        ffmpeg_installed = misc.askquestion(DialogTitle='FFMPEG Check',
                                           Question='Is FFMPEG installed?')
        
        if ffmpeg_installed:
            ffmpeg_dir = misc.get_dir(DialogTitle='Please select the directory where FFMPEG (binary) is installed:')
            
            if sys.platform=='win32':
                self.ffmpeg = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
                self.ffplay = os.path.join(ffmpeg_dir, 'ffplay.exe')
            else:
                self.ffmpeg = os.path.join(ffmpeg_dir, 'ffmpeg')
                self.ffplay = os.path.join(ffmpeg_dir, 'ffplay')
            
            if not os.path.exists(self.ffmpeg):
                print('Sorry, {0} does not exist!'.format(self.ffmpeg))
                return
            
            if not os.path.exists(self.ffplay):
                print('Sorry, {0} does not exist!'.format(self.ffplay))
                return
            
        else:
            self.ffmpeg = None
            self.ffplay = None
        
        # Save them to the default config file
        info = {'ffmpeg':self.ffmpeg, 'ffplay': self.ffplay}
        try:
            with open(self.config_file, 'w') as outFile:
                json.dump(info, outFile)
                print('Config information written to {0}'.format(os.path.abspath(self.config_file)))
        except PermissionError as e:
            curDir = os.path.abspath(os.curdir)
            print('Current directory: {0}'.format(curDir))
            print('Error: {0}'.format(e))
        
        return
    
    
class Sound:
    """

    Class for working with sound in Python.
    
    A Sound object can be initialized
        - by giving a filename
        - by providing "int16" data and a rate
        - without giving any parameter; in that case the user is prompted
          to select an infile

    Parameters
    ----------
    inFile : string
        path- and file-name of infile, if you get the sound from a file.
    inData: array
        manually generated sound data; requires "inRate" to be set, too.
    inRate: integer
        sample rate; required if "inData" are entered.

    Returns
    -------
    None :
        No return value. Initializes the Sound-properties.

    Notes
    -----
    For non WAV-files, the file is first converted to WAV using
    FFMPEG, and then read in. A warning is generated, to avoid
    unintentional deletion of existing WAV-files.
    
    SoundProperties:
        - source
        - data
        - rate
        - numChannels
        - totalSamples
        - duration
        - bitsPerSample

    SoundMethods:
        - generate_sound
        - get_info
        - play
        - read_sound
        - summary
        - write_wav
        
    Examples
    --------
    >>> from sksound.sounds import Sound
    >>> mySound1 = Sound()                  # here the user is prompted for an input file
    >>> mySound2 = Sound('test.wav')     # here the input file is provided directly
    >>>
    >>> rate = 22050
    >>> dt = 1./rate
    >>> freq = 440
    >>> t = np.arange(0,0.5,dt)
    >>> x = np.sin(2*np.pi*freq * t)
    >>> amp = 2**13
    >>> sounddata = np.int16(x*amp)
    >>> mySound3 = Sound(inData=sounddata, inRate=rate)

    """

    def __init__(self, inFile = None, inData = None, inRate = None):
        """ Initialize a Sound object """
        
        # Information about FFMPEG
        self.ffmpeg_info = FFMPEG_info()
        
        if inData is not None:
            if inRate is None:
                print('Set the "rate" to the default value (8012 Hz).')
                rate = 8012.0
            self.generate_sound(inData, inRate)
        else: 
            if inFile is None:
                inFile = self._selectInput()
                if inFile == 0:
                    return
            try:
                self.source = inFile
                self.read_sound(self.source)
            except FileNotFoundError as err:
                print(err)
                inFile = self._selectInput()
                self.source = inFile
                self.read_sound(self.source)
        
                
    def read_sound(self, inFile):
        """

        Read data from a sound-file.

        Parameters
        ----------
        inFile : string
            path- and file-name of infile

        Returns
        -------
        None :
            No return value. Sets the property "data" of the object.

        Notes
        -----
        * For non WAV-files, the file is first converted to WAV using
          FFMPEG, and then read in.
        * If FFMPEG is not installed, non-WAV files produce a "sounds.NoFFMPEG_Error"

        Examples
        --------
        >>> mySound = Sound('test.wav')
        >>> mySound.play()
        >>> mySound.read_sound('test2.wav') # If you want to read in another(!) file

        """

        # Python can natively only read "wav" files. To be flexible, use "ffmpeg" for conversion for other formats
        if not os.path.exists(inFile):
            print('{0} does not exist!'.format(inFile))
            raise FileNotFoundError
       
        (root, ext) = os.path.splitext(inFile)
        if ext[1:].lower() != 'wav':
            if self.ffmpeg_info.ffmpeg == None:
                print('Sorry, need FFMPEG for non-WAV files!')
                self.rate = None
                self.data = None
                raise NoFFMPEG_Error
                
            outFile = root + '.wav'
            cmd = [self.ffmpeg_info.ffmpeg, '-i', inFile, outFile, '-y']
            subprocess.run(cmd)
            print('Infile converted from ' + ext + ' to ".wav"')
            
            inFile = outFile
            self.source = outFile

        self.rate, self.data = read(inFile)
        
        # Set the filename
        self.source = inFile
        
        # Make sure that the data are in some integer format
        # Otherwise, e.g. Windows has difficulty playing the sound
        # Note that "self.source" is set to "None", in order to
        # play the correct, converted file with "play"
        if not np.issubdtype(self.data.dtype, np.integer):
            self.generate_sound(self.data, self.rate)
            
        self._setInfo()
        print('data read in!')


    def play(self):
        """
       Play the stored sound

       Parameters
       ----------
       None :

       Returns
       -------
       None :


       Notes
       -----
       On "Windows" the module "winsound" is used; on "Linux" I use
       "pygame"; and on "OSX" the terminal command "afplay".

       Examples
       --------
       >>> mySound = Sound('test.wav')
       >>> mySound.play()

        """

        try:
            if self.source is None:
                # If there is no source-file, write the data to a temporary WAV-file ...
                tmpFile = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                tmpFile.close()
                self.write_wav(tmpFile.name)
                
                # ... and play that file
                if sys.platform=='win32':
                    winsound.PlaySound(tmpFile.name, winsound.SND_FILENAME)
                elif sys.platform == 'darwin':
                    cmd = ['afplay', tmpFile.name]
                    subprocess.run(cmd)
                else:
                    pygame.init()
                    pygame.mixer.music.load(tmpFile.name)
                    pygame.mixer.music.play()
                    time.sleep(self.duration)
                    
                    # If you want to use FFMPEG instead, use the following commands:
                    #cmd = [self.ffmpeg_info.ffplay, '-autoexit', '-nodisp', '-i', tmpFile.name]
                    #subprocess.run(cmd)
                    
            elif os.path.exists(self.source):
                # If you have a given input file ...
                print('Playing ' + self.source)
                
                # ... then play that one
                if sys.platform == 'win32':
                    winsound.PlaySound(str(self.source), winsound.SND_FILENAME)
                elif sys.platform == 'darwin':
                    cmd = ['afplay', str(self.source)]
                    subprocess.run(cmd)
                else:
                    pygame.init()
                    pygame.mixer.music.load(self.source)
                    pygame.mixer.music.play()
                    time.sleep(self.duration)
                    
                    # If you want to use FFMPEG instead, use the following commands:
                    #cmd = [self.ffmpeg_info.ffplay, '-autoexit', '-nodisp', '-i', self.source]
                    #subprocess.run(cmd)
                    
        except SystemError:
            print('If you don''t have FFMPEG available, you can e.g. use installed audio-files. E.g.:')
            print('import subprocess')
            print('subprocess.run([r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe", r"C:\Music\14_Streets_of_Philadelphia.mp3"])')

            
    def generate_sound(self, data, rate):
        """ Set the properties of a Sound-object. """

        # If the data are not in an integer format (if they are e.g. "float"), convert
        # them to integer and scale them to a reasonable amplitude
        if not np.issubdtype(data.dtype, np.integer):
            defaultAmp = 2**13
            # Watch out with integer artefacts!
            data = np.int16(data * (defaultAmp / np.max(data)))
            
        self.data = data
        self.rate = rate
        self.source = None
        self._setInfo()

        
    def write_wav(self, full_out_file = None):
        """

        Write sound data to a WAV-file.

        Parameters
        ----------
        fullOutFile : string
            Path- and file-name of the outfile. If none is given,
            the user is asked interactively to choose a folder/name
            for the outfile.

        Returns
        -------
        None :
            

        Examples
        --------
        >>> mySound = Sound('test.wav')
        >>> mySound.write_wav()

        """

        if full_out_file is None:
            
            (out_file, out_dir) = misc.save_file(FilterSpec='*.wav', DialogTitle='Write sound to ...', 
                          DefaultName='')
            full_out_file = os.path.join(out_dir, out_file)
            if full_out_file is None:
                print('Output discarded.')
                return 0
        else:
            (out_file , out_dir) = os.path.split(full_out_file)

        write(str(full_out_file), int(self.rate), self.data)
        print('Sounddata written to ' + out_file + ', with a sample rate of ' + str(self.rate))
        print('OutDir: ' + out_dir)
        
        return full_out_file
    
    
    def get_info(self):
        """
        Return information about the sound.

        Parameters
        ----------
        None : 

        Returns
        -------
        source : name of inFile
        rate :   sampleRate
        numChannels : number of channels
        totalSamples : number of total samples
        duration : duration [sec]
        bitsPerSample : bits per sample
            
        Examples
        --------
        >>> mySound = Sound('test.wav')
        >>> info = mySound.get_info()
        >>> (source, rate, numChannels, totalSamples, duration, bitsPerSample) = mySound.get_info()

        """

        return (self.source,
                self.rate,
                self.numChannels,
                self.totalSamples,
                self.duration,
                self.dataType)

    
    def summary(self):
        """
        Display information about the sound.

        Parameters
        ----------
        None : 

        Returns
        -------
        None :
            
        Examples
        --------
        >>> mySound = Sound()
        >>> mySound.read_sound('test.wav')
        >>> mySound.summary()

        """

        import yaml
        
        (source, rate, numChannels, totalSamples, duration, dataType) = self.get_info()
        info = {'Source':source,
                'SampleRate':rate,
                'NumChannels':numChannels,
                'TotalSamples':totalSamples,
                'Duration':duration,
                'DataType':dataType}
        print(yaml.dump(info, default_flow_style=False))
        
        
    def _setInfo(self):
        """ Set the information properties of that sound """

        if len(self.data.shape)==1:
            self.numChannels = 1
            self.totalSamples = len(self.data)
        else:
            self.numChannels = self.data.shape[1]
            self.totalSamples = self.data.shape[0]
            
        self.duration = float(self.totalSamples)/self.rate # [sec]
        self.dataType = str(self.data.dtype)
        
    def _selectInput(self):
        """ GUI for the selection of an in-file. """

        (my_file, my_path) = misc.get_file(FilterSpec='*.wav', 
                                    DialogTitle='Select sound-input:', 
                                    DefaultName='')
        if my_path == 0:
            print('No file selected')
            return 0
        else:
            full_in_file = os.path.join(my_path, my_file)
            print('Selection: ' + full_in_file)
            return full_in_file

        
def main():
    """ Main function, to test the module """

    import os
    import numpy as np

    # Re-set FFMPEG
    # ffmpeg = FFMPEG_info()
    # ffmpeg.set()

    # Import a file, and play the sound
    # data_dir = r'/home/thomas/Coding/scikit-sound/sksound/tests'
    data_dir = 'tests'
    in_file = 'a1.wav'

    full_file = os.path.join(data_dir, in_file)
    try:
        # mySound = Sound(full_file)
        # mySound.play()
        # time.sleep(mySound.duration)
        mySound2 = Sound()
        mySound2.play()
    except NoFFMPEG_Error:
        pass

    # Test with self-generated data
    rate = 22050
    dt = 1./rate
    t = np.arange(0,0.5,dt)
    freq = 880
    x = np.sin(2*np.pi*freq*t)
    sounddata = np.int16(x*2**13)

    in_sound = Sound(inData=sounddata, inRate=rate)
    in_sound.summary()
    in_sound.play()
    time.sleep(in_sound.duration)

    print('hi')

    # Test if type conversion works
    in_sound2 = Sound(inData=x, inRate=rate)
    in_sound2.play()

    # Test with GUI
    in_sound = Sound()
    in_sound.play()
    print(in_sound.summary())
    out = in_sound.get_info()
    print(out)
    in_sound.write_wav()


if __name__ == '__main__':
    my_sound = Sound()
    #main()

