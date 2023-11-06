import time

import numpy as np

import matplotlib.pyplot as pl

start_time = time.time()


lScale = 1.   #< ref. len. [m]
tScale = 1.   #< ref. time [sec]
domainLength = 2.  #< [m] -- see yaml
xDomainCenter = 1.  #< [m] -- see yaml


# Prompt the user for the file location
file_location = input("Enter the file location for the eddy sequence data: ")

# Load the eddy sequence data from the user-provided file location
try:
    eddySeq = np.loadtxt(file_location)
except FileNotFoundError:
    print("File not found. Please make sure the file exists and the path is correct.")
    exit()


eddySizes = eddySeq[:,2-1] / lScale
eddyLeftEdges = (eddySeq[:,3-1] - (-0.5*domainLength + xDomainCenter)) / lScale   # channel: y in [0,2]
eddyRightEdges = (eddySeq[:,4-1] - (-0.5*domainLength + xDomainCenter)) / lScale   # channel: y in [0,2]
eddyTimes = eddySeq[:,10-1] / tScale
# idx = np.where(eddyTimes > -99)  #1: uses all eddies
idx = np.where((eddyTimes >= 0.) & (eddyTimes <= 1.0))  #2: truncate selection
neddy = len(eddyTimes[idx])
     
pl.figure(1)   
pl.figure(figsize=(10,6))
# pl.figure(aspect=1)
pl.xticks(fontsize=20)
pl.yticks(fontsize=20)
pl.xlabel('x (m)',fontsize=20)
pl.ylabel('y (m)',labelpad=1.5, fontsize=20)
pl.xlim(0,.5)
pl.ylim(-0.05,0.05)
for j in range(neddy):
     pl.plot([eddyTimes[idx][j], eddyTimes[idx][j]], [eddyLeftEdges[idx][j], eddyRightEdges[idx][j]], 'k_-', lw=0.5, ms=0.3)
pl.savefig('eddySeq-.pdf')  

print("--- %s seconds ---" % (time.time() - start_time))   
     
