#!/usr/bin/env python
'''
Freeman & Morley's Minimal Substorm Model.  Calculate the energy in the tail vs.
time using solar input from a SWMF-formatted ascii solar wind file.
See Freeman and Morley 2004, GRL.
'''

from argparse import ArgumentParser, RawDescriptionHelpFormatter

# Handle all arguments first before performing the rest
# of the script.  Start by creating the parser object and using the
# docstring as our help message. 
parser = ArgumentParser(description=__doc__)

# Now, for each argument/option, add it to the parser and add help info:
parser.add_argument('imffile', help='The name of the IMF input file to read.',
                    type=str)
parser.add_argument('-D', '--D', help='Value of the substorm time constant. '+
                    'Defaults to 2.69 hours.', type=float, default=2.69)

# Get args from caller, collect arguments into a convenient object:
args = parser.parse_args()

# Now begin the rest of our script.
import os
import numpy as np
import matplotlib.pyplot as plt
from clasp605 import ImfData

##### FUNCTION DECLARATIONS:
def smartTimeTicks(ax, time, do_label=False):
    '''
    Given an axes object, *ax* and some sequence of time, *time*, 
    set time ticks and labels to something more intelligent than 
    matplotlib defaults.  Those ticks are immediately applied to *ax*.
    If do_label is set to **True**, the x-axis is labeled.
    '''

    # This is a nice function that I stole from Spacepy.
    # It gives us more flexible time ticks.
    
    # Import tick tools:
    from matplotlib.dates import (MinuteLocator, HourLocator,
                                  DayLocator, DateFormatter)
    
    # Get time between first and last time entry, convert to hours.
    deltaT = time[-1] - time[0]
    nHours = deltaT.days * 24.0 + deltaT.seconds/3600.0

    # Based on number of hours, select frequency of ticks.
    if nHours < 12:
        Mtick = HourLocator(byhour = list(range(24)), interval = 2)
        mtick = MinuteLocator(byminute = [0,15,30,45])
        fmt = DateFormatter('%H:%M UT')
    elif nHours < 48:
        Mtick = HourLocator(byhour = [0,6,12,18])
        mtick = HourLocator(byhour = list(range(24)))
        fmt = DateFormatter('%H:%M UT')
    else:
        Mtick = DayLocator(bymonthday=list(range(5,35,5)))
        mtick = HourLocator(byhour=[0,6,12,18])
        fmt =  DateFormatter('%d %b')

    # Apply to our axes:
    ax.xaxis.set_major_locator(Mtick)
    ax.xaxis.set_minor_locator(mtick)
    ax.xaxis.set_major_formatter(fmt)

    # Add label if requested to do so:
    if do_label:
        ax.set_xlabel(time[0].strftime('%h %d, %Y  %H:%M'), size=16)

###### BEGIN MAIN PROGRAM:
        
# Set D constant in seconds:
D = args.D * 3600. # Hours -> seconds
        
# Open data file, calculate required values.
imf = ImfData(args.imffile)
imf.calc_epsilon()

# Create results containers:
n_pts = imf['time'].size
energy = np.zeros(n_pts)
epochs = []

ener_last = D*imf['epsilon'].mean()
energy[0] -= ener_last

# Integrate:
for i in range(1, n_pts):
    dt = (imf['time'][i]-imf['time'][i-1]).total_seconds()
    energy[i] = energy[i-1]+imf['epsilon'][i]*dt

    if energy[i] >= 0:
        ener_last = D*imf['epsilon'][i]
        energy[i] = - ener_last
        epochs.append(imf['time'][i])

# Create figure object and axes objects.
fig = plt.figure()
a1, a2 = fig.add_subplot(211), fig.add_subplot(212)

# Create line plots:
a1.plot(imf['time'], imf['epsilon'], 'r-', lw=2)
a2.plot(imf['time'], energy,          '-', lw=2)

# Create and label horizontal threshold line:
a2.text(imf['time'][0], 0.05, 'Substorm Energy Threshold')
a2.hlines(0.0, imf['time'][0], imf['time'][-1], linestyles='dashed', lw=2.0)

# Place epochs onto plot, preserving y-limits.
ymin, ymax = a2.get_ylim()        # get current axis limits.
ymax = .2                         # add some space above zero.
a2.vlines(epochs, ymin, ymax)     # add our vlines.  This changes limits...
a2.set_ylim( [ymin, ymax] )       # restore ylimits to good values.

# Y-axes labels:
a1.set_ylabel('Solar Wind Power' , size=14)
a2.set_ylabel('Tail Energy State', size=14)

# Y-axis ticks:
a1.set_yticklabels('')
a2.set_yticklabels('')

# Set time ticks:
smartTimeTicks(a1, imf['time'])
smartTimeTicks(a2, imf['time'], True)

fig.tight_layout()

plt.show()
