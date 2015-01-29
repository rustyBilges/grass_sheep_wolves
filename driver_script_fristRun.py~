from landscape import *

import os, sys
import numpy as np

if __name__== '__main__':
    
    simulationID = 0000  # this is the unique ID that relates to oneNote doucment
    
    masterDirectory = './simulation_%d' %simulationID
    os.mkdir(masterDirectory)
    os.chdir(masterDirectory)
    
    nRep = 1
    HL = np.arange(0,22000, 2000)
    
    saveSpeciesDistributions = True
    updateDistributionsEvery = 100   # iterations

    T = 10     # number of timesteps per run
    rest = 0.0 # rest between frames (only relevant to animation)

    
    for hl in HL:
        
        directoryName = './%d_destroyedPatches' %hl
        os.mkdir(directoryName)
        os.chdir(directoryName)
        
        # run nRep simulations.. 
        for r in range(nRep):
            # save species ditributions in here:
            subDirectoryName = './run%d' %r
            os.mkdir(subDirectoryName)
            os.chdir(subDirectoryName)
            
            
            L = Landscape(True, False, T, rest, True, 5, r, hl)          # false for now animation
            print('This is run%d at HL = %d') % (r, hl)
            print(L)
            L.saveParameters()
            
            for t in range(T):
                L.update(t)
            # then change up at EoS to save timesereis in parent directory
            os.chdir('..')
            np.savetxt('run%d_timeseries.csv' %r, L.timeSeries, delimiter=",")
            os.chdir('..')