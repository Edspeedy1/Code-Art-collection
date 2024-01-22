var = [0]*32
def randomize():
    global var

    for i in range(31):
        var[31-i] = var[30-i]
    var[0] = (var[9]+var[30]+1)%2

    num = 1000000
    for i in range(32):
        num += var[31-i]*(2**i)
    return int(str(num)[3:7])

def random():
    return randomize()/10000
def randint(mini, maxi):
    return round(random()*(maxi-mini)+mini)

import pygame, colorsys
from random import randint
pygame.init()

seed = 393
screenSize = (1200,700)
size =(200,100)
mainScreen = pygame.display.set_mode(screenSize)

for _ in range(seed): randomize()

class cellClass:
    def __init__(self,i,j):
        self.i = i
        self.j = j
        self.visited = False
        self.walls = [True,True,True,True]
        self.num = 0
    
    def checkNeighbors(self, grid):
        top,right,bottom,left = True,True,True,True
        if self.j-1 >= 0: top = grid[self.i][self.j-1].visited
        if self.i+1 < size[0]: right = grid[self.i+1][self.j].visited
        if self.j+1 < size[1]: bottom = grid[self.i][self.j+1].visited
        if self.i-1 >= 0: left = grid[self.i-1][self.j].visited
        return (top,right,bottom,left)

    def checkCount(self, grid):
        top,right,bottom,left = size[0]*size[1]+1,size[0]*size[1]+1,size[0]*size[1]+1,size[0]*size[1]+1
        if self.j-1 >= 0: top = grid[self.i][self.j-1].num
        if self.i+1 < size[0]: right = grid[self.i+1][self.j].num
        if self.j+1 < size[1]: bottom = grid[self.i][self.j+1].num
        if self.i-1 >= 0: left = grid[self.i-1][self.j].num
        return (top,right,bottom,left)       

    def display(self, color):
        rect = pygame.Rect(self.i*(screenSize[0]/size[0])+(screenSize[0]/size[0])/4, self.j*(screenSize[1]/size[1])+(screenSize[1]/size[1])/4, (screenSize[0]/size[0])/2, (screenSize[1]/size[1])/2)
        pygame.draw.rect(mainScreen, color, rect)
        topWall = pygame.Rect(self.i*(screenSize[0]/size[0])+(screenSize[0]/size[0])/4, self.j*(screenSize[1]/size[1]), (screenSize[0]/size[0])/2, (screenSize[1]/size[1]/4))
        rightWall = pygame.Rect(self.i*(screenSize[0]/size[0]), self.j*(screenSize[1]/size[1])+(screenSize[1]/size[1])/4, (screenSize[0]/size[0])/4, (screenSize[1]/size[1])/2)
        bottomWall = pygame.Rect(self.i*(screenSize[0]/size[0])+(screenSize[0]/size[0])/4, (self.j+1)*(screenSize[1]/size[1])-(screenSize[1]/size[1]/4), (screenSize[0]/size[0])/2, (screenSize[1]/size[1]/4))
        leftWall = pygame.Rect((self.i+1)*(screenSize[0]/size[0])-(screenSize[0]/size[0])/4, self.j*(screenSize[1]/size[1])+(screenSize[1]/size[1])/4, (screenSize[0]/size[0])/4, (screenSize[1]/size[1])/2)
        for k in range(4):
            pygame.draw.rect(mainScreen, [color,(0,0,0)][self.walls[k]], (topWall,rightWall,bottomWall,leftWall)[k])

grid = []
for i in range(size[0]):
    grid.append([])
    for j in range(size[1]):
        grid[i].append(cellClass(i, j))

h = 0
v = 20
head = [0,0]
stack = [[0,0]]

tilesSeen = [cellClass(0, 0),cellClass(0, 0),cellClass(0, 0)]

clock = pygame.time.Clock()
#mainScreen.fill((255,255,255))
running = True
while running:
    randomize()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
            
    if len(stack) == 0: break

    grid[head[0]][head[1]].visited = True
    tilesSeen.append(grid[head[0]][head[1]])
    for k in range(3):
        tilesSeen[-k].display((150,200,255)) #(abs(int(colorsys.hsv_to_rgb(h, 50, v)[0]/10)),abs(int(colorsys.hsv_to_rgb(h, 50, v)[1]/10)),abs(int(colorsys.hsv_to_rgb(h, 50, v)[2]/10))))

    #grid[head[0]][head[1]].display((0,175,250))

    spots = grid[head[0]][head[1]].checkNeighbors(grid)
    if spots != (True,True,True,True):
        while True:
            rvar = randint(0, 3)
            if not spots[rvar]: break
        if rvar == 0: 
            grid[head[0]][head[1]].walls[0] = False
            head[1] -= 1
            grid[head[0]][head[1]].walls[2] = False
        elif rvar == 1: 
            grid[head[0]][head[1]].walls[3] = False
            head[0] += 1
            grid[head[0]][head[1]].walls[1] = False
        elif rvar == 2: 
            grid[head[0]][head[1]].walls[2] = False
            head[1] += 1
            grid[head[0]][head[1]].walls[0] = False
        elif rvar == 3: 
            grid[head[0]][head[1]].walls[1] = False
            head[0] -= 1
            grid[head[0]][head[1]].walls[3] = False
        stack.append(head[:])
        #clock.tick(60)
    else:
        head = stack[-1]
        stack.pop(-1)

    #clock.tick(60)
    pygame.display.update()
#clock.tick(0.1)

pygame.display.update()

# running = False

start = (0,0)
end = (size[0]-1,size[1]-1)
tilesSeen = []
active = [start]
nextActive = []
counter = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False

    for k in active:
        cell = grid[k[0]][k[1]]
        cell.num = counter
        cell.display((150,50,0))
        if not cell.walls[0] and grid[k[0]][k[1]-1].num == 0: nextActive.append((cell.i,cell.j-1))
        if not cell.walls[3] and grid[k[0]+1][k[1]].num == 0: nextActive.append((cell.i+1,cell.j))
        if not cell.walls[2] and grid[k[0]][k[1]+1].num == 0: nextActive.append((cell.i,cell.j+1))
        if not cell.walls[1] and grid[k[0]-1][k[1]].num == 0: nextActive.append((cell.i-1,cell.j))
        #clock.tick(60)
        if end == k:
            head = end
            currentNum = grid[head[0]][head[1]].num
            while running:
                if head[0] == 0 and head[1] == 0:
                    running = False
                    active = []
                    break
                cell = grid[head[0]][head[1]]
                spots = cell.checkCount(grid)
                if   spots[0] == currentNum-1: newCell = (cell.i,cell.j-1)
                elif spots[1] == currentNum-1: newCell = (cell.i+1,cell.j)
                elif spots[2] == currentNum-1: newCell = (cell.i,cell.j+1)
                elif spots[3] == currentNum-1: newCell = (cell.i-1,cell.j)
                currentNum -= 1
                grid[newCell[0]][newCell[1]].display((0,150,0))
                head = newCell
                pygame.display.update()
                # clock.tick(60)
            running = False
            break
    
    active = nextActive
    nextActive = []
    counter += 1
    pygame.display.update()
    # clock.tick(60)

# pygame.image.save(mainScreen, 'ScreenshotMaze1.png')

pygame.display.update()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False