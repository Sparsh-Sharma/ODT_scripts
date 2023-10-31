
import yaml
import sys
import os
import glob as gb
import numpy as np
import matplotlib.pyplot as pl

#--------------------------------------------------------------------------------------------

def extrap(x, xp, yp):
    """ np.interp function with linear extrapolation """
    y = np.interp(x, xp, yp)
    y[x<xp[ 0]] = yp[ 0] + (x[x<xp[ 0]]-xp[ 0])*(yp[ 0]-yp[ 1])/(xp[ 0]-xp[ 1])
    y[x>xp[-1]] = yp[-1] + (x[x>xp[-1]]-xp[-1])*(yp[-1]-yp[-2])/(xp[-1]-xp[-2])
    return y

#--------------------------------------------------------------------------------------------

if len(sys.argv) != 3:
    raise ValueError("Expected arguments are:  caseName1 shift1")

try:
    caseNames = sys.argv[1::2]
except:
    raise ValueError("Expected arguments are:  caseName1 shift1")

try:
    shifts = [ int(n) for n in sys.argv[2::2] ]
except:
    raise ValueError("Expected arguments are:  caseName1 shift1")

if len(caseNames) != len(shifts):
    raise ValueError("Number of cases and shifts is not equal.")

#if not os.path.exists("../../data/"+caseN+"/post"):
    #os.mkdir("../../data/"+caseN+"/post")

#if not os.path.exists("../../data/"+caseN+"/post/post_%05d" % (nshift,)):
    #os.mkdir("../../data/"+caseN+"/post/post_%05d" % (nshift,))

#--------------------------------------------------------------------------------------------

fig1, ax11 = pl.subplots(1, 1) #, sharex='col')

ax11.set_xlabel(r'$t$')
ax11.set_ylabel(r'$y$')
ax11.set_ylim([0., 1.])

#--------------------------------------------------------------------------------------------

caseName = caseNames[0] ; shift = shifts[0]

caseDataDir = caseName + '/data'
if os.path.isdir(caseDataDir + '/data_%05d' % (shift,)):
    caseDataDir = caseDataDir + '/data_%05d' % (shift,)
else:
    print("ERROR: directory '%s' does not exist" % (caseDataDir,))

# load FIXED params
with open(caseDataDir + "/../../input/odt_input.yaml") as ifile:
    y = yaml.safe_load(ifile)
cCoord = y["params"]["cCoord"]
#Aparam = y["params"]["A_param"]
#Cparam = y["params"]["C_param"]
#Zparam = y["params"]["Z_param"]
domainLength = y["params"]["domainLength"]
xDomainCenter = y["params"]["xDomainCenter"]
#kvisc = y["params"]["kvisc0"]

#UbcLo = y["bcCond"]["uBClo"]
#UbcHi = y["bcCond"]["uBChi"]

times = y["dumpTimes"]

#--------------------------------------------------------------------------------------------
# instantaneous
NlastDmp = 1980
dataFileList = sorted( gb.glob(caseDataDir + '/dmp_*.dat') )
dataFileList = dataFileList[-NlastDmp:]

times = np.array(times, dtype=float)
times = times[-NlastDmp:]

nfiles = len(dataFileList)
print("dump time files to load: %d" % (nfiles,))

nres = 101   # play with resolution
xp = np.linspace(0., 1., nres)

xx, yy = np.meshgrid(times, xp)

zz = np.zeros((nres, nfiles))

for j in range(len(dataFileList)):
    dataFile = dataFileList[j]
    time = float(times[j])
    print("%d  %10.3e  %s" % (j, time, dataFile,))

    data = np.loadtxt(dataFile)
    pos = (data[:,0] - (-0.5*domainLength + xDomainCenter)) / domainLength  # pos in [0, 1]
    dmp = data[:,2]    # select uvel

    zz[:,j] = extrap(xp, pos, dmp)

print("dump time files loaded: %d" % (nfiles,))

#ax11.contour(xx, yy, zz)
cp = ax11.pcolor(xx, yy, zz) #, vmin=.1, vmax=.9)
axcb = fig1.add_axes([0.87, 0.16, 0.016, 0.74])
fig1.colorbar(cp, cax=axcb, label=r'$u$') #, extend='both')

#------------------
# eddy sequence
eddySeq = np.loadtxt(caseDataDir + '/eddyAcceptedSizes.dat')
eddySizes = eddySeq[:,2-1] / domainLength
eddyLeftEdges = (eddySeq[:,3-1] - (-0.5*domainLength + xDomainCenter)) / domainLength  # pos in [0, 1]
eddyRightEdges = (eddySeq[:,4-1] - (-0.5*domainLength + xDomainCenter)) / domainLength  # pos in [0, 1]
eddyTimes = eddySeq[:,10-1]

idx = np.where((eddyTimes >= times.min()) & (eddyTimes <= times.max()))
neddy = len(eddyTimes[idx])  # n eddies
meddy = 1   # every m-th eddy

print('eddies to consider: %d %d' % (neddy, neddy/meddy,))
for j in range(neddy):
    if j % meddy == 0: 
        ax11.plot([eddyTimes[idx][j], eddyTimes[idx][j]], [eddyLeftEdges[idx][j], eddyRightEdges[idx][j]], 'k_-', lw=1.)

#--------------------------------------------------------------------------------------------

pl.show() ; exit()

fig1.savefig('2dEddySequence.png')

#--------------------------------------------------------------------------------------------


