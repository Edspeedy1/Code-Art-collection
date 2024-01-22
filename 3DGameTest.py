import pygame,math

pygame.init()

mainScreen = pygame.display.set_mode((1200,680))
pygame.display.set_caption("Game")

playerXY = [600,450]

pygame.draw.circle(mainScreen, (255,255,255), playerXY, 10)

running = True
w,a,s,d,q,e = False,False,False,False,False,False
direction = 0

def show(distance, pixel, res, color):
    global mainScreen
    brightness = 1/(distance**(1/4))

    pygame.draw.rect(mainScreen, [(0,200*brightness,200*brightness),(0,0,220*brightness),(210*brightness,0,100*brightness)][color], (pixel*res, -70+distance/2, res, 800 - distance/1))

def inside(pos,center,radius):
    distance = ((pos[0]-center[0])**2+(pos[1]-center[1])**2)**(1/2)
    return distance < radius

def singleRay(direction):
    global playerXY

    rayXY = playerXY[:]
    distance = 0
    while True:
        distance += 2
        rayXY[0] += 2*math.sin(math.radians(direction))
        rayXY[1] -= 2*math.cos(math.radians(direction))
        if rayXY[0] <= 0 or rayXY[0] >= 1200:
            color = 1
            break
        if rayXY[1] <= 0 or rayXY[1] >= 900:
            color = 0
            break
        if inside(rayXY, (300,400), 100):
            color = 2
            break

    return [distance, color]



def rayCast(direction):
    global mainScreen,playerXY
    FOV = 80
    res = 10
    rayDirection = (direction - FOV/2)%360
    #print(rayDirection, direction)
    xDir = 0


    for i in range(int(1200/res)):
        distance = singleRay(rayDirection)
        show(distance[0], xDir, res, distance[1])
        xDir += 1
        rayDirection += FOV/(1200/res)
        rayDirection = rayDirection%360

speed = 10

while running:
    mainScreen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: w = True
            if event.key == pygame.K_s: s = True
            if event.key == pygame.K_a: a = True
            if event.key == pygame.K_d: d = True
            if event.key == pygame.K_q: q = True
            if event.key == pygame.K_e: e = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w: w = False
            if event.key == pygame.K_s: s = False
            if event.key == pygame.K_a: a = False
            if event.key == pygame.K_d: d = False
            if event.key == pygame.K_q: q = False
            if event.key == pygame.K_e: e = False



    if w:
        playerXY[0] += speed*math.sin(math.radians(direction))
        playerXY[1] -= speed*math.cos(math.radians(direction))
    if a:
        playerXY[0] -= speed*math.sin(math.radians(direction+90))
        playerXY[1] += speed*math.cos(math.radians(direction+90))
    if s:
        playerXY[0] -= speed*math.sin(math.radians(direction))
        playerXY[1] += speed*math.cos(math.radians(direction))
    if d:
        playerXY[0] -= speed*math.sin(math.radians(direction-90))
        playerXY[1] += speed*math.cos(math.radians(direction-90))

    if q: direction -= 2
    if e: direction += 2
    direction = direction%360
    
    if playerXY[0] <= 10: 
        playerXY[0] = 10
    if playerXY[1] <= 10: 
        playerXY[1] = 10
    if playerXY[0] >= 1190: 
        playerXY[0] = 1190
    if playerXY[1] >= 890: 
        playerXY[1] = 890

    rayCast(direction)

    pygame.display.update()
                