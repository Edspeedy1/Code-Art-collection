import pygame, random, threading
pygame.init()

SCREEN = pygame.display.set_mode((1200, 675))
PREVIEW = pygame.Surface((350,675//2))

def newPallet(size):
    varOp = [random.randint(0, 2) for _ in range(random.randint(1, size))]
    rmin, rmax = sorted((random.randint(0, 255), random.randint(0, 255)))
    while rmax < 180 or rmax-rmin < 40:
        rmin, rmax = sorted((random.randint(0, 255), random.randint(0, 255)))
    addAccent, AccentUncommon = bool(random.randint(0,3)), min(random.randint(-1, 15),random.randint(-1, 15))
    change = 0.5 if random.randint(0, 3) == 0 else 0.8 if random.randint(0, 2) == 0 else 4 if not random.randint(0, 10) else 1
    baseColor = [random.randint(0, 250) for _ in range(3)] if not random.randint(0, 2) else [0,0,0] if random.randint(0, 1) else [255,255,255]
    accentColor = [0,0,0] if random.randint(0, 2) else [255,255,255] if random.randint(0, 1) else [random.randint(0, 250) for _ in range(3)]
    return [varOp, rmax, rmin, addAccent, AccentUncommon, change, baseColor, accentColor]

STATS = newPallet(6)

def evaluateOptions(head, grid):
    D = [False,False,False,False]
    for j, i in enumerate(((0,-1), (0,1), (-1,0), (1,0))):
        if not outside((head[0] + i[0], head[1] + i[1]),(350,675//2)):
            if grid[head[0] + i[0]][head[1] + i[1]] == 0:
                D[j] = True
    return D

def outside(spot, size):
    return spot[0] < 0 or spot[1] < 0 or spot[0] >= size[0] or spot[1] >= size[1]

def makePreview(pallet):
    varOp, rmax, rmin, addAccent, AccentUncommon, change, color, accentColor = pallet[:]
    blackVar = False
    sinceAccentChange = 0
    head = [0,0]
    count = 0
    stack = [[0,0]]
    running2 = True
    GRID = [[0 for _ in range(675)] for _ in range(700)]
    while running2:
        if stack == []:
            running2 = False
        count += 1
        directions = evaluateOptions(head, GRID)
        if stack == []:
            break
        if directions == [False,False,False,False]: head = stack.pop()
        else:
            while True:
                var = random.randint(0, 3)
                if directions[var]: break
            head[0] += ((0,-1), (0,1), (-1,0), (1,0))[var][0]
            head[1] += ((0,-1), (0,1), (-1,0), (1,0))[var][1]
            GRID[head[0]][head[1]] = 1
            stack.append(head[:])
        
        var = random.choice(varOp)
        color[var] = max(min(color[var]+random.choice((-2,2))*change,rmax),rmin)
        nClr = [color[0],color[1],color[2]]
        if addAccent:
            sinceAccentChange += 1
            if random.randint(0,10000) - AccentUncommon*int(blackVar) <= 1 and sinceAccentChange > 500:
                sinceAccentChange = 0
                blackVar = not blackVar
            if blackVar: nClr = accentColor[:]
        
        # color editing
        if nClr[0] - nClr[1] > 0:
            a = (nClr[0] - nClr[1])*(nClr[0]/155)

            nClr[1] = max(nClr[1] - int(a)*2, 10)
            nClr[2] = max(nClr[2] - int(a), 10)

        pygame.draw.rect(PREVIEW, nClr, (head[0],head[1],1,1))
    
    return      # to stop before the crystalizing TODO

    CRYSTSIZE = 10
    nodeList = []
    for i in range(int(700/(CRYSTSIZE)+1)):
        a = []
        for j in range(int(675/(CRYSTSIZE))+1):
            a.append(Node(i*(CRYSTSIZE), j*CRYSTSIZE, CRYSTSIZE//2, color=accentColor))
        nodeList.append(a)
    
    for i in range(700):
        for j in range(675):
            zone = []
            for z in nodeList[max(i//CRYSTSIZE,0) : i//CRYSTSIZE+2]:
                zone +=  z[max(j//CRYSTSIZE,0) : j//CRYSTSIZE+2]
            zone.sort(key=lambda x: x.dist((i,j)))
            try: pygame.draw.rect(PREVIEW, zone[0].color, (i//2, j//2, 1, 1))
            except: pass
    draw()
    

boxList = []
class InputBox:
    def __init__(self, x, y, w, h, palletIndex):
        self.index = palletIndex
        self.w = w
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, w, h)
        self.color = [70,120,150]
        self.text = str(STATS[palletIndex]).replace('[', '').replace(']', '')
        self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)
        self.active = False
        boxList.append(self)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                if self.active:
                    self.deselect()
            self.color = [70,170,240] if self.active else [70,120,150]
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.deselect()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)

    def deselect(self):
        global STATS
        self.active = False
        self.color = [70,120,150]
        if self.index in {0,6,7}:
            L = self.text.split(',')
            for i in range(len(L)):
                try:L[i] = int(L[i])
                except: L[i] = 0
        else:
            try: L = int(self.text)
            except: L = 0
        STATS[self.index] = L
        print(STATS)

    def update(self):
        width = max(self.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def t(self):
        return 1

class toggleBoxClass(InputBox):
    def __init__(self, x, y, w, h, palletIndex):
        super().__init__(x, y, w, h, palletIndex)
        self.text = ''
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.active = not self.active
            STATS[self.index] = self.active
    def update(self): pass
    def draw(self, screen):
        if self.active: 
            pygame.draw.rect(screen, STATS[7], self.rect)
            pygame.draw.rect(screen, [210,250,255], self.rect, 2)
        else: pygame.draw.rect(screen, [30,90,120], self.rect, 2)
    def t(self):
        return 3
class ColorPreview(toggleBoxClass):
    def handle_event(self, event): pass
    def draw(self, screen):
        pygame.draw.rect(screen, STATS[self.index], self.rect)
        pygame.draw.rect(screen, [80,80,80], self.rect, 2)

class rollingColor(ColorPreview):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, 0)
        self.color = STATS[6][:]
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.color = STATS[6][:]
    def draw(self, screen):
        var = random.choice(STATS[0])
        self.color[var] = max(min(self.color[var]+random.choice((-4,4)),STATS[1]),STATS[2])
        pygame.draw.rect(screen, self.color, self.rect)
    def t(self): return 2

class randomizeButton(toggleBoxClass):
    def __init__(self, x, y, w, h, palletIndex, ID):
        super().__init__(x, y, w, h, palletIndex)
        self.ID = ID
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            global STATS
            if self.ID == 0:
                STATS = newPallet(6)
            elif self.ID == 1:
                STATS[self.index] = [random.randint(0, 255) for _ in range(3)]
            for i in STATS[0]+STATS[6]+STATS[7]:
                i = int(i)
            for i in boxList:
                if i.t() == 1:
                    i.text = str(STATS[i.index]).replace('[', '').replace(']', '')
                    i.txt_surface = pygame.font.Font(None, 32).render(i.text, True, i.color)
                elif i.t() == 2:
                    i.color = STATS[6][:]
                elif i.t() == 3:
                    i.active = STATS[3]

    def draw(self, screen):
        pygame.draw.rect(screen, [50,180,30], self.rect)
        if self.ID == 0: SCREEN.blit(pygame.font.Font(None, 30).render('Randomize', True, (22,22,22)),(self.x+5,self.y+5))
        elif self.ID == 1: SCREEN.blit(pygame.font.Font(None, 30).render('R', True, (22,22,22)),(self.x+5,self.y+5))
        pygame.draw.rect(screen, [210,250,255], self.rect, 2)

class clearButton(toggleBoxClass):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            for i in boxList:
                if i.t():
                    i.text = ''
                    i.txt_surface = pygame.font.Font(None, 32).render(i.text, True, i.color)
    def draw(self, screen):
        pygame.draw.rect(screen, [230,70,60], self.rect)
        SCREEN.blit(pygame.font.Font(None, 30).render('Clear', True, (22,22,22)),(self.x+5,self.y+5))
        pygame.draw.rect(screen, [210,250,255], self.rect, 2)

class generate(toggleBoxClass):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and threading.active_count() == 1:
            global STATS
            x = threading.Thread(target=makePreview, args=[STATS])
            x.start()
    def draw(self, screen):
        pygame.draw.rect(screen, [110,160,170], self.rect)
        SCREEN.blit(pygame.font.Font(None, 30).render('Generate', True, (22,22,22)),(self.x+5,self.y+5))
        pygame.draw.rect(screen, [210,250,255], self.rect, 2)

class Node:
    def __init__(self,x,y,Delta, color=(0,0,0)):
        self.x = x + random.randint(-Delta, Delta)
        self.y = y + random.randint(-Delta, Delta)
        try: self.color = PREVIEW.get_at((x//2, y//2))
        except: self.color = color
    def draw(self): pygame.draw.circle(SCREEN, (255,255,255), (self.x, self.y), 4)
    def dist(self, p): return ((p[0]-self.x)**2+(p[1]-self.y)**2)**(1/2)

def draw():
    SCREEN.blit(pygame.transform.scale(PREVIEW, (700,675)), (500,0))
    SCREEN.blit(pygame.font.Font(None, 40).render('Color Options', True, (120,220,250)),(50,10))
    SCREEN.blit(pygame.font.Font(None, 40).render('Range', True, (120,220,250)),(50,100))
    SCREEN.blit(pygame.font.Font(None, 30).render('Min:', True, (120,220,250)),(20,160))
    SCREEN.blit(pygame.font.Font(None, 30).render('Max:', True, (120,220,250)),(150,160))
    SCREEN.blit(pygame.font.Font(None, 40).render('Accent', True, (120,220,250)),(50,200))
    SCREEN.blit(pygame.font.Font(None, 30).render('Frequency:', True, (120,220,250)),(20,255))
    SCREEN.blit(pygame.font.Font(None, 30).render('Color:', True, (120,220,250)),(20,295))
    SCREEN.blit(pygame.font.Font(None, 40).render('Change', True, (120,220,250)),(50,350))
    SCREEN.blit(pygame.font.Font(None, 40).render('Base Color', True, (120,220,250)),(50,400))

    pygame.display.update()

InputBox(50, 50, 200, 32, 0)
InputBox(80, 150, 50, 32, 2)
InputBox(210, 150, 50, 32, 1)
toggleBoxClass(160, 205, 18, 18, 3)
InputBox(150, 245, 50, 32, 4)
InputBox(100, 285, 150, 32, 7)
InputBox(180, 350, 50, 32, 5)
InputBox(50, 450, 150, 32, 6)
ColorPreview(230, 400, 60, 30, 6)
randomizeButton(30, 600, 120, 32, 0, 0)
clearButton(300, 600, 80, 32, 0)
rollingColor(280, 80, 100, 50)
generate(300, 30, 120, 30, 0)
randomizeButton(270, 287, 28, 28, 7, 1)
randomizeButton(230, 450, 28, 28, 6, 1)

running = True
while running:
    SCREEN.fill((10,13,18))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # print(STATS)
        for box in boxList:
            box.handle_event(event)
    for box in boxList:
        box.update()
        box.draw(SCREEN)
    draw()