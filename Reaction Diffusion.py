import pygame
pygame.init()

WIDTH = 160
HEIGHT = 80

SCREEN = pygame.display.set_mode((WIDTH*10,HEIGHT*10))

DA = 1
DB = 0.5
FEED = 0.055
KILL = 0.062

grid = [[{'a':1,'b':0} for _ in range(WIDTH)] for _ in range(HEIGHT)]

for i in range(10):
    for j in range(5):
        grid[i][j]['b'] = 1

def update(grid):
    gnew = grid[:]
    for i in range(HEIGHT):
        for j in range(WIDTH):
            a = grid[i][j]['a']
            b = grid[i][j]['b']
            gnew[i][j]['a'] = a+(DA*Laplase('a',i,j,grid)-a*b*b+FEED*(1-a))
            gnew[i][j]['b'] = b+(DB*Laplase('b',i,j,grid)+a*b*b-(FEED+KILL)*b)
    return gnew

def Laplase(var,i,j,grid):
    suma = 0 - grid[i][j][var]
    suma += grid[(i-1)%HEIGHT][j][var]*0.2
    suma += grid[(i+1)%HEIGHT][j][var]*0.2
    suma += grid[i][(j-1)%WIDTH][var]*0.2
    suma += grid[i][(j+1)%WIDTH][var]*0.2
    suma += grid[(i+1)%HEIGHT][(j+1)%WIDTH][var]*0.05
    suma += grid[(i+1)%HEIGHT][(j-1)%WIDTH][var]*0.05
    suma += grid[(i-1)%HEIGHT][(j+1)%WIDTH][var]*0.05
    suma += grid[(i-1)%HEIGHT][(j-1)%WIDTH][var]*0.05
    if suma not in range(256): suma = 0.5
    return suma

def draw(grid):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            pygame.draw.rect(SCREEN, (0,max(min(abs(grid[i][j]['a']*255),255),0),max(min(abs(grid[i][j]['b']*255),255),0)), pygame.rect.Rect(j*10, i*10, 10, 10))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
    
    gnew = update(grid)
    draw(gnew)
    grid = gnew
    pygame.display.update()