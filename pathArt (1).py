import random, pygame

size = (20,10)
screenSize = (1550,680)

def NewPath(enter,ext):
    start = [[(size[0]-2)/2,size[1]-2],[1,(size[1]-2)/2],[(size[0]-2)/2,1],[size[0]-2,(size[1]-2)/2]][enter -1]
    leave = [[size[1]-2,1],[size[0]-2,(size[1]/2)],[size[0]/2,size[1]-2],[1,size[1]/2]][ext -1]
    for i in range(2):
        start[i] = int(start[i])
        leave[i] = int(leave[i])

    matrx = []
    running = True
    while running:
        matrx=[]
        for i in range(size[1]):
            matrx.append(([9]*size[0])[:])
        for i in range(len(matrx)-3):
            for j in range(len(matrx[i])-2):
                matrx[i+1][j+1] = random.randint(1,8)
        pos = []
        head = start
        for p in range(100):
            matrx[head[1]][head[0]] = 9
            pos.append(head)
            if head[1] == 9: break
            NheadV = min(matrx[head[1]+1][head[0]],matrx[head[1]-1][head[0]],matrx[head[1]][head[0]+1],matrx[head[1]][head[0]-1])
            if NheadV == matrx[head[1]+1][head[0]]: NheadP = [head[1]+1,head[0]]
            elif NheadV == matrx[head[1]-1][head[0]]: NheadP = [head[1]-1,head[0]]
            elif NheadV == matrx[head[1]][head[0]+1]: NheadP = [head[1],head[0]+1]
            else: NheadP = [head[1],head[0]-1]
            matrx[head[1]+1][head[0]],matrx[head[1]-1][head[0]],matrx[head[1]][head[0]+1],matrx[head[1]][head[0]-1] = 9,9,9,9
            head = [NheadP[1],NheadP[0]]
            if head == leave:
                goodOne = True
                for i in pos:
                    if ([i[0]-1,i[1]] in pos and [i[0],i[1]+1] in pos and [i[0],i[1]-1] in pos) or ([i[0]+1,i[1]] in pos and [i[0],i[1]+1] in pos and [i[0],i[1]-1] in pos) or ([i[0]+1,i[1]] in pos and [i[0]-1,i[1]] in pos and [i[0],i[1]-1] in pos) or ([i[0]+1,i[1]] in pos and [i[0]-1,i[1]] in pos and [i[0],i[1]+1] in pos): goodOne = False
                if len(pos) > 16 and goodOne == True: 
                    running = False
                    pos.append(head)
                    print(p)
                    break
                else:
                    break
    return pos


pygame.init()

Display = pygame.display.set_mode(screenSize)
grey = (0,0,0)
Display.fill(grey)
pixle = pygame.PixelArray(Display)

def run(color,deley):
    global list

    for i in list:
        pygame.draw.rect(Display, [(220,220,220),(random.randint(10,200),random.randint(10,200),random.randint(10,200)),(0,0,0)][color], ((i[0]-1)*80+67,(i[1]-1)*67+67,68,56))
        pygame.display.update()
        pygame.time.delay(deley)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        
    for _ in range(8):
        int1 = random.randint(1, 4)
        int2 = random.randint(1, 4)
        while int1 + 2 == int2 or int1 -2 == int2:
            int2 = random.randint(1, 4)
        list = NewPath(int1, int2)

        run(0,15)
        pygame.time.delay(10)
        pygame.display.update()
        run(1,7)
    pygame.time.delay(500)
    for _ in range(8):
        int1 = random.randint(1, 4)
        int2 = random.randint(1, 4)
        while int1 + 2 == int2 or int1 -2 == int2:
            int2 = random.randint(1, 4)
        list = NewPath(int1, int2)

        run(0,15)
        pygame.time.delay(100)
        pygame.display.update()
        run(2,7)