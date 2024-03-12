from scipy.interpolate import CubicSpline
import numpy as np
import math

class Car:
    def __init__(self, path, pathCurrentCompletion, speed, color, length):
        numOfPoints = 300
    
        pathPoints = np.array(path)
        t = np.arange(len(pathPoints))
        spline = CubicSpline(t, pathPoints, bc_type='natural')
        
        t_smooth = np.linspace(0, len(pathPoints) - 1, numOfPoints)
        self.path = spline(t_smooth)

        derivative = spline.derivative()(t_smooth)
        #self.direction = derivative(t_smooth)

        self.direction = []
        for i in range(len(derivative)):
            angle = math.atan2(derivative[i][1], derivative[i][0]) * 180 / math.pi
            self.direction.append(angle)

        self.pathIndex = int(pathCurrentCompletion * numOfPoints)
        self.speed = speed
        self.color = color
        self.length = length
        self.width = length / 2


    def move(self):
        self.pathIndex += self.speed

        if self.pathIndex >= len(self.path):
            return False
        
        return True
    
    def getLocation(self):
        return self.path[int(self.pathIndex)]
    
    def getDirection(self):
        return self.direction[int(self.pathIndex)]
    

    



    