import pygame
from math import cos,sin,radians
pygame.init()

size = (1400,780)
mainScreen = pygame.display.set_mode(size)

d = 1
n = 50

def draw(n,d):
    points = []
    colors = [(255,255,255),(170,170,170),(120,120,120),(90,90,90),(60,60,60),(30,30,30)]
    for j in range(7):
        for i in range(360):
            k = i * d
            r = 300 * sin(radians(n*k))
            x = r * cos(radians(k))
            y = r * sin(radians(k))
            points.append((x+700,y+390))
        #d += 0.5

        pygame.draw.lines(mainScreen, colors[-j], False, points)
    mainScreen.blit(pygame.font.Font(None, 70).render(str(n), True, (255,255,255)), (1200,50))
    mainScreen.blit(pygame.font.Font(None, 40).render(str(d), True, (255,255,255)), (1250,150))
    pygame.display.update()

clock = pygame.time.Clock()

running = True
while running:
    mainScreen.fill(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.time.wait(1500)
    draw(n,d)
    d+=1
    if d > 180 and d%2 == 1 or d>360: 
        d = 1
        n += 1
    clock.tick(30)
    #clock.tick(40*(50/(50+n)))