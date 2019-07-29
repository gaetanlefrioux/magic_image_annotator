import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication,QFileDialog, QDialog, QLineEdit, QAction, qApp, QDesktopWidget
from PyQt5.QtWidgets import  QInputDialog, QWidget, QVBoxLayout, QLabel, QMessageBox, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QSize, QRect, QPoint

class ImageWidget(QWidget):

    def __init__(self, background, parent=None):
        super().__init__(parent=parent)
        self.parentWindow = parent
        self.background = background
        self.imageFile = ""
        self.imagePixmap = None
        self.boundRect = None
        self.imageRect = None
        self.pointPen = QPen(Qt.red)
        self.pointPen.setWidth(4)
        self.rectPen = QPen(Qt.blue)
        self.rectPen.setWidth(2)
        self.points = []
        self.rectangles = []
        self.pointCount = 0
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(self.rect(), QBrush(self.background))
        if self.imageFile != "":
            self.imagePixmap = QPixmap(self.imageFile)
            w = self.imagePixmap.width()
            h = self.imagePixmap.height()
            self.boundRect = self.rect()
            y = (self.boundRect.height()-h)/2
            x = (self.boundRect.width()-w)/2
            self.imageRect = QRect(x, y, w, h)
            painter.drawPixmap(self.imageRect, self.imagePixmap)
            painter.setPen(self.pointPen)
            for p in self.points:
                print("drawing point %i %i"%(p[0], p[1]))
                painter.drawEllipse(p[0], p[1], 1, 1)
            painter.setPen(self.rectPen)
            for r in self.rectangles:
                painter.drawRect(r)
        painter.end()

    def setImage(self, imageFile):
        self.imageFile = imageFile
        # Resetting points and rectangles
        self.pointCount = 0
        self.points = []
        self.rectangles = []
        self.update()

    def enablePointsDrawing(self):
        print(self.imageFile)
        if self.imageFile == "":
            QMessageBox.about(self,
                "Enable to draw points",
                "You must import an image to be able to draw points"
            )
        else:
            print("enabeling point drawing")
            self.parentWindow.statusBar().showMessage("Points drawing enable")
            self.mousePressEvent = self.addPoint

    def addPoint(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.imageRect.contains(x, y):
            print("Adding point %i %i"%(x, y))
            self.points += [[x, y]]
            self.pointCount += 1
            if self.pointCount%2==0:
                self.addRect(self.points[-2:])
            self.update()

    def addRect(self, points):
        x = QPoint(points[0][0], points[0][1])
        y = QPoint(points[1][0], points[1][1])
        self.rectangles += [QRect(x, y)]
