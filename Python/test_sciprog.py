#!/usr/bin/env python
'''
Test suite for the SciProg module for Introduction to Scientific Programming.

This script uses Python's built in test suite module, `unittest`.
For more information, see:
https://docs.python.org/3/library/unittest.html
'''

import numpy as np
import datetime as dt
import unittest

import sciprog

# All test classes in this file:
#__all__ = []

# Define test case classes to group related tests together:
class TestReadImf(unittest.TestCase):
    '''
    Test that our read_imf function properly reads and parses data.
    '''

    # Set up constants, answers, and other items as object attributes.
    # For convenience:
    varnames = ['bx','by','bz', 'vx','vy','vz', 'rho', 'temp']

    #### Answers ####
    # First and last times in file:
    knownTime1 = dt.datetime(1998,  1,  1,  1, 0, 0)
    knownTime2 = dt.datetime(2015, 12, 31, 23, 0, 0)

    # First and last lines in our file:
    knownVals1 = [0.00, 1.00,  0.00, -500.00, 0.00, 0.00, 5.00, 50000.0]
    knownVals2 = [0.00, 0.00, -1.00, -500.00, 0.00, 0.00, 5.00, 50000.0]

    # Use object methods to create individual tests:
    def test_read(self):
        ''' Test our ability to read the sample file '''

        data = sciprog.read_imf('./imf_test.dat')

        for t_ans, t_read in zip([self.knownTime1, self.knownTime2],
                                 [data['time'][0], data['time'][-1]]):
            self.assertEqual(t_ans, t_read)
        
if __name__=='__main__':
    unittest.main()
