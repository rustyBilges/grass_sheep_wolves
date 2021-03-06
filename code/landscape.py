# Notes..
# Think about optimisation..esp no need to update habitat distirbution if this is static!
# Also could reduce redundancy in neighbourhood search?
# Also think about whta to do in case when individual is trapped
# Also, if habitat is destroyed this does not change so could reduce search time/decisions?

from species import * 
import random as rnd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)

import time

from configure import ROWS, COLUMNS, INIT_NUMBER_SHEEP, INIT_NUMBER_WOLVES, INIT_NUMBER_GRASS#, NUMBER_DESTROYED_PATCHES

class Landscape():
	
    def __init__(self, timeSeries=False, animate=False, T=0, rest=0, saveSpeciesDists = False, saveEvery=None, runID = 0, numberDestroyedPatches = 0):
        
        self.sheepIDTracker = 0
        self.wolfIDTracker = 0   # such that every individual born can be given a unique ID
        self.sheepCount = 0
        self.wolfCount = 0
        self.grassCount = 0
        self.sheep = {}
        self.wolves = {}
        
        self.numberDestroyedPatches = numberDestroyedPatches
        self.destroyedPatches = 0
        self.patches = []
        self._create_patches()
        self._initialise_patches()
        self.patches[0][0].grass.state = False  #JUST FOR TEMPORARY
        
        self.T = T
        
        if timeSeries==True:
            self.timeSeries = np.zeros((3, T+1))
        else:         
            self.timeSeries=None
            
        self.animate = animate
        if animate==True:            
            self.rest = rest
            self.habitatDist = np.zeros((ROWS,COLUMNS))
            self.grassDist = np.zeros((ROWS,COLUMNS))
            self.sheepDist = np.zeros((ROWS,COLUMNS))
            self.wolfDist = np.zeros((ROWS,COLUMNS))    
    
            self.fig, (self.ax1, self.ax2, self.ax3, self.ax4) = plt.subplots(1,4)
            self.species_distributions(self.habitatDist, self.grassDist, self.sheepDist, self.wolfDist)

            for i in range(ROWS):
              for j in range(COLUMNS):
                if self.patches[i][j].habitat:
                    self.habitatDist[i][j]=1

    
            self.p1 = self.ax1.imshow(self.habitatDist, cmap='Oranges', interpolation=None)    
            self.p2 = self.ax2.imshow(self.grassDist, cmap='Greens', interpolation=None)    
            self.p3 = self.ax3.imshow(self.sheepDist, cmap='Blues', interpolation=None)    
            self.p4 = self.ax4.imshow(self.wolfDist, cmap='Reds', interpolation=None)    
            plt.draw()
            time.sleep(1)
            
        self.saveSpeciesDists = saveSpeciesDists
        if saveSpeciesDists==True:
            
            self.saveEvery = saveEvery
            self.runID = runID
            
            self.habitatDist = np.zeros((ROWS,COLUMNS))
            self.grassDist = np.zeros((ROWS,COLUMNS))
            self.sheepDist = np.zeros((ROWS,COLUMNS))
            self.wolfDist = np.zeros((ROWS,COLUMNS))    
    
            self.species_distributions(self.habitatDist, self.grassDist, self.sheepDist, self.wolfDist)

            for i in range(ROWS):
              for j in range(COLUMNS):
                if self.patches[i][j].habitat:
                    self.habitatDist[i][j]=1
            np.savetxt('habitatDist_run%d.csv' %self.runID, self.habitatDist, delimiter=",")


    def _create_patches(self):
        for i in range(ROWS):
            row = []
            for j in range(COLUMNS):
                row.append(Cell())
            
            self.patches.append(row)
                
    def _initialise_patches(self):
        # destroy patches
        x_coord = rnd.randint(0,COLUMNS-1)
        y_coord = rnd.randint(0,ROWS-1)
        while self.destroyedPatches < self.numberDestroyedPatches: #NUMBER_DESTROYED_PATCHES:
            if self.patches[x_coord][y_coord].habitat:
                self.patches[x_coord][y_coord].habitat=False
                self.destroyedPatches += 1
            x_coord = rnd.randint(0,COLUMNS-1)
            y_coord = rnd.randint(0,ROWS-1) 
        # create grass    
        for i in range(ROWS):
            for j in range(COLUMNS):
                self.patches[i][j].grass = Grass(i, j)
        x_coord = rnd.randint(0,COLUMNS-1)
        y_coord = rnd.randint(0,ROWS-1)
        while self.grassCount < INIT_NUMBER_GRASS:
            if self.patches[x_coord][y_coord].grass.state==False and self.patches[x_coord][y_coord].habitat:
                self.patches[x_coord][y_coord].grass.state=True
                self.grassCount += 1
            x_coord = rnd.randint(0,COLUMNS-1)
            y_coord = rnd.randint(0,ROWS-1) 
        # create sheep
        x_coord = rnd.randint(0,COLUMNS-1)
        y_coord = rnd.randint(0,ROWS-1)
        while self.sheepCount < INIT_NUMBER_SHEEP:
            if self.patches[x_coord][y_coord].sheep==None and self.patches[x_coord][y_coord].habitat:
                self.createSheep(x_coord, y_coord)
            x_coord = rnd.randint(0,COLUMNS-1)
            y_coord = rnd.randint(0,ROWS-1)        
        # create wolves    
        x_coord = rnd.randint(0,COLUMNS-1)
        y_coord = rnd.randint(0,ROWS-1)
        while self.wolfCount < INIT_NUMBER_WOLVES:
            if self.patches[x_coord][y_coord].wolf==None and self.patches[x_coord][y_coord].habitat:
                self.createWolf(x_coord,y_coord)
            x_coord = rnd.randint(0,COLUMNS-1)
            y_coord = rnd.randint(0,ROWS-1)        
                    

    def species_distributions(self, habitatDist, grassDist, sheepDist, wolfDist):
        
        for i in range(ROWS):
            for j in range(COLUMNS):
                #if self.patches[i][j].habitat:
                #    self.habitatDist[i][j]=1
                if self.patches[i][j].grass.state==True:
                    grassDist[i,j]=1
                if self.patches[i][j].sheep!=None:
                    sheepDist[i,j]=1
                if self.patches[i][j].wolf!=None:
                    wolfDist[i,j]=1
                    
    def timeSeries_append(self, ti):
        self.timeSeries[0,ti+1] = self.grassCount
        self.timeSeries[1,ti+1] = self.sheepCount
        self.timeSeries[2,ti+1] = self.wolfCount
                            
    def __str__(self):
        return "This is a landscape of %d by %d cells.\nIt contains %d sheep, and %d wolves" % (ROWS, COLUMNS, self.sheepCount, self.wolfCount)
		


    def update(self, ti):
        
        starvedSheep = []
        starvedWolves = []
        
        for s in self.sheep:
            if self.sheep[s].alive():
                prev_i,prev_j = (self.sheep[s].i,self.sheep[s].j)
                new_ij = self.sheep[s].move(self)
                if new_ij != (prev_i,prev_j):
                	self.patches[new_ij[0]][new_ij[1]].sheep = self.sheep[s]
                	self.patches[prev_i][prev_j].sheep = None
            else:
                starvedSheep.append(s)
                #print("Sheep starved")
                
        for w in self.wolves:
            if self.wolves[w].alive():
                prev_i,prev_j = (self.wolves[w].i,self.wolves[w].j)
                new_ij = self.wolves[w].move(self)
                if new_ij != (prev_i,prev_j):
                    self.patches[new_ij[0]][new_ij[1]].wolf = self.wolves[w]
                    self.patches[prev_i][prev_j].wolf = None
            else:
                starvedWolves.append(w)
                #print("wolf starved")

        for s in starvedSheep:
            self.deleteSheep(s)
        for w in starvedWolves:
            self.deleteWolf(w)

        for w in self.wolves:
            eat_ID = self.wolves[w].eat(self)
            if (eat_ID!=None):
                self.deleteSheep(eat_ID)
                #print("Sheep eaten")
                
        for s in self.sheep:
            eat_ij = self.sheep[s].eat(self)
            if eat_ij!=None:
                self.patches[eat_ij[0]][eat_ij[1]].grass.eaten()
                self.grassCount -= 1

        for i in range(ROWS):
            for j in range(COLUMNS):
                if self.patches[i][j].habitat:
                    if self.patches[i][j].grass.grow():
                        self.grassCount += 1
        
        reproducingSheep = []
        reproducingWolves = []
                    
        for s in self.sheep:
            if self.sheep[s].reproduce(self):
                reproducingSheep.append(s)
        for s in reproducingSheep:
            newEnergy = []
            if self.sheep[s].reproduce(self):
                spawn_ij = self.sheep[s].spawn(self, newEnergy)
                self.createSheep(spawn_ij[0], spawn_ij[1], newEnergy[0])
            #print("new sheep spawned")

        for w in self.wolves:
            if self.wolves[w].reproduce(self):
                reproducingWolves.append(w)
        for w in reproducingWolves:
            newEnergy = []
            if self.wolves[w].reproduce(self):
                spawn_ij = self.wolves[w].spawn(self, newEnergy)
                self.createWolf(spawn_ij[0], spawn_ij[1], newEnergy[0])
            #print("new wolf spawned")
            
        if self.animate:
            self.updatePlot()
        if self.timeSeries!=None:
            self.timeSeries_append(ti)
            
        if self.saveSpeciesDists==True and np.mod(ti, self.saveEvery)==0:
    
            self.grassDist = np.zeros((ROWS,COLUMNS))
            self.sheepDist = np.zeros((ROWS,COLUMNS))
            self.wolfDist = np.zeros((ROWS,COLUMNS))    
    
            self.species_distributions(self.habitatDist, self.grassDist, self.sheepDist, self.wolfDist)
            np.savetxt('grassDist_run%d_iteration%d.csv' % (self.runID, ti), self.grassDist, delimiter=",")
            np.savetxt('sheepDist_run%d_iteration%d.csv' % (self.runID, ti), self.sheepDist, delimiter=",")
            np.savetxt('wolfDist_run%d_iteration%d.csv' % (self.runID, ti), self.wolfDist, delimiter=",")
    
    
    def deleteSheep(self, sheepID):
        deadSheep = self.sheep[sheepID]
        self.patches[deadSheep.i][deadSheep.j].sheep = None
        del self.sheep[sheepID]
        self.sheepCount -= 1  

    def deleteWolf(self, wolfID):
        deadWolf = self.wolves[wolfID]
        self.patches[deadWolf.i][deadWolf.j].wolf = None
        del self.wolves[wolfID]
        self.wolfCount -= 1  
 
    def createSheep(self, x, y, energy=None):             
        self.sheep[self.sheepIDTracker] = Sheep(x, y, self.sheepIDTracker, energy)
        self.patches[x][y].sheep = self.sheep[self.sheepIDTracker]
        self.sheepCount += 1
        self.sheepIDTracker += 1
        
    def createWolf(self, x, y, energy=None):
        self.wolves[self.wolfIDTracker] = Wolf(x, y, self.wolfIDTracker, energy)                
        self.patches[x][y].wolf = self.wolves[self.wolfIDTracker]
        self.wolfCount += 1
        self.wolfIDTracker += 1

    def updatePlot(self):
        #self.habitatDist = np.zeros((ROWS,COLUMNS))
        self.grassDist = np.zeros((ROWS,COLUMNS))
        self.sheepDist = np.zeros((ROWS,COLUMNS))
        self.wolfDist = np.zeros((ROWS,COLUMNS))    
        self.species_distributions(self.habitatDist, self.grassDist, self.sheepDist, self.wolfDist)
        
        self.p1.set_data(self.habitatDist)        
        self.p2.set_data(self.grassDist)        
        self.p3.set_data(self.sheepDist)
        self.p4.set_data(self.wolfDist)        
        plt.draw()
        time.sleep(self.rest)

    def saveParameters(self):
        f = open('parameters.txt', 'w')
        
        f.write('runID = %d\n' %self.runID)        
        f.write('TIMESTEPS = %d\n' %self.T)
        f.write('DESTROYED_PATCHES = %d\n' %self.numberDestroyedPatches)
        f.write('SAVE_DIST_EVERY = %d\n' %self.saveEvery)
        
        f.write('\n***********************************************\n')        
        f.write('from configuuration file...\n')
        f.write('ROWS = %d\n' %ROWS)
        f.write('COLUMNS = %d\n' %COLUMNS)    
        f.write('INIT_NUMBER_GRASS = %d\n' %INIT_NUMBER_GRASS)
        f.write('INIT_NUMBER_SHEEP = %d\n' %INIT_NUMBER_SHEEP)        
        f.write('INIT_NUMBER_WOLVES = %d\n' %INIT_NUMBER_WOLVES)
        f.write('P_REPRODUCE_SHEEP = %d\n' %P_REPRODUCE_SHEEP)
        f.write('P_REPRODUCE_WOLF = %d\n' %P_REPRODUCE_WOLF)
        f.write('SHEEP_GAIN_FROM_FOOD = %d\n' %SHEEP_GAIN_FROM_FOOD)
        f.write('WOLF_GAIN_FROM_FOOD = %d\n' %WOLF_GAIN_FROM_FOOD)
        f.write('GRASS_REGROWTH_TIME = %d\n' %GRASS_REGROWTH_TIME)
        f.write('\n***********************************************\n')        
        f.close()
        
class Cell():
    
    def __init__(self):
        self.grass = None
        self.sheep = None
        self.wolf  = None
        self.habitat = True   # True -> pristine habitat

  
if __name__ == '__main__':

    T = 10
    rest = 0.0

    L = Landscape(True, False, T, rest, False)
    print(L)

    for t in range(T):
        L.update(t)

    print(L)
    
    # save series to file
    #np.savetxt('test.csv', L.timeSeries, delimiter=",")
    
    fig2 = plt.figure()
    ax1fig2 = fig2.add_subplot(111)
    ax1fig2.plot(range(T+1), L.timeSeries[0,:]/4, 'g')
    ax1fig2.plot(range(T+1), L.timeSeries[1,:], 'b')
    ax1fig2.plot(range(T+1), L.timeSeries[2,:], 'r')
    plt.show(fig2)
