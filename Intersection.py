from Car import Car
import math
import random

class Intersection:

    # light states
    RED = 0
    GREEN = 1

    t = 0
    automaticControl = True

    def __init__(self, mapSize, roadWidth):
        self.mapSize = mapSize
        self.roadWidth = roadWidth

        self.cars = []

        halfMap = mapSize / 2
        laneDistanceFromBorder = roadWidth / 4
        distanceToIntersection = roadWidth * 0.75
        startPosition = -roadWidth / 2
        lightDistanceFromBorder = roadWidth / 2.5

        self.incoming = {}

        self.incoming["left"] = [(startPosition, halfMap + laneDistanceFromBorder), (halfMap - distanceToIntersection, halfMap + laneDistanceFromBorder)]
        self.incoming["top"] = [(halfMap - laneDistanceFromBorder, startPosition), (halfMap - laneDistanceFromBorder, halfMap - distanceToIntersection)]
        self.incoming["right"] = [(mapSize - startPosition, halfMap - laneDistanceFromBorder), (halfMap + distanceToIntersection, halfMap - laneDistanceFromBorder)]
        self.incoming["bottom"] = [(halfMap + laneDistanceFromBorder, mapSize - startPosition), (halfMap + laneDistanceFromBorder, halfMap + distanceToIntersection)]

        self.outgoing = {}

        self.outgoing["left"] = [(halfMap - distanceToIntersection, halfMap - laneDistanceFromBorder), (startPosition, halfMap - laneDistanceFromBorder)]
        self.outgoing["top"] = [(halfMap + laneDistanceFromBorder, halfMap - distanceToIntersection), (halfMap + laneDistanceFromBorder, startPosition)]
        self.outgoing["right"] = [(halfMap + distanceToIntersection, halfMap + laneDistanceFromBorder), (mapSize - startPosition, halfMap + laneDistanceFromBorder)]
        self.outgoing["bottom"] = [(halfMap - laneDistanceFromBorder, halfMap + distanceToIntersection), (halfMap - laneDistanceFromBorder, mapSize - startPosition)]

        self.stopPosition = {}

        self.stopPosition["left"] = self.incoming["left"][1]
        self.stopPosition["top"] = self.incoming["top"][1]
        self.stopPosition["right"] = self.incoming["right"][1]
        self.stopPosition["bottom"] = self.incoming["bottom"][1]

        self.trafficLightState = {}
        self.trafficLightState["left"] = self.RED
        self.trafficLightState["top"] = self.RED
        self.trafficLightState["right"] = self.RED
        self.trafficLightState["bottom"] = self.RED

        self.currentTrafficLight = -1
        self.trafficLightRotation = ["left", "top", "right", "bottom"]

        self.trafficLightPosition = {}
        self.trafficLightPosition["left"] = [self.stopPosition["left"][0], self.stopPosition["left"][1] + lightDistanceFromBorder]
        self.trafficLightPosition["top"] = [self.stopPosition["top"][0] - lightDistanceFromBorder, self.stopPosition["top"][1]]
        self.trafficLightPosition["right"] = [self.stopPosition["right"][0], self.stopPosition["right"][1] - lightDistanceFromBorder]
        self.trafficLightPosition["bottom"] = [self.stopPosition["bottom"][0] + lightDistanceFromBorder, self.stopPosition["bottom"][1]]

    def addRandomCar(self):
        randomIncoming = random.choice(list(self.incoming.keys()))

        remainingDirections = list(self.incoming.keys())
        remainingDirections.remove(randomIncoming)

        randomOutgoing = random.choice(remainingDirections)

        speed = 0.75 #random.randint(5, 10) / 10
        pathCurrentCompletion = 0 

        car = Car(self.incoming[randomIncoming] + self.outgoing[randomOutgoing], pathCurrentCompletion, speed, [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], 100)

        if self.carNearby(car, car.getLocation(), car.length * 1.5):
            return False

        self.cars.append(car)
        return True
    
    def carAtTrafficLight(self, car):
        carLocation = car.getLocation()

        for light in self.trafficLightPosition.keys():
            
            stopPosition = self.stopPosition[light]

            distance = math.sqrt((carLocation[0] - stopPosition[0]) ** 2 + (carLocation[1] - stopPosition[1]) ** 2)

            if self.trafficLightState[light] == self.RED and distance < car.length / 4:
                return True
            
        return False

    def carNearby(self, thisCar, location, radius):
        for car in self.cars:
            if car == thisCar:
                continue

            carLocation = car.getLocation()
            distance = math.sqrt((location[0] - carLocation[0]) ** 2 + (location[1] - carLocation[1]) ** 2)

            if distance < radius:
                return True

        return False

    def moveCars(self):
        for car in self.cars:

            carLocation = car.getLocation()
            carDirection = car.getDirection()

            carBumber = [carLocation[0] + math.cos(math.radians(carDirection)) * car.length / 2, carLocation[1] + math.sin(math.radians(carDirection)) * car.length / 2]

            if self.carNearby(car, carBumber, car.length / 1.8):
                continue

            if self.carAtTrafficLight(car):
                continue

            if car.move() == False:
                self.cars.remove(car)

    def updateTrafficLights(self):
        if self.t % 500 == 0:
            self.currentTrafficLight += 1
            self.currentTrafficLight %= 4

        for light in self.trafficLightState.keys():
            self.trafficLightState[light] = self.RED

        self.trafficLightState[self.trafficLightRotation[self.currentTrafficLight]] = self.GREEN


    def update(self):
        self.moveCars()

        if self.automaticControl:
            self.updateTrafficLights()

        self.t += 1

    
    