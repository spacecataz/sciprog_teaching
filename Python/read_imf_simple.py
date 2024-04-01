#!/usr/bin/env python3

'''
This script covers reading a basic IMF data file in Python. It does this
two ways: the first is a brute-force way with big loops, no `with` statement,
and hard indexing to move through variables.

The second way is the same thing cleaned up a bit.

For teaching: I walk through the first one as an example and clean it up
while walking through it again.
'''


# In python, we import useful modules first.  If the module names
# are long, we can give them aliases.  All the functions, classes,
# etc. inside of that loaded module are preceeded by the module name
# or alias.
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt


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


def format_ax(ax, ylabel=None):
    '''
    Format an axes object, *ax*, to quickly add labels, change time ticks to
    sensible values, turn off xtick labels unless we're on the bottom
    row of plots, and set the y-axis label to kwarg *ylabel*

    Example usage: format_ax(axis, ylabel='some label string')
    '''

    import matplotlib.dates as mdt

    # Better tick spacing: This looks pedantic, but is very, very powerful.
    # Use locator objects (special objects that find where to put ticks) to
    # set tick locations.  Use formatter objects to set the format of the
    # tick labels.  Because we don't know how long our file is, let's use
    # some "if" statements to keep things from blowing up.
    # Start by calculating the time spanned by the x-axis (in days):
    span = ax.get_xlim()[-1] - ax.get_xlim()[0]

    # Apply different cases based on typical scenarios:
    if span < 5:  # less than five days?  Go by hour:
        Mtick = mdt.HourLocator(byhour=[0, 6, 12, 18])
        mtick = mdt.HourLocator(byhour=range(24))
        fmt = mdt.DateFormatter('%H:%M UT')
    else:
        # Default to AutoDateFormatter.
        Mtick = mdt.AutoDateLocator()
        mtick = mdt.AutoDateLocator()
        fmt = mdt.AutoDateFormatter(Mtick)

    # Apply those to our axes.  Note that the axes objects contain
    # axis objects for the x axis and y axis.  We can edit single
    # axes so they look different!
    ax.xaxis.set_major_locator(Mtick)
    ax.xaxis.set_minor_locator(mtick)
    ax.xaxis.set_major_formatter(fmt)

    # Turn on the grid:
    ax.grid()

    # Set ylabel, if set:
    if ylabel:
        ax.set_ylabel(ylabel, size=16)

    # Kill some labels.  Get the list of label objects and turn some off.
    labels = ax.get_yticklabels()  # Get the labels...
    labels[-1].set_visible(False)  # Turn off the first.
    labels[0].set_visible(False)   # Turn off the 2nd.

    # Determine the axes' subplot location.  Use this to determine if we're in
    # the bottom row of plots.
    spec = ax.get_subplotspec()
    # Subplot specs have a nice method for determining if we're in the last row
    is_bottom = spec.is_last_row()

    # If we're in the bottom row, label the axes with the date and time.
    if is_bottom:
        # Get time limits, as floating point numbers,  from our axes object:
        tStart, tEnd = ax.get_xlim()  # returns range of x-axes.
        # Convert tStart into a datetime:
        tStart = mdt.num2date(tStart)
        # Note how Datetime objects have methods to pretty-print the time!
        ax.set_xlabel(f'Time from {tStart.isoformat()}', size=18)
    else:
        # No labels on any axis except the bottom plot.  Set the list of
        # labels to an empty list for no labels (but keep ticks!)
        ax.xaxis.set_ticklabels([])


def plot_imf(filename, outname=None, style='seaborn-v0_8-dark'):
    '''
    Read and plot imf file *filename* to screen.
    If kwarg *outname* is given, plot is saved to file using *outname* as the
    output file name.

    The Matplotlib style sheet can be set with the keyword *style*.
    '''

    # Pick style sheet to use:
    plt.style.use(style)

    # Load the data as we did last time.
    data = read_imf(filename)

    # Create a figure object.  This will hold all of our axes objects.
    # Think of this as the paper on which we write.
    # Use *figsize* to set the size in inches (metric is possible, too.)
    fig = plt.figure(figsize=(8.5, 11))
    # "subplots_adjust" sets figure spacing.  Use the interactive plot window
    # to find your best spacing values, then paste 'em here!
    # Alternatively, we can use "fig.tight_layout()"
    fig.subplots_adjust(hspace=0.001, right=0.96, top=0.93, left=0.13,
                        bottom=0.07)

    # Add subplots to the figure object.  Use a three-digit code to specify
    # the number of rows, columns, and finally which position to use.
    # Each Axes is an object that we save as a variable.
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(413)
    ax3 = plt.subplot(414)

    # Put the title on the top axis.  Note how we edit the axes using
    # object-method syntax.
    ax1.set_title(filename)

    # TOP AXES: IMF
    # Create the IMF By, Bz plot.  Note how we call the object methods
    # that belong to the axes we want to edit.  "label" sets the legend
    # label.  There are MANY kwargs that customize plots!
    ax1.plot(data['time'], data['by'], 'c--', label='$B_{Y}$')
    ax1.plot(data['time'], data['bz'], 'b',   label='$B_{Z}$')

    # Create a legend!  The legend command is very flexible, check out the
    # docstring to see how it works.
    ax1.legend(loc='upper right', ncol=2)

    # Horizontal lines!  Must specify the y, xStart and xEnd.  lw is width.
    ax1.hlines(0, data['time'][0], data['time'][-1], colors='k',
               linestyles='dashed', lw=2.0)

    # Call our format function to cleanup and label our axes.
    format_ax(ax1, 'IMF ($nT$)')

    # MIDDLE AXES: NUMBER DENSITY
    ax2.plot(data['time'], data['rho'], 'r-')
    format_ax(ax2, r'$\rho$ ($cm^{-3}$)')

    # BOTTOM AXES: VELOCITY
    ax3.plot(data['time'], -1*data['vx'], 'g-')
    format_ax(ax3, r'$V_{X}$ ($\frac{km}{s}$)')

    # Finally, either save or show the plot.
    if outname:
        fig.savefig(outname)
    else:
        plt.show()


# MAIN PROGRAM: This chunk of code only executes on run, not on import.
if __name__ == '__main__':
    filename = input('Enter IMF filename to read and plot: ')
    plot_imf(filename)