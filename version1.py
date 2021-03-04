import pygame
import numpy as np
import time
import copy
import math
import argparse
from matplotlib import pyplot as plt


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
    

class PriorityQueue:
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
        arrangement i.e., checking how many elements are inplace
        when compared to the goal state.

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

    def __init__(self, startPoint, goalPoint, size, visited):
        self.goalPoint = goalPoint
        self.queue = [startPoint]
        #self.queue = PriorityQueue(startPoint,goalPoint)
        self.size = size
        self.visited = visited
        self.visited[startPoint] = 0

    def pointProcessor(self):
        queue = self.queue
        size = self.size
        goalPoint = self.goalPoint
        visited = self.visited
        #popping an element from the queue
        #node = queue.extract()
        node = queue.pop(0)
        # print(node)
        if(obstacleOrNot(node) and node[0] > 0):
            left = (node[0]-1,node[1])
            if(goalPoint == left):
                return True

            if(left not in visited):
                visited[left] = 0
                #queue.insert(left)
                queue.append(left)

        if(obstacleOrNot(node) and node[0]!=size[0]-1):
            right = (node[0]+1,node[1])
            if(goalPoint == right):
                return True
            
            if(right not in visited):
                visited[right] = 0
                #queue.insert(right)
                queue.append(right)

        if(obstacleOrNot(node) and node[1] != 0):
            down = (node[0],node[1]-1)
            if(goalPoint == down):
                return True
            
            if(down not in visited):
                visited[down] = 0
                #queue.insert(down)
                queue.append(down)

        if(obstacleOrNot(node) and node[1]!=size[1]-1):
            up = (node[0],node[1]+1)
            if(goalPoint == up):
                return True
            
            if(up not in visited):
                visited[up] = 0
                #queue.insert(up)
                queue.append(up)

        if(obstacleOrNot(node) and node[0] != 0 and node[1] != 0):
            bottomLeft = (node[0]-1,node[1]-1)
            if(goalPoint == bottomLeft):
                return True

            if(bottomLeft not in visited):
                
                visited[bottomLeft] = 0
                #queue.insert(bottomLeft)
                queue.append(bottomLeft)

        if(obstacleOrNot(node) and node[0] != 0 and node[1] != size[1]-1):
            topLeft = (node[0]-1,node[1]+1)
            if(goalPoint == topLeft):
                return True

            if(topLeft not in visited):
                visited[topLeft] = 0
                #queue.insert(topLeft)
                queue.append(topLeft)

        if(obstacleOrNot(node) and node[0] != size[0]-1 and node[1] != 0):
            bottomRight = (node[0]+1,node[1]-1)
            if(goalPoint == bottomRight):
                return True

            if(bottomRight not in visited):
                
                visited[bottomRight] = 0
                #queue.insert(bottomRight)
                queue.append(bottomRight)

        if(obstacleOrNot(node) and node[0] != size[0]-1 and node[1] != size[1]-1):
            topRight = (node[0]+1,node[1]+1)
            if(goalPoint == topRight):
                return True

            if(topRight not in visited):
                
                visited[topRight] = 0
                #queue.insert(topRight)
                queue.append(topRight)

        

        return False  

def main():

    move = MovePoint((0,0),(314,142),(400,300),{})  
    flag = False
    count = 0
    while(not flag):
        count += 1
        flag = move.pointProcessor()

    xPoint = []
    yPoint = []
    for x in range(0,400):
        for y in range(0,300):
            if not(obstacleOrNot((x,y))):
                xPoint.append(x)
                yPoint.append(y)

    print(count)
    plt.scatter(xPoint,yPoint,s=0.1)
    plt.scatter(*zip(*move.visited.keys()),s=0.2)
    plt.show()
    

if __name__ == '__main__':
    main()



        








# print(xPoint)
# print(yPoint)
# 




# def to_pygame(coords):
#     """Convert coordinates into pygame coordinates (lower-left => top left)."""
#     return (coords[0], 300 - coords[1])

# pygame.init()

# white = (255,255,255)
# black = (0,0,0)

# red = (255,0,0)
# green = (0,255,0)
# blue = (0,0,255)

# gameDisplay = pygame.display.set_mode((400,300))
# gameDisplay.fill(white)
# rect = [(48,108),(170.87,194.04),(159.40,210.42),(36.53,124.383)]
# newCoords = [to_pygame(x) for x in rect]
# pygame.draw.polygon(gameDisplay, red, newCoords)

# pygame.draw.circle(gameDisplay, red, to_pygame((90,70)),35)
# ellipseCenter = to_pygame((186,175))
# ellipse = (ellipseCenter[0],ellipseCenter[1],120,60)
# pygame.draw.ellipse(gameDisplay, red, ellipse)

# polygon = [(200,230),(230,230),(230,240),(210,240),(210,270),(230,270),(230,280),(200,280)]
# newPolygon = [to_pygame(x) for x in polygon]
# pygame.draw.polygon(gameDisplay, red, newPolygon)

# polygon1 = [(328,63),(381.03,116.03),(381.03,171.03),(354,138),(327.17,145.03),(285.57,105.43)]
# newPolygon1 = [to_pygame(x) for x in polygon1]
# pygame.draw.polygon(gameDisplay, red, newPolygon1)




# while True:
#     pygame.event.get()
    
#     for i in range(0,400):
#         for j in range(0,300):
#             if(gameDisplay.get_at((i,j)) != (255,255,255,255)):
#                 print(gameDisplay.get_at((i,j)))

#             # pygame.time.delay(50)
#             # pygame.draw.rect(gameDisplay, green, (i,50,10,20))
#             # pygame.display.update()

#     pygame.quit()
#     quit()
    
