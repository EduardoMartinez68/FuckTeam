#-------------------------------algorithm A*
#from levels import readLevel as rl

#room 
width,height=0,0
playerX,playerY=0,0

star=True 
class Neighbors():
    f=0 #total cost
    g=0 #steps taken
    g=0 #heuristics

    neighbors=[]
    def __init__(self,room,x,y,father):
        self.room=room
        self.x=x
        self.y=y
        self.father=father 

    def calculateNeighbors(self):
        global star
        x,y=self.x,self.y
        #see if collision with the goal 
        if x==playerX and y==playerY:
            star=False

            #create an array with the coordinate of all the soon
            granFather=self.father
            self.neighbors.append([x,y])
            if not granFather==None:
                while not granFather.father==None:
                    self.neighbors.append([granFather.father.x,granFather.father.y])
                    granFather=granFather.father
            print(self.neighbors)

        #if no one has collided keep looking
        if star:
            if x>0:
                if room[y][x-1]==0: #0=floor
                    Neighbors(self.room,x-1,y,self).calculateNeighbors()
            if x<width-1:
                if room[y][x+1]==0: #0=floor
                    Neighbors(self.room,x+1,y,self).calculateNeighbors()
            if y>0:
                if room[y-1][x]==0: #0=floor
                    Neighbors(self.room,x,y-1,self).calculateNeighbors()
            if y<height-1:
                if room[y+1][x]==0: #0=floor
                    Neighbors(self.room,x,y-1,self).calculateNeighbors()




def startA(room,x,y):
    f=0 #total cost
    g=0 #steps taken
    g=0 #heuristics

    neighbors=[]
    father=None

    #calculate neighbors
    if x>0:
        if room[y][x-1]==0: #0=floor
            neighbors.append([y,x-1]) 
    if x<width-1:
        if room[y][x+1]==0: #0=floor
            neighbors.append([y,x+1]) 

    if y>0:
        if room[y-1][x]==0: #0=floor
            neighbors.append([y-1,x]) 
    if y<height-1:
        if room[y+1][x]==0: #0=floor
            neighbors.append([y+1,x]) 

    print(neighbors)



#-------------
def getDataRoom(room):
    global width, height
    width=len(room[0])
    height=len(room)

def readMap(level,x,y):
    global  playerX, playerY
    playerX,playerY=x,y

    #read the map
    #pathLevel='levels/'+level
    #floor=rl.scanMap(pathLevel+'/floor.txt')
    #getDataRoom(floor)

room=[
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
[0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
]
'''
room=[
[X,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,Y]
]'''

readMap('',23,2)
getDataRoom(room)

Neighbors(room,0,0,None).calculateNeighbors()

for y in room:
    print(y)

 