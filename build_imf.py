#!/usr/bin/env python
'''
This script obtains ACE upstream observations from NASA's CDAWeb FTP server
and uses IDL subroutines to convert them into SWMF input files.  Only one
day worth of observations can be converted at a time.

This script requires IDL and the Ridley IDL script library.

Sept. 2019: Updated for Python 3.
'''

# Start by importing only our Argparser.  We don't need anything
# else YET...
from argparse import ArgumentParser

# Instantiate and build our argument parser.  This follows what we did
# for the Minimal Substorm Model.  See online docs for more info:
# https://docs.python.org/3/library/argparse.html
parser = ArgumentParser(description=__doc__)
# Add arguments:
parser.add_argument('date', help='Date to fetch solar wind data in YYYYMMDD'+
                    ' format.', type=str)
parser.add_argument('--save', '-s', help='Save intermediary files' +
                    ' Default behavior is to delete downloaded files.',
                    action='store_true')
parser.add_argument('--debug', '-d', help='Turn on debug output.',
                    action='store_true')
parser.add_argument('--verbose', '-v', help='Turn on verbose output',
                    action='store_true')

# Get args from caller, collect arguments into a convenient object:
args = parser.parse_args()

# If we are in debug mode, we want lots and lots of output!
# Therefore, we turn on verbose mode and save mode, too:
if args.debug:
    args.verbose=True
    args.save=True

# Main program imports:
# To save time in "help mode", only import these after parsing options.
import os
import re
import urllib
import datetime as dt
from subprocess import PIPE, Popen

# A NOTE ON URLLIB: In python 3, this is just urllib.  Other items within
# urllib and urllib2 (in Python 2) have been reorganized within urllib
# in Python 3.  Check the official python docs.

# Ensure that the date is of the correct format.
# "try" does some commands.  If they fail, the program executes the
# "except" block instead of crashing.  With the except block, we can
# specify what exceptions to catch.  This keeps our program from
# ignoring ALL problems.  Sometimes, crashing is good!
# List of possible exceptions can be found here:
# https://docs.python.org/2/library/exceptions.html
try:
    # Try to parse date into datetime object.
    time = dt.datetime.strptime(args.date, '%Y%m%d')
except ValueError:  # Specify the type of exception to be specific!
    # If we can't, stop the program and print help.
    print('ERROR: Could not parse date!')
    print(__doc__)
    exit()

# In verbose mode, we print a lot of info to the screen:
if args.verbose:
    print('Fetching ACE data for {0:%Y-%m_d}...'.format(time))

# Build URL for obtaining SWEPAM file using the ".format" syntax described
# at http://docs.python.org/2/library/string.html#format-string-syntax
base = r'https://cdaweb.gsfc.nasa.gov/pub/data/ace/'
urlSwe = base + 'swepam/level_2_cdaweb/swe_h0/{0.year}/'.format(time)
urlMag = base + 'mag/level_2_cdaweb/mfi_h0/{0.year}/'.format(time)

# If verbose, tell user what we've found:
if args.verbose:
    print('\tSearching for CDFs at:\n\t{}\n\t{}'.format(urlSwe, urlMag))
    
# We want to check that the CDFs exist on the web.  To do this, we want
# to read the website and search for file name.  But we don't know the 
# file name because the version number could be anything and changes 
# arbitrarily.  We do know, however, that the date as YYYYMMDD should be
# in each file name, so let's search for that.

# Open our website.  Using "with" to set the context of our read,
# read all lines (as bytes), convert into a list of strings
# (emulating the "readlines" function.)
with urllib.request.urlopen(urlSwe) as response:
   filelist = re.findall('ac_h\d_swe_\d+_v\d+\.cdf',str(response.read()))
#filelist = str(urllib.request.urlopen(urlSwe).read())

# In debug mode, dump html contents to file.
if args.debug:
    out = open('html_raw_1.txt', 'w')

# A variable to hold the file name, defaulting to "none".
found = None
for l in filelist:
    # In debug mode, dump html file to disk.
    if args.debug: out.write(l)
    
    # Search for date in the current line.
    # We know that args.date is in the right format...
    if args.date in l:
        # The file name is the last part of the line.
        # Split up the line and save the last part.
        found = l.split()[-1]
        break  # Stop reading the website by leaving the loop.

# Outside of this loop, we now have the complete url of our target file.
if found:
    urlSwe += found
else:
    # If we never found it, it doesn't exist.  Raise an exception to
    # tell user what the problem is:
    raise ValueError('ERROR: SWEPAM file not found on server.')

# Repeat this for the magnetometer data.
with urllib.request.urlopen(urlMag) as response:
    filelist = re.findall('ac_h\d_mfi_\d+_v\d+\.cdf',str(response.read()))
found = False

if args.debug:
    out.close()
    # Open new one:
    out = open('html_raw_2.txt', 'w')
# Get file URL from list...
for l in filelist:
    if args.debug: out.write(l)

    if args.date in l:
        found = l.split()[-1]
        break
# Close debug file...
if args.debug: out.close()
# build complete URL.
if found:
    urlMag += found
else:
    raise ValueError('ERROR: MAGNETOMETER file not found on server.')

if args.verbose:
    print('\tFetching CDFs:\n\t{}\n\t{}'.format(urlSwe, urlMag))

# Download actual files.
# Though more complicated, this way is FAR FASTER than the older urlretrieve.
# We are looping through a list of urls and a list of output file names...
for url, f in zip( (urlSwe, urlMag), ('./swefile.cdf', './magfile.cdf')): 
    cdf = open(f, 'wb')             # Open file...
    download = urllib.request.urlopen(url) # Open website...
    cdf.write(download.read())      # "read" reads whole file, "write" saves it.
    cdf.close()                     # Close our saved CDF.

# Build a string of characters to send to IDL.
# These are the commands that you would type manually.
# Note the return characters (\n)!  These are important!
command_string = '.r cdf_to_mhd\n' + \
                 'magfile.cdf\n'   + \
                 'i\n'             + \
                 'imf_{0.year}{0.month}{0.day}.dat\n'.format(time) + \
                 'swefile.cdf\n'   + \
                 'd\n'             + \
                 'print, "HELP PYTHON HAS ME!"\n' + \
                 'exit\n'

if args.debug:
    print("Here are the commands being sent to IDL:")
    print(command_string)

# This next section is discussed in depth here:
# https://docs.python.org/2/library/subprocess.html
# Now, open a pipe to idl.  We are telling python to turn IDL's standard in
# to a pipe connected to python.
idl = Popen('idl', stdin=PIPE, text=True)

# You don't have the IDL script, so this won't work for you
idl.communicate(command_string)

# Close the program:
idl.terminate()

# Unless we are in "save" mode, remove downloaded files.
if not args.save:
    # The os module has useful functions for handling files:
    os.remove('./swefile.cdf')
    os.remove('./magfile.cdf')
