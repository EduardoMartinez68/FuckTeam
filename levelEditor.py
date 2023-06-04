import pygame, sys
pygame.init()
size=1000,600
sizeCube=25
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Fuck You level editor")

mode=0
level=[] #mode 0
floor=[] #mode 1
floorCoordinates=[]
height=[] #mode 2
heightCoordinates=[]
objects=[] #mode 3
objectsCoordinates=[]
ceiling=[] #mode 4
ceilingCoordinates=[]


baldosaX=0
baldosaY=0
mouseX,mouseY=0,0
alarm=[30]
click=True
def drawLine(x,y,x2,y2):
    index=12
    pygame.draw.line(screen,(index,index,index),[x,y],[x2,y2],1)

def updateScreen():
    screen.fill((0,0,0)) #background
    for y in range(int(size[1]/sizeCube)):
        y=y*sizeCube
        drawLine(0,y,size[0],y)

    for x in range(int(size[0]/sizeCube)):
        x=x*sizeCube
        drawLine(x,0,x,size[1]) 

font = pygame.font.Font(None, 25)
def drawText(message,x,y):
    global font 
    text = font.render(message, True, (255,255,255))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

#-------------------------------------------------------------
def theCoordinatesAreRepeated(array,x,y):
    for i in array:
        if x==i[1] and y==[0]:
            return True 
    return False 

def changeBlock(array,limit,arrayCoordinates):
    global click
    if click: #know if the player do click
        click=False
        i=array[baldosaY][baldosaX]#save the dato of the array 
        array[baldosaY][baldosaX] = 0 if i>=limit else i+1
        #check that the coordinates are not repeated
        if not theCoordinatesAreRepeated(arrayCoordinates,baldosaX,baldosaY):
            arrayCoordinates.append([baldosaY,baldosaX])

#------------------------------------------------draw the map 
def drawWall(typeBoxel,boxelX,boxelY):
    if typeBoxel==1:
        pygame.draw.rect(screen,(255,255,255),[boxelX,boxelY,sizeCube,sizeCube],1)
    elif typeBoxel==2:
        pygame.draw.line(screen,(255,255,255),[boxelX,boxelY],[boxelX+sizeCube,boxelY+sizeCube],1)
    elif typeBoxel==3:
        pygame.draw.line(screen,(255,255,255),[boxelX+sizeCube,boxelY],[boxelX,boxelY+sizeCube],1)

def drawObject(typeBoxel,boxelX,boxelY):
    if typeBoxel==1:
        pygame.draw.rect(screen,(255,255,255),[boxelX,boxelY,sizeCube,sizeCube],1)
    elif typeBoxel==2:
        pygame.draw.line(screen,(255,255,255),[boxelX+sizeCube,boxelY],[boxelX,boxelY+sizeCube],1)
    elif typeBoxel==3:
        pygame.draw.line(screen,(255,255,255),[boxelX,boxelY],[boxelX+sizeCube,boxelY+sizeCube],1)

def drawHeight(typeBoxel,boxelX,boxelY):
    mitCube=sizeCube/2
    x,y=boxelX+mitCube,boxelY+mitCube
    drawText(str(typeBoxel),x,y)


#-------------------------------------------------
def getValueOfTheArray(arrayCoordinates,function):
    #we will go through all the data that we saved
    for boxel in arrayCoordinates:
        #we will calculate the coordinates that go to draw
        boxelX=boxel[1]*sizeCube
        boxelY=boxel[0]*sizeCube
        typeBoxel=level[boxel[0]][boxel[1]] #we get the value of the type boxel that we will draw

        if function==0:
            drawWall(typeBoxel,boxelX,boxelY) 
        elif function==1:
            pass
        elif function==2:
            drawHeight(typeBoxel,boxelX,boxelY)
        elif function==3:
            pass
        elif function==4:
            pass

def updateModeMap():
    updateScreen()
    if mode==0:
        changeBlock(level,3,objectsCoordinates)
        getValueOfTheArray(objectsCoordinates,0)
    elif mode==1:
        pass 
    elif mode==2:
        changeBlock(height,3,heightCoordinates)
        getValueOfTheArray(heightCoordinates,2) 
    elif mode==3:
        pass 
    elif mode==4:
        pass

def changeMode():
    global click,mode
    if click:
        click=False 
        mode=0 if mode>=4 else mode+1
        updateModeMap()
        print(mode)

def createArrayMap():
    for y in range(int(size[1]/sizeCube)): 
        wall=[]
        for x in range(int(size[0]/sizeCube)):
            wall.append(0)
        level.append(wall)
        height.append(wall)
        floor.append(wall)
        objects.append(wall)
        ceiling.append(wall)

def saveMap(nameMap):
    #delete the data that we haved in the txt 
    f = open(f'levels/{nameMap}/floor.txt', "w")
    h = open(f'levels/{nameMap}/height.txt', "w")
    o = open(f'levels/{nameMap}/objects.txt', "w")
    c = open(f'levels/{nameMap}/ceiling.txt', "w")
    f.close()
    h.close()
    o.close()
    c.close()
    
    #save the new information of the level
    f = open(f'levels/{nameMap}/floor.txt', "a")
    h = open(f'levels/{nameMap}/height.txt', "a")
    o = open(f'levels/{nameMap}/objects.txt', "a")
    c = open(f'levels/{nameMap}/ceiling.txt', "a")
    sizeX=len(level[0])
    for y in range(len(level)):
        for x in range(sizeX):  
            if x!=sizeX-1:
                f.write(str(level[y][x])+',')
                h.write(str(height[y][x])+',')
                o.write(str(objects[y][x])+',')
                c.write(str(ceiling[y][x])+',')
            else:
                f.write(str(level[y][x]))
                h.write(str(height[y][x]))
                o.write(str(objects[y][x]))
                c.write(str(ceiling[y][x]))   

        f.write('\n')
        h.write('\n')
        o.write('\n')
        c.write('\n')
    f.close()
    h.close()
    o.close()
    c.close()


createArrayMap() 
updateScreen()
while True:
    if not click:
        if  alarm[0]>0:
            alarm[0]-=1
        else:
            click=True 
            alarm[0]=60
    
    for event in pygame.event.get():
        mouseX,mouseY=pygame.mouse.get_pos()
        if event.type==pygame.QUIT:
            pygame.quit()
        if event.type==pygame.KEYDOWN:
            if event.key==27:
                pygame.quit()
            if event.key==103:
                saveMap('demo')
            if event.key==101:
                changeMode()
            if event.key==45:
                sizeCube-=25
            elif event.key==61:
                sizeCube+=25
            
            sizeCube=25 if sizeCube<=0 else sizeCube

        if pygame.mouse.get_pressed()[0]:
            baldosaX,baldosaY=int(mouseX/sizeCube),int(mouseY/sizeCube)
            updateModeMap()

        #if event.type==pygame.MOUSEBUTTONDOWN:
            #baldosaX,baldosaY=int(mouseX/sizeCube),int(mouseY/sizeCube)
    pygame.display.flip() 

