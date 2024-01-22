import pygame, numpy, random, colorsys


screenSize = (1400,800)
sizex,sizey = 1400,800
sequence = 'rl'       #'lrrll'  # '55 rrlrrslr' 'lrs' # 'slls' 'rlsrss' 'slrssslrrrsls' '32 rllllrrlrrslsslssrsrrslrrssrrslssslrsslsrlllrrlsrrrrs' '53 lrs' 'rlsrls' ''
speed = 100
ants = 99

randomAll = False

# colors = [(0,0,0),(55,55,55),(100,100,100),(60,60,150),(0,0,255),(0,150,255),(0,255,200),(50,255,100),(0,255,0),(255,255,0),(255,100,50),(255,0,0)]
betterColor = True
betterColorLength = 60
colorRange = (random.randint(0, 360),random.randint(0, 360)) #(0,0) # 0-360, 0-360
colorSkip = 2


def newColorRange(colorRange):
    global colors
    colors = [(0,0,0)]
    colorRangeInt = ((colorRange[1]/360+int(colorRange[1] <= colorRange[0]))-colorRange[0]/360)/(betterColorLength)
    for i in range(betterColorLength):
        var = colorSkip*i*colorRangeInt+colorRange[0]/360
        color = colorsys.hls_to_rgb(var, 0.5, 1)
        colors.append((color[0]*255,color[1]*255,color[2]*255))
if betterColor: newColorRange(colorRange)

def randomAllStats():
    global ants,sequence
    ants = random.randint(1, 60)
    sequence = ''
    if betterColor: var = betterColorLength
    else: var = 12
    for _ in range(random.randint(2, var)):
        sequence += random.choice(['r','l','s'])
    print(ants,sequence)

if randomAll:
    randomAllStats()

pygame.init()
mainScreen = pygame.display.set_mode(screenSize)
def setUp():
    return numpy.zeros((sizex,sizey))
grid = setUp()

def drawGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(mainScreen, colors[int(grid[i][j])], pygame.Rect(i*screenSize[0]/sizex,j*screenSize[1]/sizey,screenSize[0]/sizex,screenSize[1]/sizey))
    

def drawTiles(list,grid,colors):
    for k in range(len(list)):
        i = list[k][0]
        j = list[k][1]
        pygame.draw.rect(mainScreen, colors[int(grid[i][j])], pygame.Rect(i*screenSize[0]/sizex,j*screenSize[1]/sizey,screenSize[0]/sizex,screenSize[1]/sizey))

class antClass:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.dir = 1
    def right(self):
        self.dir = (self.dir + 1)%4
    def left(self):
        self.dir = (self.dir + 3)%4
    def forward(self, grid):
        list = (self.x, self.y)
        grid[self.x][self.y] = (grid[self.x][self.y]+1)%len(sequence)
        dirList = [(0,1),(1,0),(0,-1),(-1,0)]
        self.x = (self.x + dirList[self.dir][0])%sizex
        self.y = (self.y + dirList[self.dir][1])%sizey
        return list

antList = []
for _ in range(ants):
    antList.append(antClass(sizex//2,sizey//2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                newColorRange((random.randint(0, 360),random.randint(0, 720)))
                drawGrid(grid)
            if event.key == pygame.K_r:
                grid = setUp()
                mainScreen.fill(0)
            if event.key == pygame.K_SPACE:
                betterColorLength = random.randint(2, 60)
                grid = setUp()
                mainScreen.fill(0)
                antList = []
                randomAllStats()
                for _ in range(ants):
                    antList.append(antClass(sizex//2,sizey//2))
                newColorRange((random.randint(0, 360),random.randint(0, 720)))

    tileList = []

    for i in range(speed): 
        for ant in antList:
            if sequence[int(grid[ant.x][ant.y])].lower() == 'r':
                ant.right()
            elif sequence[int(grid[ant.x][ant.y])].lower() == 'l':
                ant.left()
            tileList.append(ant.forward(grid))
    
    drawTiles(tileList, grid, colors)
    #drawGrid(grid)
    pygame.display.update()
