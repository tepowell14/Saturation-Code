#!/usr/bin/python

import argparse
import os, sys
import h5py
import numpy as np
import pylab

import scipy.ndimage
import matplotlib.pyplot as plt

# import utils.cxiwriter
# import ipc.mpi

# this_dir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(this_dir)
# #
# from backend import add_record

filename = '/reg/d/psdm/amo/amol3416/scratch/tpowell/intensities/r%04d_done.h5'

#Parse command line arguments
parser = argparse.ArgumentParser(prog='saturation_threshold.py', description='Check for Saturated Regions')
parser.add_argument('run', type=int, help='Run number')
args = parser.parse_args()

# from hummingbird import parse_cmdline_args
# args = parse_cmdline_args()

with h5py.File(filename %args.run, 'r') as f:
    intensities = f['intensityMJUM2'][:]
    Patterns = f['hybridPattern'][:]

#---------------------------------------------------------------------------------
#Find and save 5 most intense hits (expected to be hits with highest # lit pixels)
#---------------------------------------------------------------------------------

#Most intense hits
max_intensities = []

for intensity in intensities:
    if len(max_intensities) != 5:
        max_intensities.append(intensity)
        max_intensities.sort(reverse=True)
    else:
        for i in max_intensities:
            if intensity > i:
                max_intensities.insert(max_intensities.index(i), intensity)
                max_intensities = max_intensities[:5]
                break

print max_intensities

# keep track of max_intensities indices to find corresponding hybrid patterns
top_hybridPatterns = []

for i in max_intensities:
    dex = np.where(intensities==i)
    top_hybridPatterns.append(Patterns[dex][0])

#print top_hybridPatterns

#------------------------------------------------------
#Print information of interest (average/max intensity)
#------------------------------------------------------
maxintensities_arr = np.array(max_intensities)
print "--------------------------"
print "TOP 5 INTENSITIES [mJ/um2]"
print "--------------------------"
print "min = %.2e, max = %.2e" % (maxintensities_arr.min(), maxintensities_arr.max())
print "mean = %.2e, std = %.2e" % (maxintensities_arr.mean(), maxintensities_arr.std())
print "median = %.2e" % (np.median(maxintensities_arr))


#---------------------------------------------------------------------------------------------------------
#2-D image of maximum pixels values of patterns in a run 
#---------------------------------------------------------------------------------------------------------
#Getting maximum pixels values of patterns in a run (from top most intense hits in a run)

top_hybridPatterns_arr = np.array(top_hybridPatterns)
    
patt1 = np.array(top_hybridPatterns[0])
patt2 = np.array(top_hybridPatterns[1])
patt3 = np.array(top_hybridPatterns[2])
patt4 = np.array(top_hybridPatterns[3])
patt5 = np.array(top_hybridPatterns[4])

maxhybrid_arr = np.maximum(patt1, patt2)
maxhybrid_arr = np.maximum(maxhybrid_arr, patt3)
maxhybrid_arr = np.maximum(maxhybrid_arr, patt4)
maxhybrid_arr = np.maximum(maxhybrid_arr, patt5)

max_hybrid = maxhybrid_arr.tolist()

#-------------------------------------------------------------------------
#For the intense patterns plot the pixel values along two horizontal lines (Input the y= lines to scan across)
#-------------------------------------------------------------------------

#line1 = raw_input('Enter first line scan: ')
#133
#139

#LINE SCAN

#Set up the data
z = max_hybrid

#Extract the lines in pixel coordinates with num points
x0, y0 = 0, 133 
x1, y1 = 250, 133
num = 1000
x, y = np.linspace(x0, x1, num), np.linspace(y0, y1, num)

n0, m0 = 0, 138 
n1, m1 = 250, 138
n, m = np.linspace(n0, n1, num), np.linspace(m0, m1, num)

# Extract the values along the lines, using cubic interpolation

#bilinear/cubic interpolation (smooth graph)

#First line (x,y)
#firstline = []

zxy1 = scipy.ndimage.map_coordinates(top_hybridPatterns[0], np.vstack((x,y)))
zxy2 = scipy.ndimage.map_coordinates(top_hybridPatterns[1], np.vstack((x,y)))
zxy3 = scipy.ndimage.map_coordinates(top_hybridPatterns[2], np.vstack((x,y)))
zxy4 = scipy.ndimage.map_coordinates(top_hybridPatterns[3], np.vstack((x,y)))
zxy5 = scipy.ndimage.map_coordinates(top_hybridPatterns[4], np.vstack((x,y)))

#for i in range(5):
    #firstline.append(firstline,scipy.ndimage.map_coordinates(top_hybridPatterns[i], np.vstack((x,y)))

#firstline=firstline.reshape((5,256,256))

#Second line (n,m)
znm1 = scipy.ndimage.map_coordinates(top_hybridPatterns[0], np.vstack((n,m)))
znm2 = scipy.ndimage.map_coordinates(top_hybridPatterns[1], np.vstack((n,m)))
znm3 = scipy.ndimage.map_coordinates(top_hybridPatterns[2], np.vstack((n,m)))
znm4 = scipy.ndimage.map_coordinates(top_hybridPatterns[3], np.vstack((n,m)))
znm5 = scipy.ndimage.map_coordinates(top_hybridPatterns[4], np.vstack((n,m)))


#Shows single window with all plots
plt.figure(1)
plt.imshow(z)
plt.plot([x0, x1], [y0, y1], 'w--')
plt.plot([n0, n1], [m0, m1], 'w--')
plt.title('Maximum Pixel Values')
plt.ylabel('y')
plt.xlabel('x')
plt.xlim(0,250)
plt.ylim(0,250)
plt.colorbar(label='[a.d.u.]')

fig, axes = plt.subplots(nrows=2)

#plot (x,y) line scan

#for i in firstline:
    #axes[0].plot(i)

axes[0].plot(zxy1)
axes[0].plot(zxy2)
axes[0].plot(zxy3)
axes[0].plot(zxy4)
axes[0].plot(zxy5)

#(x,y) line scan threshold
p0, q0 = 0, 135000 
p1, q1 = 1000, 135000
t1 = axes[0].plot([p0, p1], [q0, q1], 'k--', label = 'Saturation Threshold 135000 a.d.u.')
axes[0].legend()

axes[0].set_title('Pixel Values in Intense Patterns along y=133')
axes[0].set_ylabel('Raw Pixel Value [a.d.u.]')
axes[0].set_xlabel('x(fast changing dim.)')


#plot (n,m) line scan
axes[1].plot(znm1)
axes[1].plot(znm2)
axes[1].plot(znm3)
axes[1].plot(znm4)
axes[1].plot(znm5)

#(n,m) line scan threshold
j0, k0 = 0, 70000 
j1, k1 = 1000, 70000
t2 = axes[1].plot([j0, j1], [k0, k1], 'k--', label = 'Saturation Threshold 70000 a.d.u.')
axes[1].legend()

axes[1].set_title('Pixel Values in Intense Patterns along y=138')
axes[1].set_ylabel('Raw Pixel Value [a.d.u.]')
axes[1].set_xlabel('x(fast changing dim.)')

plt.show()

#Get this warning when I have several plots show instead of using subplots: /reg/neh/home/benedikt/local/lib/python2.7/site-packages/matplotlib-1.3.1-py2.7-linux-x86_64.egg/matplotlib/collections.py:548: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison  if self._edgecolors == 'face':

#-----------------------------------------------------------------------------------------------------------------
#Determine saturation threshold for the 4 quadrants from the line scan patterns (Save Plots for visual inspection)
#-----------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
#Save top hybrid patterns, max hybrid pattern & max intensities
#---------------------------------------------------------------------------------------------------------

#Saving to file

f = h5py.File('/reg/d/psdm/amo/amol3416/scratch/tpowell/max_intensities/r%04d_top.h5' %args.run, 'w')
f.create_dataset('tophybridPatterns', data = top_hybridPatterns)
f.create_dataset('maxintensityMJUM2', data = max_intensities)
f.create_dataset('maxhybridPattern', data = max_hybrid)
f.close()
