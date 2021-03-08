import pygame
import numpy as np
import time
import copy
import math
import argparse
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


def obstacleOrNot(node):
    x = node[0]
    y = node[1]
    #circle
    if((x-90)**2 + (y-70)**2 - 35**2 < 0): #circle
        return False
    
    # tilted Rectangle
    elif((8604*x - 12287*y + 914004 < 0) and (81900*x +59350*y-25510527 < 0) and (86036*x - 122870*y + 12140167 > 0) and (8192*x + 5735*y - 1012596 > 0)):
        return False
    
    # C shaped Polygon
    elif((x >= 200 and x <= 210 and y <= 280 and y >=230 ) or (x>= 210 and x <= 230 and y >=270 and y <= 280) or (y >= 230 and y <= 240 and x >= 210 and x <= 230)):
        return False
    
    # ellipse
    elif((((x-246)/60))**2 + (((y-145)/30))**2 - 1 < 0):
        return False
    
    # crooked polygon
    elif(((x-y-265<=0) and (x+y-391>=0) and (5*x+5*y-2351<=0) and (50*x-50*y-9007>=0)) or ((5*x+5*y-2351>=0) and (703*x+2883*y-646716<0) and (x+y-492<=0) and (x-y-265<=0)) or ((x+y-492>=0) and (x-y-265<=0) and (x<=381.03) and (1101*x-901*y-265416>0))):#                   (x<381.03) and (1101*x-901*y-265416>0) and (703*x+2883*y-646716<0) and (50*x-50*y-9007>0) and ):
        return False

    else:
        return True

class Queue:
    def __init__(self, node):
        self.queue = [node]

    def insert(self, node):
        self.queue.append(node)

    def extract(self):
        return self.queue.pop(0)

class CustomPriorityQueue:
    """
    Class created to implement priority queue

    Maintains a list of nodes with another list
    maintaining the priority of each node.

    """

    def __init__(self, node, goalPoint):
        """
        Initialize a PriorityQueue object corresponding to a
        test-case.

        Note the initial queue has the test-case provided
        and the priorityList is given a priority of 1(any
        value works) for the testcase provided.

        Input: node/testCase(np.array)

        Return:

        """
        self.queue = [node]
        self.priorityList = [1]
        self.goalPoint = goalPoint

    def extentOfArrangement(self, node):
        """
        Generate a priority number for each node by the extent of
        arrangement i.e., checking the distance from current node
        to the goal node.

        Input: self,testCase/node

        Returns: Priority of the input node

        """
        
        priority = -1*math.sqrt((node[0]-self.goalPoint[0])**2 + (node[1]-self.goalPoint[1])**2)
        return priority

    def insert(self, node):
        """
        Insert an element in the queue and also store its
        priority generated using the extentOfArrangement.

        Input: self,testCase/node

        Returns:

        """
        priority = self.extentOfArrangement(node)
        self.queue.append(node)
        self.priorityList.append(priority)

    def extract(self):
        """
        Pop a testCase/node which has the max priority
        from the queue.

        Input:

        Returns: The node with the maximum
        priority(np.array)

        """
        indexOfMaximumPriority = self.priorityList.index(max(self.priorityList))
        self.priorityList.pop(indexOfMaximumPriority)
        return self.queue.pop(indexOfMaximumPriority)




class MovePoint:

    def __init__(self, startPoint, goalPoint, size,algo):
        self.goalPoint = goalPoint
        self.algo = algo
        if(algo == "q"):
            self.queue = Queue(startPoint)
        elif(algo == "pq"):
            self.queue = CustomPriorityQueue(startPoint,goalPoint)
        self.size = size
        self.visited = {}
        self.visited[startPoint] = 0
        
    
    def nodeOperation(self, node, moveCost, *args, **kwargs):
        newNode = False
        obj = list(kwargs.keys())
        if(len(obj) == 1):
            if(obj[0] == "x"):
                if(obstacleOrNot(node) and node[0] != kwargs["x"]):
                    newNode = (node[0]+args[0],node[1]+args[1])
            else:
                if(obstacleOrNot(node) and node[1] != kwargs["y"]):
                    newNode = (node[0]+args[0],node[1]+args[1])
        else:
            if(obstacleOrNot(node) and node[0] != kwargs["x"] and node[1] != kwargs["y"]):
                newNode = (node[0]+args[0],node[1]+args[1])


        if(newNode and self.goalPoint == newNode):
                self.visited[newNode] = node
                return True
        if(newNode and newNode not in self.visited):
            self.visited[newNode] = node
            self.queue.insert(newNode)
        return False


       

    def pointProcessor(self):
        queue = self.queue

        size = self.size
        goalPoint = self.goalPoint
        visited = self.visited
        #popping an element from the queue
        node= queue.extract()
        
        #left
        if(self.nodeOperation(node,1,-1,0,x=0)):
            return True
        
        #right
        if(self.nodeOperation(node,1,1,0,x=size[0])):
            return True

        #down
        if(self.nodeOperation(node,1,0,-1,y=0)):
            return True

        #top
        if(self.nodeOperation(node,1,0,1,y=size[1])):
            return True

        #bottomLeft
        if(self.nodeOperation(node,math.sqrt(2),-1,-1,x=0,y=0)):
            return True

        
        #topLeft
        if(self.nodeOperation(node,math.sqrt(2),-1,1,x=0,y=size[1])):
            return True
        

        #bottomRight
        if(self.nodeOperation(node,math.sqrt(2),1,-1,x=size[0],y=0)):
            return True

        #topRight
        if(self.nodeOperation(node,math.sqrt(2),1,1,x=size[0],y=size[1])):
            return True

        return False

    def backTrace(self,startPoint):
        goalPoint = self.goalPoint

        visited = self.visited
        backTraceArr = []
        
        node = goalPoint
        while(node != startPoint):
            node = visited[node]
            backTraceArr.append(node)
        return backTraceArr



def to_pygame(coords):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    return (coords[0], 300 - coords[1])

def main():
    start = time.time()
    startPoint = (0,0)
    endPoint = (212,266)
    arenaSize = (400,300)

    if((not obstacleOrNot(startPoint)) or (startPoint[0] > arenaSize[0]) or (startPoint[1] > arenaSize[0])):
        outStr = "Error: Start Point either on/inside obstacle or outside specified arena"
        print("#"*len(outStr))
        print("\n"+outStr+"\n")
        print("#"*len(outStr))
        return False
    if((not obstacleOrNot(endPoint)) or (endPoint[0] > arenaSize[0]) or (endPoint[1] > arenaSize[0])):
        outStr = "Error: Goal either on/inside obstacle or outside specified arena"
        print("#"*len(outStr))
        print("\n"+outStr+"\n")
        print("#"*len(outStr))
        return False

    algo = "q"
    move = MovePoint(startPoint,endPoint,arenaSize,algo)  
    flag = False
    count = 0
    while(not flag):
        count += 1
        flag = move.pointProcessor()
    
    end = time.time()
    print(end-start)
    print(count)
    
    backTraceArr = move.backTrace(startPoint)
    
    pygame.init()

    white = (255,255,255)
    black = (0,0,0)
    
    yellow = (255,255,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255,10)


    gameDisplay = pygame.display.set_mode((400,300))
    gameDisplay.fill(white)
    rect = [(48,108),(170.87,194.04),(159.40,210.42),(36.53,124.383)]
    newCoords = [to_pygame(x) for x in rect]
    pygame.draw.polygon(gameDisplay, red, newCoords)

    pygame.draw.circle(gameDisplay, red, to_pygame((90,70)),35)
    ellipseCenter = to_pygame((186,175))
    ellipse = (ellipseCenter[0],ellipseCenter[1],120,60)
    pygame.draw.ellipse(gameDisplay, red, ellipse)

    polygon = [(200,230),(230,230),(230,240),(210,240),(210,270),(230,270),(230,280),(200,280)]
    newPolygon = [to_pygame(x) for x in polygon]
    pygame.draw.polygon(gameDisplay, red, newPolygon)

    polygon1 = [(328,63),(381.03,116.03),(381.03,171.03),(354,138),(327.17,145.03),(285.57,105.43)]
    newPolygon1 = [to_pygame(x) for x in polygon1]
    pygame.draw.polygon(gameDisplay, red, newPolygon1)


    clock = pygame.time.Clock()
    
    while True:
        pygame.event.get()

        
        pygame.draw.circle(gameDisplay, black, to_pygame(endPoint),2)
        for key in move.visited.keys():
            pygame.draw.circle(gameDisplay, blue, to_pygame(key),1)
            clock.tick(1000000)
            pygame.display.update()

        for point in backTraceArr:
            pygame.draw.circle(gameDisplay, green, to_pygame(point),1)
            clock.tick(200)
            pygame.display.update()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        time.sleep(5)
        pygame.quit()
        
        
        # xpts = []
        # ypts = []
        # for x in range(arenaSize[0]):
        #         for y in range(arenaSize[1]):
        #             if not (obstacleOrNot((x,y))):
        #                 xpts.append(x)
        #                 ypts.append(y)
        # plt.scatter(xpts,ypts,s=0.1)
        # plt.show()
        quit()
    
    

   
    
    

if __name__ == '__main__':
    main()



        





