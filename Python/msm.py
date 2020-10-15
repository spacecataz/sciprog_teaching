#!/usr/bin/env python
'''
Freeman & Morley's Minimal Substorm Model.  Calculate the energy in the tail vs.
time using solar input from a SWMF-formatted ascii solar wind file.
See Freeman and Morley 2004, GRL.
'''

# The argparse module handles input arguments from the unix shell
# command line interface.  We'll cover this more during our
# scripting section.
from argparse import ArgumentParser

# Handle all arguments first before performing the rest
# of the script.  Start by creating the parser object and using the
# docstring as our help message. 
parser = ArgumentParser(description=__doc__)

# Now, for each argument/option, add it to the parser and add help info.
# Documentation of argparse is found here: https://docs.python.org/3/library/argparse.html
# ...and a good tutorial is found here: https://docs.python.org/3/howto/argparse.html
# Note how we use argparse to set defaults!
parser.add_argument('imffile', help='The name of the IMF input file to read.',
                    type=str)
parser.add_argument('-D', '--D', help='Value of the substorm time constant. '+
                    'Defaults to 2.69 hours.', type=float, default=2.69)

# Get args from caller, collect arguments into a convenient object:
args = parser.parse_args()

# Now begin the rest of our script.
# Start with our imports, starting with the standard Python library, then
# user-installed libraries, then user-generated libraries.
import os
import numpy as np
import matplotlib.pyplot as plt
from sciprog import ImfData, smartTimeTicks

# Set our plotting style:
plt.style.use('seaborn-darkgrid')
        
# Set D constant in seconds.   Note how we obtain
# the value from "args", set by argparse.
D = args.D * 3600. # Hours -> seconds
        
# Open data file, calculate required values.  Use
# our object oriented approach.
imf = ImfData(args.imffile)
imf.calc_epsilon()  # This also calculates |V| and |B|.

# Create results containers: energy will have the
# same number of entries as our solar wind file.
# We don't know how many substorms we'll generate a priori,
# so we'll create an empty list to which we can append values.
n_pts = imf['time'].size
energy = np.zeros(n_pts)
epochs = []

# Set our initial energy condition.  Do this by assuming a substorm
# just happened, so our energy state is D*P below the energy
# threshold value (assumed to be zero, see the powerpoint file).
# Use the average epsilon value to initialize:
energy[0] = -D*imf['epsilon'].mean()

# Integrate!
# Loop over all subsequent time values.  "i" represents the
# position of t_now + delta T; i-1 is t_now.  Each iteration
# advances from t_now to t_now + delta T.
for i in range(1, n_pts):
    # Get time step from imf file.  Subtract two times, which
    # gives us a "timedelta" object.  By calling the "total_seconds"
    # method, we convert it into a floating point value.
    dt = (imf['time'][i]-imf['time'][i-1]).total_seconds()

    # This is our actual integration step (Euler's Method):
    energy[i] = energy[i-1]+imf['epsilon'][i]*dt

    # See if we crossed our threshold:
    if energy[i] >= 0:
        # If so, "release energy" as required by MSM:
        energy[i] = - D*imf['epsilon'][i]
        # Save epoch to list:
        epochs.append(imf['time'][i])

# Save epochs to file.  Note that we're using the "with" statement.
# See sciprog.py for details on this.
# Note how we end each line with a newline character (\n).
with open('substorm_epochs.txt', 'w') as f:
    f.write('Substorm onsets created from the Minimal Substorm Model (MSM)\n')
    f.write(f'Input file used: {args.imffile}\n')
    for e in epochs: f.write(f'{e:%Y-%m-%d %H:%M:%S} UT \n')
        
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
ymin, ymax = a2.get_ylim()                    # get current axis limits.
ymax = .2                                     # add some space above zero.
a2.vlines(epochs, ymin, ymax, colors='k')     # add our vlines.  This changes limits...
a2.set_ylim( [ymin, ymax] )                   # restore ylimits to good values.

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
