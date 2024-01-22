import pygame, random
pygame.init()

gridSize = 100, 50
windowSize = 140, 70

SCREEN = pygame.display.set_mode(windowSize)
pygame.display.set_caption('Pixels Fighting')
pygame.display.set_icon(pygame.transform.scale(pygame.image.load('PixelsFightingIcon.png'), (32,32)))
scale = windowSize[0]//gridSize[0], windowSize[1]//gridSize[1]

def setUp():
    global GRID, C, scale
    GRID = [[2*i//gridSize[0] for j in range(gridSize[1])] for i in range(gridSize[0])]

    C = []
    for i in range(gridSize[0]*gridSize[1]): C.append((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))
    for i in range(gridSize[0]):
        for j in range(gridSize[1]):
            pygame.draw.rect(SCREEN, C[GRID[i][j]], (i*scale[0],j*scale[1],scale[0],scale[1]))

def update():
    global GRID
    GRID2 = GRID[:]
    for i in range(gridSize[0]):
        for j in range(gridSize[1]):
            if i != 0 and j != 0 and i != gridSize[0]-1 and j != gridSize[1]-1: 
                if GRID[i+1][j] == GRID[i-1][j] == GRID[i][j+1] == GRID[i][j-1] == GRID[i][j]: continue
                V = random.choice((GRID[i+1][j], GRID[i-1][j], GRID[i][j+1], GRID[i][j-1]))
            else:
                o = []
                if i != 0: o.append(GRID[i-1][j])
                if j != 0: o.append(GRID[i][j-1])
                if i != gridSize[0]-1: o.append(GRID[i+1][j])
                if j != gridSize[1]-1: o.append(GRID[i][j+1])
                V = random.choice(o)

            if V != GRID[i][j]:
                GRID2[i][j] = V
                pygame.draw.rect(SCREEN, C[V], (i*scale[0],j*scale[1],scale[0],scale[1]))
    GRID = GRID2[:]

setUp()
clock = pygame.time.Clock()

c = 0
running = True
while running:
    c += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: setUp()
    
    update()
    clock.tick(20)
    pygame.display.update()
    if c%50 == 0:
        s = 0
        for i in range(gridSize[0]):
            s += sum(GRID[i])
        cap = str(int(10000*(s/(gridSize[0]*gridSize[1])))/100)+'%'
        print(cap)
        pygame.display.set_caption('Pixels Fighting - ' +cap)
