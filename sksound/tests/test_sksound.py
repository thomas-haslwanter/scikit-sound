import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import unittest

class TestSequenceFunctions(unittest.TestCase):
    
    def test_sksounds(self):
        for module in ['sounds']:
            print(dir(module))
