#!/usr/bin/env python
'''
A module that contains all of the classes and functions used in 
Introduction to Scientfic Programming 
Umich Course CLASP605 (2012-2018)
UT Arlington Course PHYS 5391 (2020-...)

To use, put this file in a place where Python can find it.  To see Python's
search path, type this in the python terminal:
>>>from sys import path
>>>print(path)
To change the path, set the environment variable $PYTHONPATH in your shell.
Here, in BASH, I add my own python stuff to the python path:
$> export PYTHONPATH=/Users/dwelling/python

Next, import the module:
>>>import sciprog

'''

# It is good practice to put most imports at the top of the file.
# Exceptions may be made for modules that are only used for one function.
import numpy as np

# If there are top level parameters or constants, declaring them next is
# a good idea from an organizational standpoint.

# Now, we'll declare functions:
def read_imf(infile, debug=False):
    '''
    This function reads an SWMF-formatted IMF/solar wind file and parses it into
    a special data structure.

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
    if type(infile) != type('str'):
        raise(TypeError('Input file name must be a string.'))

    # Open the file in read-only mode by creating a file object.
    f = open(infile, 'r')

    # Read the very first line.  Just like IDL, Python will remember our 
    # position in the file so that no lines are read twice.
    line=f.readline()
    
    # These files have a lot of header information.  We want to skip that.
    # We know, a priori, that the data begins after the "#START" text.  
    # Let's loop through the first lines until we hit that line.
    # When comparing two strings, we want to cut off leading and trailing
    # blanks.  We do that with the "strip" object method.
    while line.strip() != '#START':
        line=f.readline()

    # DEBUG:
    if debug: print('DEBUG: Our last header line was {}'.format(line))
        
    # At this point, we should be at the line where the data starts.
    # We can load the rest of the lines by using the "readlines()" (note the
    # s) to slurp all remaining lines.  Slurp is a term that means "read the
    # whole damn file."
    lines=f.readlines()

    # We're now done with this file, so close it.
    f.close()

    # AN IMPORTANT NOTE: THE "WITH" STATEMENT.
    # We could, alternatively, use this syntax to open/read the file:
    #with open(infile, 'r') as f:
    #    *do everything here up to f.close()*
    # "with" is a code block used to wrap actions that have distinct
    # "enter" and "exit" actions.  For example, when we open a file,
    # the enter action is to create a file object that is connected to
    # a file, open that file, and create the file pointer.  On exit,
    # we need to close that file as the "exit" action.  If there's an
    # error, it's possible that the code ends without ever performing the
    # exit action.  "with" blocks solve this existential problem.
    # For more information, see:
    # https://docs.python.org/3/reference/compound_stmts.html#with
    
    # How many lines do we have?  The "len()" function will tell us! 
    nLines = len(lines)

    # Now we can make a container for our data.  Our container will be a 
    # dictionary.  Each variable (time, bx, by, etc.) will be an key with
    # the corresponding value a vector of values.  One way to set it up is:
    data={}  #empty dictionary.
    keys=['bx','by','bz', 'vx','vy','vz', 'rho', 'temp']
    data['time']=np.zeros(nLines, dtype='object') # a vector of time objects!
    for k in keys:
        data[k]=np.zeros(nLines) # a vector of floats!

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
        parts=l.split()
        # Handle time first.  We need the first 7 values from the line (year 
        # through milisecond) and we need to turn them into ints and hand them
        # to the datetime module to make a datetime object.  We put the datetime
        # object into our time vector like so:
        # METHOD ONE: BRUTE FORCE.  When all else fails, do this:
        # for each part of the date and time, convert the string into an
        # integer, and use them to build the datetime object by hand.
        #data['time'][i]=dt.datetime(int(parts[0]), #year
        #                            int(parts[1]), #month
        #                            int(parts[2]), #day
        #                            int(parts[3]), #hour
        #                            int(parts[4]), #minute
        #                            int(parts[5]), #second
        #                            int(parts[6])/1000 #microsec
        #                            )
        # Looks contrived?  Wait until you see what is required in IDL.
        # METHOD TWO: Use the datetime.strptime method to build straight
        # from the string.  Note that we don't always know how much white
        # space there will be between entries, so let's rebuild the string
        # from our parts list:
        tNow = ' '.join(parts[:6])
        data['time'][i]=dt.datetime.strptime(tNow, '%Y %m %d %H %M %S')
        # These format codes are described here:
        # https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
        
        # We can now go through the rest of the parts and put them into
        # the right spots in our arrays.  Loop it!
        # The "brute force" way to do this would be to do use an index
        # to get the right value for the right variable name:
        #for j in range( len(keys) ):
        #    k = keys[j]    # Get our variable name as a dict key
        #    p = parts[7+j] # Get value; the 7 is to skip the time variables!
        #    data[k][i] = p # Put right value in right spot.
            
        # A much more "pythonic" way (elegant in the python style) is to
        # simultaneously iterate over both your keys and values at once:
        for k, p in zip(keys, parts[7:]):
            data[k][i]=p
        # With a little dictionary magic and loop fun, we did the entire 
        # variable group in two lines.  Play with the syntax to figure out
        # how this works (left as an excercise for the reader.)

    # That's it!  Our data dictionary is full.  Return it to the user.
    # You could plot a value by typing:
    #>>>import matplotlib.pyplot as plt
    #>>>plt.plot(data['time'], data['bz'])
    return(data)

# Make a function that customizes an axes:
def format_ax(ax, ylabel=None):
    '''
    Format an axes object, *ax*, to quickly add labels, change time ticks to
    sensible values, turn off xtick labels unless we're on the bottom
    row of plots, and set the y-axis label to kwarg *ylabel*
    
    Example usage: format_ax(axis, ylabel='some label string')
    '''

    import matplotlib.dates as mdt
    
    # Better tick spacing.  Let's put a major tick every 6 hours, a minor
    # tick every hour, and label the ticks by HH:MM UT.  Use locator
    # objects (special objects that find where to put ticks) to set tick
    # locations.  Use formatter objects to set the format of the tick
    # labels.  This looks pedantic, but is very, very powerful.
    Mtick=mdt.HourLocator(byhour=[0,6,12,18])
    mtick=mdt.HourLocator(byhour=range(24))
    fmt = mdt.DateFormatter('%H:%M UT')

    # Apply those to our axes.  Note that the axes objects contain
    # axis objects for the x axis and y axis.  We can edit single
    # axes so they look different!
    ax.xaxis.set_major_locator(Mtick)
    ax.xaxis.set_minor_locator(mtick)
    ax.xaxis.set_major_formatter(fmt)

    # Turn on the grid:
    ax.grid()
    
    # Set ylabel, if set:
    if ylabel: ax.set_ylabel(ylabel, size=16)

    # Kill some labels.  Get the list of label objects and turn some off.
    labels =ax.get_yticklabels()   # Get the labels...
    labels[-1].set_visible(False)  # Turn off the first.
    labels[0].set_visible(False)   # Turn off the 2nd.

    # Determine the axes' geometry.  Use this to determine if we're in the
    # bottom row of plots.  The geometry is returned as (nrows, ncols, iplot).
    geom = ax.get_geometry()
    # We're in the bottom row if the number of the current plot we're on is
    # greater than the number of plots in all rows above the last.
    is_bottom = geom[-1] > (geom[0]-1)*geom[1]
    
    # If we're in the bottom row, label the axes with the date and time.
    if is_bottom:
        # Get time limits, as floating point numbers,  from our axes object:
        tStart, tEnd = ax.get_xlim() # returns range of x-axes.
        # Convert tStart into a datetime:
        tStart = mdt.num2date(tStart)
        # Note how Datetime objects have methods to pretty-print the time!
        ax.set_xlabel( 'Time from {}'.format(tStart.isoformat()), size=18 )
    else:
        # No labels on any axis except the bottom plot.  Set the list of
        # labels to an empty list for no labels (but keep ticks!)
        ax.xaxis.set_ticklabels([])

def plot_imf(filename, outname=None):
    '''
    Read and plot imf file *filename* to screen.
    If kwarg *outname* is given, plot is saved to file using *outname* as the
    output file name.
    '''
    
    # Start by importing.
    import matplotlib.pyplot as plt  # our base plotting package.

    # Load the data as we did last time.
    data = read_imf(filename)
    
    # Create a figure object.  This will hold all of our axes objects.  
    # Think of this as the paper on which we write.
    # Use *figsize* to set the size in inches (metric is possible, too.)
    fig = plt.figure(figsize=(8.5,11))
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
    if(outname):
        fig.savefig(outname)
    else:
        plt.show()

# Let's re-do our IMF plotting tool using an object-oriented approach.  We
# still want the data structure to behave like a dictionary, so we'll
# inherit from *dict*, Python's dictionary class.
class ImfData(dict):
    '''
    A class for handling Imf data in SWMF ascii format.  To instantiate, 
    simply use,
    
    >>>imf = ImfData('some/file/here.txt')

    The data values are accessed using dictionary syntax:

    >>>imf['bx']
    >>>print(imf.keys())

    This class' parent is **dict**, so it behaves as a specialized
    dictionary.

    '''

    # Define the __init__ class, which sets how the object is made:
    def __init__(self, filename):
        # Call initialization method of parent class.  This causes the
        # object to be built just like a dictionary...
        super(ImfData, self).__init__(self)

        # ...but we'll customize how it is made:
        # Store file name.
        self.file = filename

        # Load the data into self:
        self._read_data()

        # Good to return "None".
        return None
        
    def __str__(self):
        '''
        Set the string representation of the object, i.e., what is displayed
        if you type print(self).
        '''
        return 'ImfData object of {}'.format(self.file)

    def __repr__(self):
        '''
        This sets how the object is displayed to screen when Python tries to
        show you information about the object.  Let's default to the __str__
        result.
        '''
        return self.__str__()

    def calc_b(self):
        '''
        Calculate the magnitude of the magnetic field.  Store as self['b'].
        '''
        # Import numpy's square root function.
        from numpy import sqrt
        # Calculate and store the total field magnitude.
        self['b'] = sqrt(self['bx']**2 + self['by']**2 +self['bz']**2)

    def calc_v(self):
        '''
        Calculate the magnitude of the velocity vector.  Store as self['v'].
        '''
        # Import numpy's square root function.
        from numpy import sqrt
        # Calculate and store the total field magnitude.
        self['v'] = sqrt(self['vx']**2 + self['vy']**2 +self['vz']**2)

    def calc_clock(self):
        '''
        Calculate IMF clock angle, arctan(By/Bz).
        Theta=0 is purely northward IMF, 180 is southward.
        '''
        self['clock'] = np.arctan2(self['by'],self['bz'])
        
    def calc_epsilon(self):
        '''
        Calculate the epsilon parameter representing the power input into 
        the magnetosphere.
        '''
        # Ensure prequisite variables are calculated:
        if 'b' not in self: self.calc_b()
        if 'v' not in self: self.calc_v()
        if 'clock' not in self: self.calc_clock()

        # Calculate epsilon:
        mu_o = 4*np.pi*1E-7

        # Calculate conversion factors:
        conv = 1000. * 1E-9**2 /mu_o # km/s->m/s; nT**2->T**2
        
        self['epsilon'] = conv*self['v']*self['b']**2*np.sin(self['clock']/2)**4

    def _read_data(self):
        '''
        Load data from self.file to self.  Works similar to stand-alone
        function, "read_imf".
        '''
        
        # This looks almost exactly like read_imf, so I'll skip the details.
        # Note, however, that our data container is now self and not a
        # dictionary that is returned!
        
        import numpy as np
        import datetime as dt
        
        # Check our arguments, raise exceptions if something is wrong.
        if type(self.file) != type('str'):
            raise(TypeError('Input file name must be a string.'))

        # Open the file in read-only mode by creating a file object.
        f = open(self.file, 'r')

        # Read the very first line. 
        line=f.readline()
    
        # Skip ahead to end of header.
        while line.strip() != '#START':
            line=f.readline()
        
        # Slurp remainder of file; close it.
        lines=f.readlines()
        f.close()
    
        # How many lines do we have?  The "len()" function will tell us! 
        nLines = len(lines)

        # Define variable names:
        keys=['bx','by','bz', 'vx','vy','vz', 'rho', 'temp']
        self['time']=np.zeros(nLines, dtype='object')
        for k in keys:
            self[k]=np.zeros(nLines) # a vector of floats!

        # Parse remainder of file:
        for i, l in enumerate(lines):
            # Split up the line into parts:
            parts=l.split()
            
            # Extract time:
            tNow = ' '.join(parts[:6])
            self['time'][i]=dt.datetime.strptime(tNow, '%Y %m %d %H %M %S')
            
            # Extract remaining data:
            for k, p in zip(keys, parts[7:]):
                self[k][i]=p


    def plot_imf(self, outname=None):
        '''
        Plot the IMF information in *self* to screen.
        If kwarg *outname* is given, plot is saved to file using *outname* as the
        output file name.
        '''

        # Again, this works very similarly to our previous plotting function.
        # However, we use **self** instead of opening the file from scratch.
        
        # Start by importing.
        import matplotlib.pyplot as plt  # our base plotting package.

        # Create a figure object, set spacing.
        fig = plt.figure(figsize=(8.5,11))
        fig.subplots_adjust(hspace=0.001, right=0.96, top=0.93, left=0.13, 
                            bottom=0.07)

        # Add subplots to the figure object. 
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(413)
        ax3 = plt.subplot(414)

        # Put the title on the top axis. 
        ax1.set_title(self.file)

        # TOP AXES: IMF
        ax1.plot(self['time'], self['by'], 'c--', label='$B_{Y}$')
        ax1.plot(self['time'], self['bz'], 'b', label='$B_{Z}$')
        
        # Create a legend:
        ax1.legend(loc='upper right', ncol=2)
        
        # Horizontal lines!  Must specify the y, xStart and xEnd.  lw is width.
        ax1.hlines(0, self['time'][0], self['time'][-1], colors='k', 
                   linestyles='dashed', lw=2.0)

        # Call our format function to cleanup and label our axes.
        format_ax(ax1, 'IMF ($nT$)')
        
        # MIDDLE AXES: NUMBER DENSITY
        ax2.plot(self['time'], self['rho'], 'r-')
        format_ax(ax2, r'$\rho$ ($cm^{-3}$)')
        
        # BOTTOM AXES: VELOCITY
        ax3.plot(self['time'], -1*self['vx'], 'g-')
        format_ax(ax3, r'$V_{X}$ ($\frac{km}{s}$)')
        
        # Finally, either save or show the plot.
        if(outname):
            fig.savefig(outname)
        else:
            plt.show()
        
if __name__ == '__main__':
    # This section runs when you execute this file as a script.
    # For resuable modules, this is a good place to test the
    # module contents.  For a more powerful, formal testing capability,
    # see Python's 'unittest' module:
    # http://docs.python-guide.org/en/latest/writing/tests/

    import matplotlib.pyplot as plt
    
    # Let's test our read/write functionality:
    print('Testing ImfData objects...')
    print('\tTesting ImfData.__init__:')
    imf = ImfData('./imf_test.dat')

    # Test some of the values to ensure they were read correctly.
    # Last line of the file is often a good choice.
    if imf['bz'][-1] != -1:
        # This line "raises" an error.  It causes Python to stop running
        # the code and tell the user something is wrong.  The type of error
        # is a "ValueError" here, and the message is the string 'IMF Bz...'
        raise(ValueError('IMF Bz is not read correctly.'))
    # Do this for other values:
    if imf['rho'][-1] !=  5.0:
        raise(ValueError('Number density is not read correctly.'))
    if imf['temp'][-1] !=  5E4:
        raise(ValueError('Temperature is not read correctly.'))

    # Test the calculations:
    print('\tTesting ImfData.calc_* functions:')
    # I could write another line for each function, like I did above, but
    # that would be dumb.  Let's be more pythonic.  Start by collecting all
    # of the methods that start with 'calc_' into a list:
    calcs = []
    for method in dir(imf):
        if 'calc_' in method: calcs.append( getattr(imf, method) )

    # Now,
    calcs = [imf.calc_b, imf.calc_v]
    for meth, value, result in zip(calcs, ['b', 'v'], [1, 500]):
        meth()
        if imf[value][-1] != result:
            raise(ValueError('Calculation of {} failed!'.format(value)))
