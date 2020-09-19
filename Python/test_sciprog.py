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
    knownTime1 = dt.datetime(2005, 8, 31, 8, 59, 49)
    knownTime2 = dt.datetime(2005, 9,  2, 2,  0, 13)

    # First and last lines in our file:
    knownVals1 = [-6.47, 0.83, 14.46, -399.57,  -6.43, -15.27, 12.79, 45781.6]
    knownVals2 = [-5.18, 0.71, -1.67, -419.93, -30.28, -37.11,  6.46, 77399.5]

    # Use object methods to create individual tests:
    def test_read(self):
        ''' Test our ability to read the sample file '''

        data = sciprog.read_imf('./imf_full.dat')

        for t_ans, t_read in zip([self.knownTime1, self.knownTime2],
                                 [data['time'][0], data['time'][-1]]):
            self.assertEqual(t_ans, t_read)
        
if __name__=='__main__':
    unittest.main()
