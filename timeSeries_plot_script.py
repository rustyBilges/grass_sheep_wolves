import matplotlib.pyplot as plt
import numpy as np
import os, sys

def plotTimeseries(timeseries):
    T = timeseries.shape[1]
    
    fig2 = plt.figure()
    ax1fig2 = fig2.add_subplot(111)
    ax1fig2.plot(range(T), timeseries[0,:]/4, 'g')
    ax1fig2.plot(range(T), timeseries[1,:], 'b')
    ax1fig2.plot(range(T), timeseries[2,:], 'r')
    #plt.show(fig2)
    plt.xlabel('time')
    plt.ylabel('species biomass')
    plt.savefig('timeseries.png', bbox_inches='tight')

def AR1(x):
    # auto-correlation at lag 1
    result = np.correlate(x, x, mode='full')
    return result[1+ result.size/2]

def CV(x):
    # coefficient of variation
    return np.std(x)/np.mean(x)
def plotCSD_indicators(cov, ar1):
    T = cov.shape[1]
    
    fig2 = plt.figure()
    ax1fig2 = fig2.add_subplot(121)
    ax1fig2.plot(range(T), cov[0,:], 'g')
    ax1fig2.plot(range(T), cov[1,:], 'b')
    ax1fig2.plot(range(T), cov[2,:], 'r')
    #plt.show(fig2)
    plt.xlabel('habitat loss')
    plt.ylabel('CV')
    
    ax2fig2 = fig2.add_subplot(122)
    ax2fig2.plot(range(T), ar1[0,:], 'g')
    ax2fig2.plot(range(T), ar1[1,:], 'b')
    ax2fig2.plot(range(T), ar1[2,:], 'r')
    #plt.show(fig2)
    plt.xlabel('habitat loss')
    plt.ylabel('AR1')
    plt.savefig('CSD_indicators_speciesLevel.png', bbox_inches='tight')

# do plotting for:
simID = 0

masterDirectory = 'simulation_%d' %simID
os.chdir(masterDirectory)

nRep =1
HL = np.arange(0,22000, 2000)

# to store stats results:
cov = np.zeros((3,len(HL)))
ar1 = np.zeros((3,len(HL)))

hl_index = 0
for hl in HL:
        
    directoryName = './%d_destroyedPatches' %hl
    os.chdir(directoryName)
        
        
    for r in range(nRep):
        fName = 'run%d_timeseries.csv' %r
        timeseries = np.genfromtxt(fName, delimiter=',')
        
        #print(timeseries)
        plotTimeseries(timeseries)
        
        for sp in range(3):
            cov[sp,hl_index] += CV(timeseries[sp,:])
            ar1[sp,hl_index] += AR1(timeseries[sp,:])
            
    for sp in range(3):
        cov[sp,hl_index] = cov[sp,hl_index]/nRep
        ar1[sp,hl_index] = ar1[sp,hl_index]/nRep
    os.chdir('..')

plotCSD_indicators(cov, ar1)  # at the species level