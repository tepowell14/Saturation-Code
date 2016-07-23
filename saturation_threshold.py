#!/usr/bin/python

import argparse
import os, sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

filename = '/reg/d/psdm/amo/amol3416/scratch/tpowell/intensities/r%04d_done.h5'

#Parse command line arguments
parser = argparse.ArgumentParser(prog='saturation_threshold.py', description='Check for Saturated Regions')
parser.add_argument('run', type=int, help='Run number')
args = parser.parse_args()

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
max_hybridPatterns = []

for i in max_intensities:
    dex = np.where(intensities==i)
    print dex
    max_hybridPatterns.append(Patterns[dex])

print max_hybridPatterns

#------------------------------------------------------
#Print information of interest (average/max intensity)
#------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
#Show and save 2-D image of maximum pixels values of patterns in a run (Input the y= lines to scan across)
#---------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------
#For the intense patterns plot the pixel values along two horizontal lines
#-------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#Determine saturation threshold for the 4 quadrants from the line scan patterns (Save Plots for visual inspection)
#-----------------------------------------------------------------------------------------------------------------
