from configure import ROWS, COLUMNS, SHEEP_GAIN_FROM_FOOD, WOLF_GAIN_FROM_FOOD, GRASS_REGROWTH_TIME
import random as rnd

class Individual():
	
    def __init__(self, species, i, j, ID):
        self.species = species
        self.energy  = 10          # how to assgin energies?
        self.i = i
        self.j = j
        self.ID = ID
        self.neighbours = Neighbourhood()
    
    def alive(self):    
        # check if individual has run out of energy
        if self.energy<=0:
            return False
        else:
            return True 
     
    def move(self, landscape, neighbour_list):
        # neighbour_list: list of which neighbouring cells contain the same species
        r = rnd.randint(0,7)
        while (r in neighbour_list):
            r = rnd.randint(0,7)
        prev_i = self.i
        prev_j = self.j    
        self.i,self.j = self.neighbours.return_ij(r, prev_i, prev_j)
        self.energy -= 1
        return (self.i,self.j)
    
class Grass(Individual):
    
    def __init__(self, i, j):
        Individual.__init__(self, "grass", i, j, 0)
        self.state = True             # True -> alive
        self.counter = 0
        #self.i = i
        #self.j = j
        
    def eaten(self):
        self.state = False
        self.counter = 0
        
    def grow(self):
        
        if self.state == False:
            counter += 1
            if counter == GRASS_REGROWTH_TIME:
                self.state = True
        
class Sheep(Individual):

    def __init__(self, i, j, ID):
        Individual.__init__(self, "sheep", i, j, ID)
        
    def move(self, landscape):
        # find neighbouring sheep
        neighbour_list = []
        for n in range(self.neighbours.N):
            coords = self.neighbours.return_ij(n, self.i, self.j)
            if (landscape.patches[coords[0]][coords[1]].sheep != None):
                # there be a sheep!
                neighbour_list.append(n)
        
        return Individual.move(self,landscape, neighbour_list)

    def eat(self, landscape):
        if (landscape.patches[self.i][self.j].grass.state):
            # I have food!
            self.energy += SHEEP_GAIN_FROM_FOOD
            eat_ij = (self.i,self.j)
        else:
            eat_ij = None
        return eat_ij

class Wolf(Individual):

    def __init__(self, i, j, ID):
        Individual.__init__(self, "wolf", i, j, ID)
        
    def move(self, landscape):
        # find neighbouring sheep
        neighbour_list = []
        for n in range(self.neighbours.N):
            coords = self.neighbours.return_ij(n, self.i, self.j)
            if (landscape.patches[coords[0]][coords[1]].wolf != None):
                # there be a sheep!
                neighbour_list.append(n)
        
        return Individual.move(self,landscape, neighbour_list)

    def eat(self, landscape):
        if (landscape.patches[self.i][self.j].sheep!=None):
            # I have food!
            self.energy += WOLF_GAIN_FROM_FOOD
            eat_ID = landscape.patches[self.i][self.j].sheep.ID
        else:
            eat_ID = None
        return eat_ID

class Neighbourhood():
    def __init__(self):
        self.name = "8_nearest_neighbours"
        self.N = 8
    def return_ij(self, n_id, i, j):
        # returns (x,y) of neighbour n_id based on i,j of individual        
        if (n_id==0):
            x = i-1
            y = j-1
        elif (n_id==1):
            x = i
            y = j-1    
        elif (n_id==2):
            x = i + 1
            y = j-1    
        elif (n_id==3):
            x = i -1
            y = j  
        elif (n_id==4):
            x = i+1
            y = j    
        elif (n_id==5):
            x = i-1
            y = j+1
        elif (n_id==6):
            x = i
            y = j+1    
        elif (n_id==7):
            x = i+1
            y = j+1
            
        if (x<0):
            x=ROWS-1
        if (x>=ROWS):
            x=0
        if (y<0):
            y=COLUMNS-1
        if (y>=COLUMNS):
            y=0
            
        return (x,y)