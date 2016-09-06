#!/usr/bin/python

import argparse
import os, sys
import h5py
import numpy as np
import pylab
import scipy.ndimage
import matplotlib.pyplot as plt

filename = '/reg/d/psdm/amo/amol3416/scratch/tpowell/intensities/r%04d_done.h5'
#filename = '/reg/d/psdm/amo/amol3416/scratch/tpowell/hits/r%04d_hits_done.h5'

#Parse command line arguments
parser = argparse.ArgumentParser(prog='saturation_threshold.py', description='Check for Saturated Regions')
parser.add_argument('run', type=int, help='Run number')
args = parser.parse_args()

with h5py.File(filename %args.run, 'r') as f:
    intensities = f['intensityMJUM2'][:]
    #intensities = f['hitscore'][:]
    Patterns = f['front'][:]

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

# keep track of max_intensities indices to find corresponding scattering patterns
top_scatteringPatterns = []

for i in max_intensities:
    dex = np.where(intensities==i)
    top_scatteringPatterns.append(Patterns[dex][0])

#print top_scatteringPatterns

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

#print "--------------------------"
#print "TOP 5 HITSCORES"
#print "--------------------------"
#print "min = %.2e, max = %.2e" % (maxintensities_arr.min(), maxintensities_arr.max())
#print "mean = %.2e, std = %.2e" % (maxintensities_arr.mean(), maxintensities_arr.std())
#print "median = %.2e" % (np.median(maxintensities_arr))

#---------------------------------------------------------------------------------------------------------
#2-D image of maximum pixels values of patterns in a run 
#---------------------------------------------------------------------------------------------------------
#Getting maximum pixels values of patterns in a run (from top most intense hits in a run)

top_scatteringPatterns_arr = np.array(top_scatteringPatterns)
    
patt1 = np.array(top_scatteringPatterns[0])
patt2 = np.array(top_scatteringPatterns[1])
patt3 = np.array(top_scatteringPatterns[2])
patt4 = np.array(top_scatteringPatterns[3])
patt5 = np.array(top_scatteringPatterns[4])

maxscattering_arr = np.maximum(patt1, patt2)
maxscattering_arr = np.maximum(maxscattering_arr, patt3)
maxscattering_arr = np.maximum(maxscattering_arr, patt4)
maxscattering_arr = np.maximum(maxscattering_arr, patt5)

max_scattering = maxscattering_arr.tolist()

#-------------------------------------------------------------------------
#For the intense patterns plot the pixel values along two horizontal lines (Input the y= lines to scan across)
#-------------------------------------------------------------------------
#Set up the data
z = max_scattering

plt.figure(1)
plt.imshow(z)
plt.title('Maximum Pixel Values')
plt.ylabel('y')
plt.xlabel('x')
plt.xlim(0,1000)
plt.ylim(0,1000)
plt.colorbar(label='[a.d.u.]')
plt.show()

line1 = int(raw_input('Enter first line scan: '))
line2 = int(raw_input('Enter second line scan: '))
#133
#138

def plotting(thr_lines):
    
    #LINE SCAN

    #Extract the lines in pixel coordinates with num points
    x0, y0 = 0, line1 
    x1, y1 = 1000, line1
    num = 1000
    x, y = np.linspace(x0, x1, num), np.linspace(y0, y1, num)

    n0, m0 = 0, line2 
    n1, m1 = 1000, line2
    n, m = np.linspace(n0, n1, num), np.linspace(m0, m1, num)

    # Extract the values along the lines, using cubic interpolation

    firstline = []
    secondline = []
    for i in range (0,5):
        firstline.append(scipy.ndimage.map_coordinates(top_scatteringPatterns[i], np.vstack((x,y))))
        secondline.append(scipy.ndimage.map_coordinates(top_scatteringPatterns[i], np.vstack((n,m))))

    plt.figure()
    plt.imshow(z)
    plt.plot([x0, x1], [y0, y1], 'w--')
    plt.plot([n0, n1], [m0, m1], 'w--')
    plt.title('Maximum Pixel Values')
    plt.ylabel('y')
    plt.xlabel('x')
    plt.xlim(0,1000)
    plt.ylim(0,1000)
    plt.colorbar(label='[a.d.u.]')

    #plotting line scans

    fig, axes = plt.subplots(nrows=2)
    
    for i in range (0,5):
        axes[0].plot(firstline[i])
        axes[1].plot(secondline[i])

    if thr_lines == True:
        #(x,y) line scan threshold
        p0, q0 = 0, sat_thr1 
        p1, q1 = 500, sat_thr1
        t1 = axes[0].plot([p0, p1], [q0, q1], 'k--')#, label = 'Saturation Threshold 135000 a.d.u.')
        #axes[0].legend()

        r0, s0 = 500, sat_thr2 
        r1, s1 = 1000, sat_thr2
        t2 = axes[0].plot([r0, r1], [s0, s1], 'k--')#, label = 'Saturation Threshold 135000 a.d.u.')
        #axes[0].legend()

        #(n,m) line scan threshold
        j0, k0 = 0, sat_thr3
        j1, k1 = 500, sat_thr3
        t3 = axes[1].plot([j0, j1], [k0, k1], 'k--')
        #axes[1].legend()

        l0, f0 = 500, sat_thr4
        l1, f1 = 1000, sat_thr4
        t4 = axes[1].plot([l0, l1], [f0, f1], 'k--')
        #axes[1].legend()
    
    axes[0].set_title('Pixel Values in Intense Patterns along y=%s' %line1)
    axes[0].set_ylabel('Raw Pixel Value [a.d.u.]')
    axes[0].set_xlabel('x(fast changing dim.)')
    
    
    axes[1].set_title('Pixel Values in Intense Patterns along y=%s' %line2)
    axes[1].set_ylabel('Raw Pixel Value [a.d.u.]')
    axes[1].set_xlabel('x(fast changing dim.)')

    fig.subplots_adjust(hspace=.5)
    plt.tight_layout()

    plt.savefig('/reg/d/psdm/amo/amol3416/scratch/tpowell/max_intensities/r%04d_thresholds.png' %args.run)
    
    plt.show()

plotting(False)

#Get this warning when I have several plots show instead of using subplots: /reg/neh/home/benedikt/local/lib/python2.7/site-packages/matplotlib-1.3.1-py2.7-linux-x86_64.egg/matplotlib/collections.py:548: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison  if self._edgecolors == 'face':

#-----------------------------------------------------------------------------------------------------------------
#Determine saturation threshold for the 4 quadrants from the line scan patterns (Save Plots for visual inspection)
#-----------------------------------------------------------------------------------------------------------------

sat_thr1 = int(raw_input('Enter first quadrant threshold: '))

sat_thr2 = int(raw_input('Enter second quadrant threshold: '))

sat_thr3 = int(raw_input('Enter third quadrant threshold: '))

sat_thr4 = int(raw_input('Enter fourth quadrant threshold: '))

quad_thresholds = [sat_thr1, sat_thr2, sat_thr3, sat_thr4]

#135000
#70000

plotting(True)

#---------------------------------------------------------------------------------------------------------
#Save top scattering patterns, max scattering pattern & max intensities
#---------------------------------------------------------------------------------------------------------

#Saving to file

f = h5py.File('/reg/d/psdm/amo/amol3416/scratch/tpowell/max_intensities/r%04d_top.h5' %args.run, 'w')
f.create_dataset('topscatteringPatterns', data = top_scatteringPatterns)

f.create_dataset('maxintensityMJUM2', data = max_intensities)
#f.create_dataset('maxhitscores', data = max_intensities)

f.create_dataset('maxscatteringPattern', data = max_scattering)
f.create_dataset('saturationThresholds', data = quad_thresholds)
f.close()
