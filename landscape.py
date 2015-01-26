from species import * #Individual, Grass, Sheep
import random as rnd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)

import time

from configure import ROWS, COLUMNS, INIT_NUMBER_SHEEP, INIT_NUMBER_WOLVES, INIT_NUMBER_GRASS

class Landscape():
	
    def __init__(self):
        
        self.sheepIDTracker = 0
        self.wolfIDTracker = 0   # such that every individual born can be given a unique ID
        self.sheepCount = 0
        self.wolfCount = 0
        self.grassCount = 0
        self.sheep = {}
        self.wolves = {}
        
        self.patches = []
        self._create_patches()
        self._initialise_patches()
        self.patches[0][0].grass.state = False  #JUST FOR TEMPORARY

    def _create_patches(self):
        for i in range(ROWS):
            row = []
            for j in range(COLUMNS):
                row.append(Cell())
            
            self.patches.append(row)
                
    def _initialise_patches(self):
        # create grass    
        for i in range(ROWS):
            for j in range(COLUMNS):
                self.patches[i][j].grass = Grass(i, j)
        x_coord = rnd.randint(0,COLUMNS-1)
        y_coord = rnd.randint(0,ROWS-1)
        while self.grassCount < INIT_NUMBER_GRASS:
            if self.patches[x_coord][y_coord].grass.state==False:
                self.patches[x_coord][y_coord].grass.state=True
                self.grassCount += 1
            x_coord = rnd.randint(0,COLUMNS-1)
            y_coord = rnd.randint(0,ROWS-1) 
        # create sheep
        x_coord = rnd.randint(0,COLUMNS-1)
        y_coord = rnd.randint(0,ROWS-1)
        while self.sheepCount < INIT_NUMBER_SHEEP:
            if self.patches[x_coord][y_coord].sheep==None:
                self.createSheep(x_coord, y_coord)
            x_coord = rnd.randint(0,COLUMNS-1)
            y_coord = rnd.randint(0,ROWS-1)        
        # create wolves    
        x_coord = rnd.randint(0,COLUMNS-1)
        y_coord = rnd.randint(0,ROWS-1)
        while self.wolfCount < INIT_NUMBER_WOLVES:
            if self.patches[x_coord][y_coord].wolf==None:
                self.createWolf(x_coord,y_coord)
            x_coord = rnd.randint(0,COLUMNS-1)
            y_coord = rnd.randint(0,ROWS-1)        
                    

    def species_distributions(self, grassDist, sheepDist, wolfDist, timeSeries, ti):
        
        for i in range(ROWS):
            for j in range(COLUMNS):
                if self.patches[i][j].grass.state==True:
                    grassDist[i,j]=1
                if self.patches[i][j].sheep!=None:
                    sheepDist[i,j]=1
                if self.patches[i][j].wolf!=None:
                    wolfDist[i,j]=1
                    
        timeSeries[0,ti] = self.grassCount
        timeSeries[1,ti] = self.sheepCount
        timeSeries[2,ti] = self.wolfCount
                    
    def __str__(self):
        return "This is a landscape of %d by %d cells.\nIt contains %d sheep, and %d wolves" % (ROWS, COLUMNS, self.sheepCount, self.wolfCount)
		


    def update(self):
        
        starvedSheep = []
        starvedWolves = []
        
        for s in self.sheep:
            if self.sheep[s].alive():
                prev_i,prev_j = (self.sheep[s].i,self.sheep[s].j)
                new_ij = self.sheep[s].move(self)
                self.patches[new_ij[0]][new_ij[1]].sheep = self.sheep[s]
                self.patches[prev_i][prev_j].sheep = None
            else:
                starvedSheep.append(s)
                print("Sheep starved")
                
        for w in self.wolves:
            if self.wolves[w].alive():
                prev_i,prev_j = (self.wolves[w].i,self.wolves[w].j)
                new_ij = self.wolves[w].move(self)
                self.patches[new_ij[0]][new_ij[1]].wolf = self.wolves[w]
                self.patches[prev_i][prev_j].wolf = None
            else:
                starvedWolves.append(w)
                print("wolf starved")

        for s in starvedSheep:
            self.deleteSheep(s)
        for w in starvedWolves:
            self.deleteWolf(w)

        for w in self.wolves:
            eat_ID = self.wolves[w].eat(self)
            if (eat_ID!=None):
                self.deleteSheep(eat_ID)
                print("Sheep eaten")
                
        for s in self.sheep:
            eat_ij = self.sheep[s].eat(self)
            if eat_ij!=None:
                self.patches[eat_ij[0]][eat_ij[1]].grass.eaten()
                self.grassCount -= 1

        for i in range(ROWS):
            for j in range(COLUMNS):
                if self.patches[i][j].grass.grow():
                    self.grassCount += 1
        
        reproducingSheep = []
        reproducingWolves = []
                    
        for s in self.sheep:
            if self.sheep[s].reproduce():
                reproducingSheep.append(s)
        for s in reproducingSheep:
            spawn_ij = self.sheep[s].spawn(self)
            self.createSheep(spawn_ij[0], spawn_ij[1])
            print("new sheep spawned")

        for w in self.wolves:
            if self.wolves[w].reproduce():
                reproducingWolves.append(w)
        for w in reproducingWolves:
            spawn_ij = self.wolves[w].spawn(self)
            self.createWolf(spawn_ij[0], spawn_ij[1])
            print("new wolf spawned")
    
    
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
 
    def createSheep(self, x, y):             
        self.sheep[self.sheepIDTracker] = Sheep(x, y, self.sheepIDTracker)
        self.patches[x][y].sheep = self.sheep[self.sheepIDTracker]
        self.sheepCount += 1
        self.sheepIDTracker += 1
        
    def createWolf(self, x, y):
        self.wolves[self.wolfIDTracker] = Wolf(x, y, self.wolfIDTracker)                
        self.patches[x][y].wolf = self.wolves[self.wolfIDTracker]
        self.wolfCount += 1
        self.wolfIDTracker += 1

class Cell():
    
    def __init__(self):
        self.grass = None
        self.sheep = None
        self.wolf  = None
        self.habitat = 1   # 1 -> pristine habitat

  
if __name__ == '__main__':

    T = 1000
    rest = 0.0
    timeSeries = np.zeros((3, T+1))    
    
    grassDist = np.zeros((ROWS,COLUMNS))
    sheepDist = np.zeros((ROWS,COLUMNS))
    wolfDist = np.zeros((ROWS,COLUMNS))    
    
    L = Landscape()
    print(L)
    
    fig, (ax1, ax2, ax3) = plt.subplots(1,3)
    L.species_distributions(grassDist, sheepDist, wolfDist, timeSeries, 0)
    
    p1 = ax1.imshow(grassDist, cmap='Greens', interpolation=None)    
    p2 = ax2.imshow(sheepDist, cmap='Blues', interpolation=None)    
    p3 = ax3.imshow(wolfDist, cmap='Reds', interpolation=None)    
    plt.draw()

    time.sleep(1)

    for t in range(T):
        L.update()
        grassDist = np.zeros((ROWS,COLUMNS))
        sheepDist = np.zeros((ROWS,COLUMNS))
        wolfDist = np.zeros((ROWS,COLUMNS))    
        L.species_distributions(grassDist, sheepDist, wolfDist, timeSeries, t+1)
        
        p1.set_data(grassDist)        
        p2.set_data(sheepDist)
        p3.set_data(wolfDist)        
        plt.draw()
        time.sleep(rest)
    
    print(L)
    
    fig2 = plt.figure()
    ax1fig2 = fig2.add_subplot(111)
    ax1fig2.plot(range(T+1), timeSeries[0,:]/4, 'g')
    ax1fig2.plot(range(T+1), timeSeries[1,:], 'b')
    ax1fig2.plot(range(T+1), timeSeries[2,:], 'r')
    plt.show(fig2)