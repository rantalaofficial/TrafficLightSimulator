# make a pygui window
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import math

from Car import Car
from Intersection import Intersection

SCREEN_SIZE = 1000

ROAD_WIDTH = 200

intersection = Intersection(SCREEN_SIZE, ROAD_WIDTH)

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        self.timer = QTimer()
        self.timer.setInterval(int(1000 / 60))  # 60 fps
        self.timer.timeout.connect(self.updateCanvas)
        self.timer.start()

        self.UI()
        
    def UI(self):
        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.move(15, 15)

        self.label = QLabel("Spawn rate: " + str(self.slider.value()), self)
        self.label.move(35, 40)
        self.label.resize(200, 50)

        self.toggleButton = QPushButton("Reset", self)
        self.toggleButton.setCheckable(True)
        self.toggleButton.move(20, 100)
        self.toggleButton.resize(200, 50)
        self.toggleButton.clicked.connect(self.resetClicked)

        # button for automatic / manual mode
        self.toggleButton = QPushButton("Automatic control: ON", self)
        self.toggleButton.setCheckable(True)
        self.toggleButton.move(20, 160)
        self.toggleButton.resize(200, 50)
        self.toggleButton.clicked.connect(self.toggleButtonClicked)

        self.slider.valueChanged.connect(self.updateSliders)

        self.setWindowTitle("Robot")
        self.setGeometry(100, 100, 800, 800)
        self.show()

    def resetClicked(self):
        intersection.cars = []

    def updateSliders(self):
        sliderValue = self.slider.value()
        self.label.setText("Spawn rate: " + str(sliderValue))

    def toggleButtonClicked(self):
        intersection.automaticControl = not intersection.automaticControl

        if intersection.automaticControl:
            self.toggleButton.setText("Automatic control: ON")
        else:
            self.toggleButton.setText("Automatic control: OFF")
            for light in intersection.trafficLightState:
                intersection.trafficLightState[light] = intersection.RED

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        painter.drawRect(0, 0, SCREEN_SIZE, SCREEN_SIZE)

        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawRect(SCREEN_SIZE / 2 - ROAD_WIDTH / 2, 0, ROAD_WIDTH, SCREEN_SIZE)

        painter.drawRect(0, SCREEN_SIZE / 2 - ROAD_WIDTH / 2, SCREEN_SIZE, ROAD_WIDTH)
        
        

        for light in intersection.trafficLightPosition:
            painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
            painter.drawRect(intersection.trafficLightPosition[light][0] - 15, intersection.trafficLightPosition[light][1] - 15, 30, 30)

            if intersection.trafficLightState[light] == intersection.RED:
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
            elif intersection.trafficLightState[light] == intersection.GREEN:
                painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))

            painter.drawEllipse(intersection.trafficLightPosition[light][0] - 10, intersection.trafficLightPosition[light][1] - 10, 20, 20)
        
        # check if mouse clicked traffic light
        

        # points = intersection.incoming["left"] + intersection.incoming["top"] + intersection.incoming["right"] + intersection.incoming["bottom"]
        # flip = False
        # for point in points:
        #     if flip:
        #         painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        #         flip = False
        #     else:
        #         painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        #         flip = True
        #     painter.drawEllipse(point[0], point[1], 10, 10)

        if random.randint(0, 100) < self.slider.value() / 20:
            intersection.addRandomCar()

        intersection.update()

        for car in intersection.cars:

            location = car.getLocation()
            direction = car.getDirection()

            painter.translate(location[0], location[1])
            painter.rotate(direction + 90)
            painter.translate(-car.width / 2, -car.length / 2)

            painter.setBrush(QBrush(QColor(car.color[0], car.color[1], car.color[2]), Qt.SolidPattern))
            painter.drawRect(0, 0, car.width, car.length)

            painter.resetTransform()
        
    def mousePressEvent(self, event):
        mousePosition = [event.x(), event.y()]
        for light in intersection.trafficLightPosition:
            if math.sqrt((mousePosition[0] - intersection.trafficLightPosition[light][0])**2 + (mousePosition[1] - intersection.trafficLightPosition[light][1])**2) < 15:
                intersection.trafficLightState[light] = not intersection.trafficLightState[light]


    def mouseMoveEvent(self, event):
        self.targetCoords = [event.x(), event.y()]

    def updateCanvas(self):
        self.update()
        


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.canvas = Canvas()

        self.setCentralWidget(self.canvas)

        self.setGeometry(100, 100, SCREEN_SIZE, SCREEN_SIZE)
        self.setWindowTitle('Traffic light Simulator')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


