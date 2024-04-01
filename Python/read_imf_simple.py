#!/usr/bin/env python3

'''
This script covers reading a basic IMF data file in Python. It does this
two ways: the first is a brute-force way with big loops, no `with` statement,
and hard indexing to move through variables.

The second way is the same thing cleaned up a bit.

For teaching: I walk through the first one as an example and clean it up
while walking through it again.
'''

def read_imf_simple(infile, debug=False):
    '''
    This function reads an SWMF-formatted IMF/solar wind file and parses it
    into a special data structure.

    Usage:
    >>>data = read_imf('some_file_name.dat')

    The returned value is a dictionary of values read from the file.

    The *debug* kwarg, if set to **True**, will create debug print outs.

    This function serves as a simple example; in real-life, creating a class
    that knows how to read, write, and plot these types of files is way more
    useful!
    '''

    # In python, we import useful modules first.  If the module names
    # are long, we can give them aliases.  All the functions, classes,
    # etc. inside of that loaded module are preceeded by the module name
    # or alias.
    import numpy as np
    import datetime as dt

    # Check our arguments, raise "exceptions" (errors) if something is wrong.
    if not isinstance(infile, str):
        raise TypeError('Input file name must be a string.')

    # Open the file in read-only mode by creating a file object.
    f = open(infile, 'r')

    # Read the very first line. Python will remember our
    # position in the file so that no lines are read twice.
    line = f.readline()

    # These files have a lot of header information.  We want to skip that.
    # We know, a priori, that the data begins after the "#START" text.
    # Let's loop through the first lines until we hit that line.
    # When comparing two strings, we want to cut off leading and trailing
    # blanks.  We do that with the "strip" object method.
    while line.strip() != '#START':
        line = f.readline()

    # DEBUG:
    if debug:
        print(f'DEBUG: Our last header line was {line}')

    # At this point, we should be at the line where the data starts.
    # We can load the rest of the lines by using the "readlines()" (note the
    # s) to slurp all remaining lines.  Slurp is a term that means "read the
    # whole damn file."
    lines = f.readlines()

    # We're now done with this file, so close it.
    f.close()

    # How many lines do we have?  The "len()" function will tell us!
    nLines = len(lines)

    # Now we can make a container for our data.  Our container will be a
    # dictionary.  Each variable (time, bx, by, etc.) will be an key with
    # the corresponding value a vector of values.  One way to set it up is:
    data = {}  # empty dictionary.
    keys = ['bx', 'by', 'bz', 'vx', 'vy', 'vz', 'rho', 't']
    data['time'] = np.zeros(nLines, dtype=object)  # a vector of time objects!
    # Repeat for all of our variables.
    data['bx'] = np.zeros(nLines)
    data['by'] = np.zeros(nLines)
    data['bz'] = np.zeros(nLines)
    data['vx'] = np.zeros(nLines)
    data['vy'] = np.zeros(nLines)
    data['vz'] = np.zeros(nLines)
    data['rho'] = np.zeros(nLines)
    data['t'] = np.zeros(nLines)

    if debug:
        print('DEBUG: Our data dictionary looks like this:')
        for key in data:
            print(f'\t{key}:\t{data[key]}')

    # We now have a container of the correct size and type for all our values.
    # We knew the keys a priori; it's possible and easy to get the list of
    # values from the file if it's listed in the file.

    # Now, to parse.  This is just a matter of splitting the line into parts,
    # turning them into floats or ints.  Special care must be taken with time
    # because we want datetime objects (Python's special time variables.)
    # Start by looping through all lines:
    for i, l in enumerate(lines):
        # Split up the line into parts:
        parts = l.split()
        # Handle time first.  We need the first 7 values from the line (year
        # through milisecond) and we need to turn them into ints and hand them
        # to the datetime module to make a datetime object.  We put the
        # datetime object into our time vector like so:
        # METHOD ONE: BRUTE FORCE.  When all else fails, do this:
        # for each part of the date and time, convert the string into an
        # integer, and use them to build the datetime object by hand.
        data['time'][i] = dt.datetime(int(parts[0]),  # year
                                      int(parts[1]),  # month
                                      int(parts[2]),  # day
                                      int(parts[3]),  # hour
                                      int(parts[4]),  # minute
                                      int(parts[5]),  # second
                                      int(parts[6])/1000  # microsec
                                      )

        # We can now go through the rest of the parts and put them into
        # the right spots in our arrays.  Loop it!
        # The "brute force" way to do this would be to do use an index
        # to get the right value for the right variable name:
        for j in range(len(keys)):
            k = keys[j]     # Get our variable name as a dict key
            p = parts[7+j]  # Get value; the 7 is to skip the time variables!
            data[k][i] = p  # Put right value in right spot.

    # That's it!  Our data dictionary is full.  Return it to the user.
    # You could plot a value by typing:
    # >>>import matplotlib.pyplot as plt
    # >>>plt.plot(data['time'], data['bz'])
    return data


def read_imf(infile, debug=False):
    '''
    This function reads an SWMF-formatted IMF/solar wind file and parses it
    into a special data structure.

    Usage:
    >>>data = read_imf('some_file_name.dat')

    The returned value is a dictionary of values read from the file.

    The *debug* kwarg, if set to **True**, will create debug print outs.

    This function serves as a simple example; in real-life, creating a class
    that knows how to read, write, and plot these types of files is way more
    useful!
    '''

    # In python, we import useful modules first.  If the module names
    # are long, we can give them aliases.  All the functions, classes,
    # etc. inside of that loaded module are preceeded by the module name
    # or alias.
    import numpy as np
    import datetime as dt

    # Check our arguments, raise "exceptions" (errors) if something is wrong.
    if not isinstance(infile, str):
        raise TypeError('Input file name must be a string.')

    # AN IMPORTANT NOTE: THE "WITH" STATEMENT.
    # "with" is a code block used to wrap actions that have distinct
    # "enter" and "exit" actions.  For example, when we open a file,
    # the enter action is to create a file object that is connected to
    # a file, open that file, and create the file pointer.  On exit,
    # we need to close that file as the "exit" action.  If there's an
    # error, it's possible that the code ends without ever performing the
    # exit action.  "with" blocks solve this existential problem.
    # For more information, see:
    # https://docs.python.org/3/reference/compound_stmts.html#with
    # We will use "with" in the reimplementation of this (below).

    # Open file, parse header, slurp lines:
    with open(infile, 'r') as f:
        # Get first line:
        line = f.readline()

        # Skip our header:
        while '#START' not in line:
            line = f.readline()

        # DEBUG:
        if debug:
            print(f'DEBUG: Our last header line was {line}')

        # Slurp remainder.
        lines = f.readlines()

    # How many lines do we have?  The "len()" function will tell us!
    nLines = len(lines)

    # Now we can make a container for our data.
    data = {}  # empty dictionary.
    keys = ['bx', 'by', 'bz', 'vx', 'vy', 'vz', 'rho', 'temp']
    data['time'] = np.zeros(nLines, dtype=object)  # a vector of time objects!
    # All other values as a vector of floats:
    for k in keys:
        data[k] = np.zeros(nLines)

    if debug:
        print('DEBUG: Our data dictionary looks like this:')
        for key in data:
            print(f'\t{key}:\t{data[key]}')

    # Now, to parse:
    for i, l in enumerate(lines):
        # Split up the line into parts:
        parts = l.split()

        # Use the datetime.strptime method to build straight
        # from the string.  Note that we don't always know how much white
        # space there will be between entries, so let's rebuild the string
        # from our parts list:
        tNow = ' '.join(parts[:6])
        data['time'][i] = dt.datetime.strptime(tNow, '%Y %m %d %H %M %S')
        # These format codes are described here:
        # https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior

        # A much more "pythonic" way (elegant in the python style) is to
        # simultaneously iterate over both your keys and values at once:
        for k, p in zip(keys, parts[7:]):
            data[k][i] = p

    # Return data to user.
    return data
