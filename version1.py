import pygame
import time
import math
from matplotlib import pyplot as plt



def obstacleOrNot(point):
    """
        Check whether the point is inside or outside the
        defined obstacles.

        Note: The obstacles have been defined using half 
        plane method


        Input: point/testCase(tuple)

        Return: Boolean(True or False)

    """
    x = point[0]
    y = point[1]
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
    """
        Class to duplicate functionality of queue data-
        structure

        Maintains a list of nodes

    """
    def __init__(self, node):
        """
        Initialize a Queue object corresponding to a
        test-case.

        Input: point/testCase(tuple)

        Return: None

        """
        self.queue = [node]

    def insert(self, node):
        """
        Insert a point in back of the queue.

        Input: self,testCase/point

        Returns: None

        """
        self.queue.append(node)

    def extract(self):
        """
        Pop a point from the queue.

        Input: None

        Returns: point(tuple)

        """
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

        Input: point(tuple)

        Return:

        """
        self.queue = [node]
        self.priorityList = [1]
        self.goalPoint = goalPoint

    def priority(self, node):
        """
        Generate a priority number for each node by the distance of point
        from the goalpoint

        Input: self,point(tuple)

        Returns: Priority of the point(float)

        """
        
        priority = -1*math.sqrt((node[0]-self.goalPoint[0])**2 + (node[1]-self.goalPoint[1])**2)
        return priority

    def insert(self, node):
        """
        Insert an element in the queue and also store its
        priority generated using the priority.

        Input: self,point

        Returns: None

        """
        priority = self.priority(node)
        self.queue.append(node)
        self.priorityList.append(priority)

    def extract(self):
        """
        Pop a point which has the max priority
        from the queue.

        Input: None

        Returns: The node with the maximum
        priority(tuple)

        """
        indexOfMaximumPriority = self.priorityList.index(max(self.priorityList))
        self.priorityList.pop(indexOfMaximumPriority)
        return self.queue.pop(indexOfMaximumPriority)




class MovePoint:
    """
    Class that is used to do decide point moving opeartion
    and processing which includes generating possible moves for the
    point.

    """

    def __init__(self, startPoint, goalPoint, size,algo):
        """
        Initialize the MovePoint object corresponding to a
        start point, goal point, size of arena and the algorithm 
        to use.
        

        Input: startPoint(tuple), endPoint(tuple),
        size(tuple), algo(str)

        Return: None

        """
        self.goalPoint = goalPoint
        self.algo = algo
        if(algo == 1):
            self.queue = Queue(startPoint)
        elif(algo == 2):
            self.queue = CustomPriorityQueue(startPoint,goalPoint)
        self.size = size
        self.visited = {}
        self.visited[startPoint] = 0
        
    
    def nodeOperation(self, node, moveCost, *args, **kwargs):
        """
        Generate the next node based on the operation and
        the node

        Input: node/point(tuple), moveCost(float),
        *args(list), **kwargs(dict)

        Return: True/False(Bool)
        """
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
        """
        Process the point moving operation and check if the
        goal node is achived or not.

        Input: self

        Return: True/False(Bool)

        """
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
        """
        Back trace the path from goal point to start point

        Input: self,startPoint(tuple)

        Return: backTraceArr(list)

        """
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
    print("\n")
    print(r"""    ____        __  __       ____  __                           
   / __ \____ _/ /_/ /_     / __ \/ /___ _____  ____  ___  _____
  / /_/ / __ `/ __/ __ \   / /_/ / / __ `/ __ \/ __ \/ _ \/ ___/
 / ____/ /_/ / /_/ / / /  / ____/ / /_/ / / / / / / /  __/ /    
/_/    \__,_/\__/_/ /_/  /_/   /_/\__,_/_/ /_/_/ /_/\___/_/     
                                                                
""")
    
    x1 = int(input("\nEnter the x coordinate of the start point: "))
    y1 = int(input("Enter the y coordinate of the start point: "))

    x2 = int(input("Enter the x coordinate of the goal point: "))
    y2 = int(input("Enter the y coordinate of the goal point: "))
    print("\n")
    
    start = time.time()
    startPoint = (x1,y1)
    endPoint = (x2,y2)
    arenaSize = (400,300)

    if((not obstacleOrNot(startPoint)) or (startPoint[0] > arenaSize[0]) or (startPoint[1] > arenaSize[1])):
        outStr = "Error: Start Point either on/inside obstacle or outside specified arena"
        print("#"*len(outStr))
        print("\n"+outStr+"\n")
        print("#"*len(outStr))
        print("\n")
        return False
    if((not obstacleOrNot(endPoint)) or (endPoint[0] > arenaSize[0]) or (endPoint[1] > arenaSize[1])):
        outStr = "Error: Goal either on/inside obstacle or outside specified arena"
        print("#"*len(outStr))
        print("\n"+outStr+"\n")
        print("#"*len(outStr))
        print("\n")
        return False

    algo = int(input("Choose the algorithm that you desire to use \n 1. Enter 1 for Standard BFS\n 2. Enter 2 for Optimized BFS\n\nAnswer: "))
    if(algo!= 1 and algo!= 2):
        print("Error!!: Choose between option 1 or 2")
        return False

    move = MovePoint(startPoint,endPoint,arenaSize,algo)  
    flag = False
    while(not flag):
        flag = move.pointProcessor()
    
    end = time.time()
    finalOut = f"\nPath found in {round(end - start, 4)} seconds.\n"
    print(finalOut)
    
    backTraceArr = move.backTrace(startPoint)
    
    pygame.init()

    pygame.display.set_caption("Path Planner")

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
            clock.tick(10000000)
            pygame.display.update()

        for point in backTraceArr:
            pygame.draw.circle(gameDisplay, green, to_pygame(point),1)
            clock.tick(150)
            pygame.display.update()

        
        
        
        time.sleep(3)
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



        





