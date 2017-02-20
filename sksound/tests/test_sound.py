import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import sounds 
import unittest
import numpy as np

class TestSequenceFunctions(unittest.TestCase):
    
    def test_sound_generate(self):
        # Test with self-generated data
        rate = 22050
        dt = 1./rate
        t = np.arange(0,0.5,dt)
        freq = 880
        x = np.sin(2*np.pi*freq*t)
        sounddata = np.int16(x*2**13)
        inSound = sounds.Sound(inData=sounddata, inRate=rate)
        inSound.play()
        
        # Test if type conversion works
        inSound2 = sounds.Sound(inData=x, inRate=rate)
        inSound2.play()
        
    def test_sound_read(self):
        # Single channel, stereo, and mp3 input
        sound_files = ['peas.wav', 'tiger.wav', 'YouAreNotIt.mp3']
        for file in sound_files:
            try:
                inSound = sounds.Sound(file)
                inSound.play()
            except sounds.NoFFMPEG_Error:
                pass
        
    def test_sound_select(self):
        # Test with GUI
        inSound = sounds.Sound()
        inSound.play()
        print('hi')
        
        # Info about sound, and its display
        (source, rate, numChannels, totalSamples, duration, bitsPerSample) = inSound.get_info()
        inSound.summary()
        print('ho')
        
    def test_sound_write(self):
        # Test with self-generated data
        rate = 22050
        dt = 1./rate
        t = np.arange(0,0.5,dt)
        freq = 880
        x = np.sin(2*np.pi*freq*t)
        sounddata = np.int16(x*2**13)
        inSound = sounds.Sound(inData=sounddata, inRate=rate)
        
        # Write sound-data
        inSound.write_wav()
        
if __name__ == '__main__':
    unittest.main()
    
