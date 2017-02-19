'''
Python module to read, play, and write sound data.
For flexibility, FFMPEG is used for non-WAV files.

If you re-set the location of FFMPEG, please run the following code:

>>> ffmpeg = FFMPEG_info()
>>> ffmpeg.set()
    
You can obtain it for free from
    http://ffmpeg.org
    
Mac users using Anaconda should follow the instructions on

        https://anaconda.org/soft-matter/ffmpeg

    Otherwise, the tups under

        https://github.com/fluent-ffmpeg/node-fluent-ffmpeg/wiki/Installing-ffmpeg-on-Mac-OS-X

    seemed to work. Binaries are also available from

        - http://www.evermeet.cx/ffmpeg/ffmpeg-2.1.4.7z
        - http://www.evermeet.cx/ffplay/ffplay-2.1.4.7z

Note that FFMPEG must be installed externally!
Please install ffmpeg/ffplay in the following directory:

    - Windows:  "C:\\\\Program Files\\\\ffmpeg\\\\bin\\\\"
    - Mac:  	"/usr/local/bin/" (is already included in the default paths of the Mac terminal.)
    - Linux:	"/usr/bin/"

Compatible with Python 2.x and 3.x

'''

'''
Date:   Feb-2017
Ver:    0.1
Author: thomas haslwanter

'''


# "ffmpeg" has to be installed externally, into the location listed below
# You can obtain it for free from http://ffmpeg.org

import numpy as np
import os
import sys
from scipy.io.wavfile import read, write
import tempfile
import subprocess
import json
import appdirs
import easygui
import sounddevice

# The following construct is required since I want to run the module as a script
# inside the thLib-directory
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# On Win playing sound works automatically
# For the other packages you need the module "sounddevice"
import sounddevice

if sys.platform=='win32':
    import winsound
    
    
class FFMPEG_info:
    '''
    Class for storing the config-info for FFMPEG.
    
    If first checks if FFMPEG is installed. FFMPEG is necessary to
    read MP3-files etc. Once checked, the corresponding information
    is saved in "ffmpeg.json", under "/FFMPEG_info/sksound/":
    
    FFMPEG_info properties:
        - config_file : JSON-file, with the config-information
        - ffmpeg : Commandline location of the command "ffmpeg"
        - ffplay : Commandline location of the command "ffplay"
    
    
    '''

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
        
        ffmpeg_installed = easygui.ynbox(msg="Is FFMPEG installed?")
        if ffmpeg_installed:
            ffmpeg_dir = easygui.diropenbox(msg='Please select the directory where FFMPEG (binary) is installed:')
            
            self.ffmpeg = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
            self.ffplay = os.path.join(ffmpeg_dir, 'ffplay.exe')
            
            
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
    '''
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

    Examples
    --------
    >>> from thLib.sounds import Sound
    >>> mySound1 = Sound()
    >>> mySound2 = Sound('test.wav')
    >>>
    >>> rate = 22050
    >>> dt = 1./rate
    >>> freq = 440
    >>> t = np.arange(0,0.5,dt)
    >>> x = np.sin(2*np.pi*freq * t)
    >>> amp = 2**13
    >>> sounddata = np.int16(x*amp)
    >>> mySound3 = Sound(inData=sounddata, inRate=rate)

    '''
    

    def __init__(self, inFile = None, inData = None, inRate = None):
        '''Initialize a Sound object '''
        
        # Information about FFMPEG
        self.info = FFMPEG_info()
        
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
        '''
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

        Examples
        --------
        >>> mySound = Sound()
        >>> mySound.read_sound('test.wav')

        '''
        
        # Python can natively only read "wav" files. To be flexible, use "ffmpeg" for conversion for other formats
        if not os.path.exists(inFile):
            print('{0} does not exist!'.format(inFile))
            raise FileNotFoundError
       
        (root, ext) = os.path.splitext(inFile)
        if ext[1:].lower() != 'wav':
            if self.info.ffmpeg == None:
                print('Sorry, need FFMPEG for non-WAV files!')
                exit()
                
            outFile = root + '.wav'
            cmd = [self.info.ffmpeg, '-i', inFile, outFile, '-y']
            subprocess.run(cmd)
            print('Infile converted from ' + ext + ' to ".wav"')
            
            inFile = outFile
            self.source = outFile

        self.rate, self.data = read(inFile)
        self._setInfo()
        print('data read in!')
    

    def play(self):
        '''
        Play the stored sound

        Parameters
        ----------
        None : 

        Returns
        -------
        None :
            

        Notes
        -----
        On "Windows" the module "winsound" is used; on other
        platforms, the sound is played using "ffplay" from FFMPEG.

        Examples
        --------
        >>> mySound = Sound()
        >>> mySound.read_sound('test.wav')
        >>> mySound.play()

        '''

        try:
            if self.source is None:
                tmpFile = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                tmpFile.close()
                self.write_wav(tmpFile.name)
                if sys.platform=='win32':
                    winsound.PlaySound(tmpFile.name, winsound.SND_FILENAME)
                else:
                    cmd = [self.info.ffplay, '-autoexit', '-nodisp', '-i', tmpFile.name]
                    subprocess.run(cmd)
            elif os.path.exists(self.source):
                print('Playing ' + self.source)
                if sys.platform=='win32':
                    winsound.PlaySound(str(self.source), winsound.SND_FILENAME)
                else:
                    cmd = [self.info.ffplay, '-autoexit', '-nodisp', '-i', self.source]
                    subprocess.run(cmd)
        except SystemError:
            print('If you don''t have FFMPEG available, you can e.g. use installed audio-files. E.g.:')
            print('import subprocess')
            print('subprocess.run([r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe", r"C:\Music\14_Streets_of_Philadelphia.mp3"])')
            

    def generate_sound(self, data, rate):
        ''' Set the properties of a Sound-object. '''

        # If the data are in another format, e.g. "float", convert
        # them to integer and scale them to a reasonable amplitude
        if not type(data[0]) == np.int16:
            defaultAmp = 2**13
            # Watch out with integer artefacts!
            data = np.int16(data * (defaultAmp / np.max(data)))
            
        self.data = data
        self.rate = rate
        self.source = None
        self._setInfo()


    def write_wav(self, full_out_file = None):            
        '''
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
        >>> mySound = Sound()
        >>> mySound.read_sound('test.wav')
        >>> mySound.write_wav()

        '''

        if full_out_file is None:
            full_out_file = easygui.filesavebox(msg='Write sound to ....', default='*.wav', 
                               filetypes=['*.wav'])
            if full_out_file is None:
                print('Output discarded.')
                return 0
            else:
                (outFile , outDir) = os.path.split(full_out_file)

                write(str(full_out_file), int(self.rate), self.data)
                print('Sounddata written to ' + outFile + ', with a sample rate of ' + str(self.rate))
                print('OutDir: ' + outDir)

                return full_out_file
    
    def get_info(self):
        '''
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
        >>> mySound = Sound()
        >>> mySound.read_sound('test.wav')
        >>> info = mySound.get_info()
        >>> (source, rate, numChannels, totalSamples, duration, bitsPerSample) = mySound.info()

        '''
        
        return (self.source,
                self.rate,
                self.numChannels,
                self.totalSamples,
                self.duration,
                self.dataType)

    def summary(self):
        '''
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

        '''
        
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
        '''Set the information properties of that sound'''
            
        if len(self.data.shape)==1:
            self.numChannels = 1
            self.totalSamples = len(self.data)
        else:
            self.numChannels = self.data.shape[1]
            self.totalSamples = self.data.shape[0]
            
        self.duration = float(self.totalSamples)/self.rate # [sec]
        self.dataType = str(self.data.dtype)
        
    def _selectInput(self):
        '''GUI for the selection of an in-file. '''

        full_in_file = easygui.fileopenbox(msg='Select sound-input:', default='*.wav', 
                                          filetypes=['*.wav', '*.mp3'])
        if full_in_file is None:
            print('No file selected')
            return 0
        else:
            print('Selection: ' + full_in_file)
            return full_in_file

def main():
    ''' Main function, to test the module '''
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Re-set FFMPEG
    #ffmpeg = FFMPEG_info()
    #ffmpeg.set()
    
    ### Import a file, and play the sound
    #dataDir = r'C:\Users\p20529\Documents\Teaching\ETH\CSS\Exercises\Ex_Auditory\sounds\mp3'
    #inFile = 'tiger.mp3'
    
    #fullFile = os.path.join(dataDir, inFile)
    #mySound = Sound(fullFile)
    #mySound.play()
    
    ## Test with self-generated data
    #rate = 22050
    #dt = 1./rate
    #t = np.arange(0,0.5,dt)
    #freq = 880
    #x = np.sin(2*np.pi*freq*t)
    #sounddata = np.int16(x*2**13)
    
    #inSound = Sound(inData=sounddata, inRate=rate)
    #inSound.summary()
    #inSound.play()
    
    ## Test if type conversion works
    #inSound2 = Sound(inData=x, inRate=rate)
    #inSound2.play()
    
    # Test with GUI
    inSound = Sound()
    inSound.play()
    print(inSound.summary())
    #out = inSound.get_info()
    #print(out)
    #inSound.write_wav()
    
if __name__ == '__main__':
    main()
    
