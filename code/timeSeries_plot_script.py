import matplotlib.pyplot as plt
import numpy as np
import os, sys

def plotTimeseries(timeseries, run):
    T = timeseries.shape[1]
    
    fig2 = plt.figure()
    ax1fig2 = fig2.add_subplot(111)
    ax1fig2.plot(range(T), timeseries[0,:]/4, 'g')
    ax1fig2.plot(range(T), timeseries[1,:], 'b')
    ax1fig2.plot(range(T), timeseries[2,:], 'r')
    #plt.show(fig2)
    plt.xlabel('time')
    plt.ylabel('species biomass')
    plt.savefig('run%d_timeseries.png' %run, bbox_inches='tight')

def plotAllTimeseries(Tseries):
    T = Tseries[0].shape[1]
    
    fig2 = plt.figure()
    for i in range(len(Tseries)):
        
        plt.subplot(4,3,i+1)
        plt.plot(range(T), Tseries[i][0,:]/4, 'g')
        plt.plot(range(T), Tseries[i][1,:], 'b')
        plt.plot(range(T), Tseries[i][2,:], 'r')
        
    #plt.show(fig2)
    #plt.xlabel('time')
    #plt.ylabel('species biomass')
    fig2.tight_layout()
    plt.savefig('allTimeseries_run0.png')

def plotTotalBiomass(Tseries):
    T = Tseries[0].shape[1]
    
    fig2 = plt.figure()
    for i in range(len(Tseries)):
        
        plt.subplot(4,3,i+1)
        plt.plot(range(T), Tseries[i][0,:]+Tseries[i][1,:]+Tseries[i][2,:], 'k')
        
    #plt.show(fig2)
    #plt.xlabel('time')
    #plt.ylabel('species biomass')
    fig2.tight_layout()
    plt.savefig('totalBiomass_run0.png')

def AR1(X, split=2):
    x = X[X.size/2:]
    # auto-correlation at lag 1
    result = np.correlate(x, x, mode='full')
    return result[1+ result.size/2]

def CV(X, split=2):
    # coefficient of variation
    x = X[X.size/2:]
    return np.std(x)/np.mean(x)

def plotCSD_indicators(cov, ar1, covTot, ar1Tot, meanBiomass, finalBiomass):
    T = cov.shape[1]
    
    fig2 = plt.figure()
    ax1fig2 = fig2.add_subplot(321)
    ax1fig2.plot(range(T), cov[0,:], 'g')
    ax1fig2.plot(range(T), cov[1,:], 'b')
    ax1fig2.plot(range(T), cov[2,:], 'r')
    plt.ylim([0,0.5])
    #plt.show(fig2)
    plt.xlabel('habitat loss')
    plt.ylabel('CV')
    
    ax2fig2 = fig2.add_subplot(322)
    #ax2fig2.plot(range(T), ar1[0,:], 'g')
    ax2fig2.plot(range(T), ar1[1,:], 'b')
    ax2fig2.plot(range(T), ar1[2,:], 'r')
    #plt.show(fig2)
    plt.xlabel('habitat loss')
    plt.ylabel('AR1')

    ax3fig2 = fig2.add_subplot(323)
    ax3fig2.plot(range(T), covTot[0,:], 'k')
    #plt.show(fig2)
    plt.xlabel('habitat loss')
    plt.ylabel('CV_tot')
    
    ax4fig2 = fig2.add_subplot(324)
    ax4fig2.plot(range(T), ar1Tot[0,:], 'k')
    #plt.show(fig2)
    plt.xlabel('habitat loss')
    plt.ylabel('AR1_tot') 
    
    ax5fig2 = fig2.add_subplot(325)
    ax5fig2.plot(range(T), meanBiomass[0,:]/4, 'g')
    ax5fig2.plot(range(T), meanBiomass[1,:], 'b')
    ax5fig2.plot(range(T), meanBiomass[2,:], 'r')
    #plt.show(fig2)
    plt.xlabel('habitat loss')
    plt.ylabel('mean biomass')
    
    ax5fig2 = fig2.add_subplot(326)
    ax5fig2.plot(range(T), finalBiomass[0,:]/4, 'g')
    ax5fig2.plot(range(T), finalBiomass[1,:], 'b')
    ax5fig2.plot(range(T), finalBiomass[2,:], 'r')
    #plt.show(fig2)
    plt.xlabel('habitat loss')
    plt.ylabel('final biomass')
   
    
    plt.tight_layout()
    plt.savefig('CSD_indicators_speciesLevel.png', bbox_inches='tight')


#############################################################

# do plotting for:
simID = 0

masterDirectory = 'simulation_%d' %simID
os.chdir(masterDirectory)

nRep =1
HL = np.arange(0,22000, 2000)

# to store stats results:
cov = np.zeros((3,len(HL)))
ar1 = np.zeros((3,len(HL)))
# results for total Biomass:
covTot = np.zeros((1,len(HL)))
ar1Tot = np.zeros((1,len(HL)))

hl_index = 0

# to plot all timeseries for run0:
Tseries = []

# to plot the average species Biomass versus HL
meanBiomass = np.zeros((3, len(HL)))
finalBiomass = np.zeros((3, len(HL)))

for hl in HL:
        
    directoryName = './%d_destroyedPatches' %hl
    os.chdir(directoryName)
        
        
    for r in range(nRep):
        fName = 'run%d_timeseries.csv' %r
        timeseries = np.genfromtxt(fName, delimiter=',')
        
        if r==0:
            Tseries.append(timeseries)
        #print(timeseries)
        plotTimeseries(timeseries, r)
        
        for sp in range(3):
            cov[sp,hl_index] += CV(timeseries[sp,:])
            ar1[sp,hl_index] += AR1(timeseries[sp,:])
            
            meanBiomass[sp,hl_index] += np.mean(timeseries[sp,:])
            finalBiomass[sp, hl_index] += timeseries[sp,-1]
        
        covTot[0,hl_index] += CV(timeseries[0,:]+timeseries[1,:]+timeseries[2,:])
        ar1Tot[0,hl_index] += AR1(timeseries[0,:]+timeseries[1,:]+timeseries[2,:])
        
                
    for sp in range(3):
        cov[sp,hl_index] = cov[sp,hl_index]/nRep
        ar1[sp,hl_index] = ar1[sp,hl_index]/nRep
        
        meanBiomass[sp,hl_index] = meanBiomass[sp,hl_index]/nRep
        finalBiomass[sp,hl_index] = finalBiomass[sp,hl_index]/nRep
        

    
    covTot[0,hl_index] = covTot[0,hl_index]/nRep
    ar1Tot[0,hl_index] = ar1Tot[0,hl_index]/nRep
        
    hl_index += 1
    os.chdir('..')
plotAllTimeseries(Tseries)
plotTotalBiomass(Tseries)
plotCSD_indicators(cov, ar1, covTot, ar1Tot, meanBiomass, finalBiomass)  # at the species level