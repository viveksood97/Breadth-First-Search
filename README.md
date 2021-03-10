# ENPM661 - Project2

#### Project 2 for ENPM661: Planning for Autonomous Robots by Vivek Sood(UID:117504279)
### Description

##### 1. This python script is used to find path between start point and goal point while avoiding defined obstacles.
##### 2. The two algorithms that I have implemented are standard BFS and an optimized BFS that uses a priority queue.

### Packages Used
```python
import pygame
import time
import math
from matplotlib import pyplot as plt
```
##### Note: Apart from pygame everything else is an inbuilt package
### Usage
##### To run the program
```bash
python3 version.py
```
##### This will generate a prompt.

```bash
pygame 2.0.1 (SDL 2.0.14, Python 3.6.10)
Hello from the pygame community. https://www.pygame.org/contribute.html
 
   ____        __  __       ____  __                           
   / __ \____ _/ /_/ /_     / __ \/ /___ _____  ____  ___  _____
  / /_/ / __ `/ __/ __ \   / /_/ / / __ `/ __ \/ __ \/ _ \/ ___/
 / ____/ /_/ / /_/ / / /  / ____/ / /_/ / / / / / / /  __/ /    
/_/    \__,_/\__/_/ /_/  /_/   /_/\__,_/_/ /_/_/ /_/\___/_/     
                                                                


Enter the x coordinate of the start point: 0
Enter the y coordinate of the start point: 0
Enter the x coordinate of the goal point: 216
Enter the y coordinate of the goal point: 216

```
##### Enter start and goal positions. After entering the positions line by line another prompt will be generated asking you to specify the desired algorithm.

```bash
Choose the algorithm that you desire to use 
 1. Enter 1 for Standard BFS
 2. Enter 2 for Optimized BFS

Answer: 1
```
##### Enter your choice and the code will find a path and start the animation depicting the path.