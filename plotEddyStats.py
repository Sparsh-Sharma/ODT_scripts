import sys
import os
import numpy as np
import matplotlib.pyplot as pl

#---------------------------------

if len(sys.argv) < 3: 
    raise ValueError('CASENAME and SHIFT argument expected. NBINS and NSTART is optional')

case = sys.argv[1]
shift = int(sys.argv[2])

nBins = 5000    # not too coarse, not too fine
if len(sys.argv) > 3:
    nBins = int(sys.argv[3])

nStart = 0      # first line to read
if len(sys.argv) > 4:
    nStart = int(sys.argv[4])

#---------------------------------

domainLength = 1.           # check input file
boundaryLeft = -0.5         # check input file
boundaryRight = boundaryLeft + domainLength

#---------------------------------

#caseDataDir = '../../data/' + case + '/data'
caseDataDir = case + '/data'
if os.path.isdir(caseDataDir + '/data_%05d' % (shift,)):
    caseDataDir = caseDataDir + '/data_%05d' % (shift,)

data = np.loadtxt(caseDataDir + '/eddyAcceptedSizes.dat')
eddySizes = data[nStart:,1] / domainLength  # fraction of domain
eddyLeft = data[nStart:,2] / domainLength   # fraction of domain
eddyRight = data[nStart:,3] / domainLength  # fraction of domain

boundaryLeft /= domainLength    # fraction of domain
boundaryRight /= domainLength   # fraction of domain

#---------------------------------

bins, binWidth = np.linspace(0., domainLength, nBins+1, retstep=True)

counts, binEdges = np.histogram(eddySizes, bins=bins)
lengths = (binEdges[:-1] + binEdges[1:])*0.5
widths = (binEdges[1:] - binEdges[:-1])

imax = np.argmax(counts)
lpMax = lengths[imax]

weights = counts * widths
lpInt = np.sum(lengths * weights) / np.sum(weights)

lmin = 1.e+30
for i in range(counts.size):
    if counts[i] > 0:
        lmin = lengths[i]
        break
        
lmax = -1.e+30
for i in range(counts.size):
    j = counts.size-1-i
    if counts[j] > 0:
        lmax = lengths[j]
        break

#---------------------------------

print( '%10.6g %8d %10d %10.6g %10.6g %10.6g %10.6g %s %d' 
      % (lpMax, counts[imax], counts.sum(), lpInt, lmin, lmax, binWidth, case, shift,) )

#---------------------------------

#---- eddy sizes (pdf) of all accepted eddies
pl.figure(1)

pl.plot(lengths, counts, 'k+')
pl.plot(lpMax, counts[imax], 'ro')
pl.axvline(lpInt, color='r', ls='-')

pl.grid('on')
#pl.show()

#---- eddy sizes (cdf) of all accepted eddies
cumCounts = np.zeros_like(counts)
cumCounts[0] = counts[0]
for i in range(1, cumCounts.size, 1):
    cumCounts[i] = cumCounts[i-1] + counts[i]
cdf = cumCounts / float(counts.sum())

pl.figure(2)

pl.plot(lengths, cdf, 'k+')
pl.axvline(lpMax, color='r', ls='--')
pl.axvline(lpInt, color='r', ls='-')

pl.grid('on')
#pl.show()


#---- interior vs. near-wall eddies (applicable to channel and similar internal flow)
eddySizesBulk = eddySizes[ np.nonzero((eddySizes < eddyLeft - boundaryLeft) & (eddySizes < boundaryRight - eddyRight)) ]
eddySizesWall = eddySizes[ np.nonzero((eddySizes >= eddyLeft - boundaryLeft) | (eddySizes >= boundaryRight - eddyRight)) ]

countsBulk, binEdges = np.histogram(eddySizesBulk, bins=bins)
countsWall, binEdges = np.histogram(eddySizesWall, bins=bins)

pl.figure(3)

pl.plot(lengths, counts, 'k+')
pl.plot(lengths, countsBulk, 'b.')
pl.plot(lengths, countsWall, 'r.')

pl.plot(lpMax, counts[imax], 'ro')
pl.axvline(lpInt, color='r', ls='-')

pl.grid('on')
#pl.show()

pl.show()

