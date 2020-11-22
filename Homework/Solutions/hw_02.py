#!/usr/bin/env python

'''
Let's quickly crank out some values for Homework 2.
'''
import sys
import datetime as dt

import numpy as np

# Add directories to path so we can use lecture modules here:
path = '../../Python/'
if path not in sys.path: sys.path.append(path)

# Now import sciprog:
from sciprog import ImfData

def read_dst(filename):
    '''
    Adapted from Spacepy's `spacepy.pybats.Kyoto` module, this 
    reads KyotoWDC's rather sticky file format.
    '''

    with open(filename, 'r') as f:
        lines = f.readlines()
        
    npts=len(lines)
    time = []
    dst  = np.zeros(24*npts)
    for i,line in enumerate(lines):
        # Get year, month, day.
        try:
            yy = int(line[14:16]) * 100
        except:
            yy = 1900
        yy = yy + int(line[3:5])
        dd = int(line[8:10])
        mm = int(line[5:7 ])
        
        # Parse the rest of the data.
        for j in range(0,24):
            time.append(dt.datetime(yy, mm, dd, j))
            loc = 20 + 4*j
            dst[24*i + j] = float(line[loc:loc+4])

    time  = np.array(time)
    dst   = np.array(dst)

    return time, dst

if __name__ == "__main__":
    # IMF WORK:
    imf = ImfData('../../Data/imf_jul2000.dat')
    imf.calc_b()
    imf.calc_v()

    print("IMF STATS:")
    print(f"\tMean |B| = {imf['b'].mean()}")
    print(f"\tMean |V| = {imf['v'].mean()}")
    
    
    with open('b_data.txt', 'w') as out:
        out.write('Bx\tBy\tBz\t|B|\n')
        for i in range(imf['bx'].size):
            out.write(f"{imf['bx'][i]:+.3f}\t{imf['by'][i]:+.3f}\t"+
                      f"{imf['bz'][i]:+.3f}\t{imf['b' ][i]:+.3f}\n")
        
    with open('v_data.txt','w') as out:
        out.write('Vx\tVy\tVz\t|V|\n')
        for i in range(imf['vx'].size):
            out.write(f"{imf['vx'][i]:+.1f}\t{imf['vy'][i]:+.2f}\t"+
                      f"{imf['vz'][i]:+.2f}\t{imf['v' ][i]:+.1f}\n")
    
    
    # DST WORK:
    time, dst = read_dst('../../Data/Dst_July2000.dat')

    print(f"DST STATS:")
    print(f"\tMax/Min DST= {dst.max()}, {dst.min()}")
    print(f"\tMean DST   = {dst.mean():.3f}")
    print(f"\tMedian DST = {np.median(dst):.3f}")
    print(f"\tStdDev DST = {np.std(dst):+.3f}")
