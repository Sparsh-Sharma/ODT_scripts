import time

import numpy as np

import matplotlib.pyplot as pl

start_time = time.time()


lScale = 1.   #< ref. len. [m]
tScale = 1.   #< ref. time [sec]
domainLength = 2.  #< [m] -- see yaml
xDomainCenter = 1.  #< [m] -- see yaml
eddySeq = np.loadtxt('./1.dat')
eddySizes = eddySeq[:,2-1] / lScale
eddyLeftEdges = (eddySeq[:,3-1] - (-0.5*domainLength + xDomainCenter)) / lScale   # channel: y in [0,2]
eddyRightEdges = (eddySeq[:,4-1] - (-0.5*domainLength + xDomainCenter)) / lScale   # channel: y in [0,2]
eddyTimes = eddySeq[:,10-1] / tScale
# idx = np.where(eddyTimes > -99)  #1: uses all eddies
idx = np.where((eddyTimes >= 0.) & (eddyTimes <= 1.0))  #2: truncate selection
neddy = len(eddyTimes[idx])


# for j in range(neddy):
#      pl.plot([eddyTimes[idx][j], eddyTimes[idx][j]], [eddyLeftEdges[idx][j], eddyRightEdges[idx][j]], 'k_-', lw=1.)
#      pl.xlabel('x')
#      pl.ylabel('r',labelpad=1.5)
#      pl.xlim(0,0.3)
#      # plt.ylim(0,60)
#      # pl.savefig('eddySeq.eps')
#      pl.savefig('eddySeq.pdf')
     
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


# start_time = time.time()
# main()
print("--- %s seconds ---" % (time.time() - start_time))   
     