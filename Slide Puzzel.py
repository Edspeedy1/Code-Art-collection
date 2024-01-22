import pygame, random, time

SCREEN = pygame.display.set_mode((600,600))
GRIDSIZE = 8,8
img = pygame.transform.scale(pygame.image.load("eds.png"), (600,600))

GRID = [[img.subsurface((i*600/GRIDSIZE[0], j*600/GRIDSIZE[1], 600/GRIDSIZE[0], 600/GRIDSIZE[1])) for i in range(GRIDSIZE[0])] for j in range(GRIDSIZE[1])]
GRID[GRIDSIZE[0]-1][GRIDSIZE[1]-1] = 0
head = [GRIDSIZE[0]-1, GRIDSIZE[1]-1]

def draw():
    SCREEN.fill(0)
    for i in range(GRIDSIZE[0]):
        for j in range(GRIDSIZE[1]):
            try: SCREEN.blit(GRID[i][j], (j*600/GRIDSIZE[0],i*600/GRIDSIZE[1]))
            except: pygame.draw.rect(SCREEN, (50,50,60), (j*600/GRIDSIZE[0],i*600/GRIDSIZE[1], 600/GRIDSIZE[0],600/GRIDSIZE[1]))


def move(direction, head, grid):
    if direction == 'r' and head[1]+1<GRIDSIZE[1]:
        grid[head[0]][head[1]] = grid[head[0]][head[1]+1]
        grid[head[0]][head[1]+1] = 0
        head = [head[0],head[1]+1]
    elif direction == 'd' and head[0]+1<GRIDSIZE[0]:
        grid[head[0]][head[1]] = grid[head[0]+1][head[1]]
        grid[head[0]+1][head[1]] = 0
        head = [head[0]+1,head[1]]
    elif direction == 'l' and head[1]-1>=0:
        grid[head[0]][head[1]] = grid[head[0]][head[1]-1]
        grid[head[0]][head[1]-1] = 0
        head = [head[0],head[1]-1]
    elif direction == 'u' and head[0]-1 >=0:
        grid[head[0]][head[1]] = grid[head[0]-1][head[1]]
        grid[head[0]-1][head[1]] = 0
        head = [head[0]-1,head[1]]
    return grid, head


moveString = ''
running = True
randomize = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                randomize = True
            if event.key == pygame.K_UP:
                moveString += 'u'
            if event.key == pygame.K_RIGHT:
                moveString += 'r'
            if event.key == pygame.K_DOWN:
                moveString += 'd'
            if event.key == pygame.K_LEFT:
                moveString += 'l'
            if event.key == pygame.K_RSHIFT:
                print(time.time()-t)
                t = time.time()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                randomize = False
                t = time.time()
    if randomize:
        for _ in range(100):
            moveString += random.choice(('u','r','d','l'))
    for letter in moveString:
        GRID, head = move(letter, head, GRID)

    moveString = ''
    draw()
    pygame.display.update()