from species import * #Individual, Grass, Sheep
import random as rnd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)

import time

from configure import ROWS, COLUMNS, INIT_NUMBER_SHEEP, INIT_NUMBER_WOLVES

class Landscape():
	
    def __init__(self):
        self.sheepCount = 0
        self.wolfCount = 0
        self.sheep = []
        self.wolves = []
        
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
        # create sheep
        x_coord = rnd.randint(0,COLUMNS-1)
        y_coord = rnd.randint(0,ROWS-1)
        while self.sheepCount < INIT_NUMBER_SHEEP:
            print(x_coord)
            print(y_coord)
            if self.patches[x_coord][y_coord].sheep==None:
                self.sheep.append(Sheep(x_coord, y_coord))
                self.patches[x_coord][y_coord].sheep = self.sheep[self.sheepCount]
                self.sheepCount += 1
            x_coord = rnd.randint(0,COLUMNS-1)
            y_coord = rnd.randint(0,ROWS-1)        
        # create wolves    
        x_coord = rnd.randint(0,COLUMNS-1)
        y_coord = rnd.randint(0,ROWS-1)
        while self.wolfCount < INIT_NUMBER_WOLVES:
            print(x_coord)
            print(y_coord)
            if self.patches[x_coord][y_coord].wolf==None:
                self.wolves.append(Wolf(x_coord, y_coord))
                self.patches[x_coord][y_coord].wolf = self.wolves[self.wolfCount]
                self.wolfCount += 1
            x_coord = rnd.randint(0,COLUMNS-1)
            y_coord = rnd.randint(0,ROWS-1)        
                    

    def species_distributions(self, grassDist, sheepDist, wolfDist):
        for i in range(ROWS):
            for j in range(COLUMNS):
                if self.patches[i][j].grass.state==True:
                    grassDist[i,j]=1
                if self.patches[i][j].sheep!=None:
                    sheepDist[i,j]=1
                if self.patches[i][j].wolf!=None:
                    wolfDist[i,j]=1
    def __str__(self):
        return "This is a landscape of %d by %d cells.\nIt contains %d sheep, and %d wolves" % (ROWS, COLUMNS, self.sheepCount, self.wolfCount)
		


    def update(self):
        for s in range(self.sheepCount):
            prev_i,prev_j = (self.sheep[s].i,self.sheep[s].j)
            new_ij = self.sheep[s].move(self)
            self.patches[new_ij[0]][new_ij[1]].sheep = self.sheep[s]
            self.patches[prev_i][prev_j].sheep = None

        for w in range(self.wolfCount):
            prev_i,prev_j = (self.wolves[w].i,self.wolves[w].j)
            new_ij = self.wolves[w].move(self)
            self.patches[new_ij[0]][new_ij[1]].wolf = self.wolves[w]
            self.patches[prev_i][prev_j].wolf = None

        for w in range(self.wolfCount):
            eat_ij = self.wolves[w].eat(self)
            if (eat_ij!=None):
                self.patches[eat_ij[0]][eat_ij[1]].sheep = None
                print("Sheep eaten")
                
# landscape to consist of an array of cells
class Cell():
    
    def __init__(self):
        self.grass = None
        self.sheep = None
        self.wolf  = None
        self.habitat = 1   # 1 -> pristine habitat

    def update(self, landscape):
    # DEPRICATED
        if (self.sheep!=None):
            new_ij = self.sheep.move(landscape)
            #print(landscape)
        else:
            new_ij=None
        return new_ij

if __name__ == '__main__':
    grassDist = np.zeros((ROWS,COLUMNS))
    sheepDist = np.zeros((ROWS,COLUMNS))
    wolfDist = np.zeros((ROWS,COLUMNS))    
    
    L = Landscape()
    print(L)
    
    fig, (ax1, ax2, ax3) = plt.subplots(1,3)
    L.species_distributions(grassDist, sheepDist, wolfDist)
    
    p1 = ax1.imshow(grassDist, cmap='Greens', interpolation=None)    
    p2 = ax2.imshow(sheepDist, cmap='Blues', interpolation=None)    
    p3 = ax3.imshow(wolfDist, cmap='Reds', interpolation=None)    
    plt.draw()

    time.sleep(1)

    T = 10
    rest = 0.2
    for t in range(T):
        L.update()
        grassDist = np.zeros((ROWS,COLUMNS))
        sheepDist = np.zeros((ROWS,COLUMNS))
        wolfDist = np.zeros((ROWS,COLUMNS))    
        L.species_distributions(grassDist, sheepDist, wolfDist)
        
        p2.set_data(sheepDist)
        p3.set_data(wolfDist)        
        plt.draw()
        time.sleep(rest)
    
    print(L)