#!/usr/bin/env python
'''
A quick and dirty script to visualize results from our example fortran 
program.  Opens the given file, reads data into a 2D array and time/space 
grid into 1D arrays, and creates a contour plot to illustrate the result.
'''

from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)
# Add arguments:
parser.add_argument('filename', help="Name of file to open and plot.",
                    type=str)
args = parser.parse_args()

# The usual imports:
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator, LogFormatterMathtext

# Open file.
f=open(args.filename, 'r')

# Parse header.
title=f.readline().strip() # Use header line as plot title.

# Use regular expressions to parse the rest of the header.
# Regexs made this step a lot easier!  
# The domain as a numpy array:
domain = np.array(re.findall('(\d+\.\d*)', f.readline()), dtype=float)  
# size of domain in space and time (as integers):
nx, nt = re.search('(\d+)x(\d+)', f.readline()).groups()  # number of points.
nx, nt = int(nx), int(nt)

# Create containers for x-grid, time-grid, and 2D results array:
results = np.zeros( (nx, nt) )
t = np.zeros(nt)

# Read spatial grid (just on the first line, skip sub-header).
# Convert into floating point integer numpy array.
x = np.array(f.readline().split()[1:], dtype=float)

# Read rest of file:
for i, l in enumerate(f.readlines()):
    parts = l.split()
    t[i] = parts[0]
    results[:,i] = parts[1:]

# Some ranges/values for the plot.  We use these to control the colorbar.
minlog = 1E-3
maxlog = 1.0
lev_exp = np.arange(np.log10(minlog), np.log10(maxlog), 0.1)
levs = np.power(10, lev_exp)

# Create a figure and a plot:
fig=plt.figure()
ax =fig.add_subplot(111)

# Sometimes, we get 0 or below 0 results, which doesn't work with
# log axes (or log-scale contours).  Tricky indexing!!
results[results<minlog] = minlog

# Create a filled contour.  Note how we use the levels and limits from
# above to carefully adjust and control our plot.  See the Matplotlib docs!
cont =ax.contourf(t, x, results, levs, 
                  norm=LogNorm(), cmap='hot')
# Create a colorbar for the plot, use math text ticks.
cbar=fig.colorbar(cont, ax=ax, ticks=LogLocator(), 
                  format=LogFormatterMathtext())
cbar.set_label('Intensity (arbitrary units)')

# Finally, label axes/plot.
ax.set_ylabel('X (arbitrary units)')
ax.set_xlabel('Time ($s$)')
ax.set_title(title)

# These lines are useful for updating the figure:
if plt.isinteractive():
    plt.draw()
else:
    plt.show()
