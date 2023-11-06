import time
import numpy as np
import matplotlib.pyplot as pl

start_time = time.time()

lScale = 1.   # ref. len. [m]
tScale = 1.   # ref. time [sec]
domainLength = 2.  # [m] -- see yaml
xDomainCenter = 1.  # [m] -- see yaml

# Prompt the user for the file location
file_location = input("Enter the file location for the eddy sequence data: ")

# Prompt the user for the value of n
n = int(input("Enter the value of n for plotting every nth Eddy Event: "))

# Load the eddy sequence data from the user-provided file location
try:
    eddySeq = np.loadtxt(file_location)
except FileNotFoundError:
    print("File not found. Please make sure the file exists and the path is correct.")
    exit()

eddySizes = eddySeq[:, 2-1] / lScale
eddyLeftEdges = (eddySeq[:, 3-1] - (-0.5 * domainLength + xDomainCenter)) / lScale
eddyRightEdges = (eddySeq[:, 4-1] - (-0.5 * domainLength + xDomainCenter)) / lScale
eddyTimes = eddySeq[:, 10-1] / tScale

pl.figure(1)
pl.figure(figsize=(10, 6))
pl.xticks(fontsize=20)
pl.yticks(fontsize=20)
pl.xlabel('x (m)', fontsize=20)
pl.ylabel('y (m)', labelpad=1.5, fontsize=20)
pl.xlim(0, 0.5)
pl.ylim(-0.05, 0.05)

for j in range(0, len(eddyTimes), n):
    # Draw horizontal bars connecting the left and right edges
    pl.hlines(eddyLeftEdges[j], eddyTimes[j] - 0.001, eddyTimes[j] + 0.001, colors='k', lw=0.5)
    pl.hlines(eddyRightEdges[j], eddyTimes[j] - 0.001, eddyTimes[j] + 0.001, colors='k', lw=0.5)

    # Plot vertical lines at the eddy times
    pl.plot([eddyTimes[j], eddyTimes[j]], [eddyLeftEdges[j], eddyRightEdges[j]], 'k_-', lw=0.5, ms=0.3)

# Uncomment this line to save the figure
# pl.savefig('eddySeq-.pdf')

print("--- %s seconds ---" % (time.time() - start_time))
