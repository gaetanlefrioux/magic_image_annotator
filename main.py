#!/usr/bin/python3

import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication,QFileDialog, QDialog, QLineEdit, QAction, qApp
from PyQt5.QtWidgets import  QInputDialog, QWidget, QVBoxLayout, QLabel, QMessageBox, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUI()
        self.image = ""
        self.imagesDirectory = ""
        self.dataDirectory = ""
        self.dataFile = ""
        self.dataFileObject = None
        self.imageLabel = None
        self.pointCount = 0
        self.fileNameInput = None
        self.createFileDialog = None

    def setUI(self):
        importAction = QAction("Import Image", self)
        importAction.setShortcut("Ctrl+I")
        importAction.setStatusTip("Import an image")
        importAction.triggered.connect(self.importImage)

        conDataFileAction = QAction("Connect data file", self)
        conDataFileAction.setShortcut("Ctrl+D")
        conDataFileAction.setStatusTip("Connect to a data file")
        conDataFileAction.triggered.connect(self.connectToDataFile)

        emptyDataFileAction = QAction("Create empty data file", self)
        emptyDataFileAction.setShortcut("Ctrl+E")
        emptyDataFileAction.setStatusTip("Create an empty data file")
        emptyDataFileAction.triggered.connect(self.createDataFileWin)

        drawPointsAction = QAction(QIcon("./drawPointsIcon.jpeg"), "Draw points", self)
        drawPointsAction.setShortcut("Ctrl+P")
        drawPointsAction.setStatusTip("Draw edges points of object")
        drawPointsAction.triggered.connect(self.enablePointsDrawing)

        menu = self.menuBar()
        imageImport = menu.addMenu("Import image")
        imageImport.addAction(importAction)
        dataFile = menu.addMenu("Data File")
        dataFile.addAction(emptyDataFileAction)
        dataFile.addAction(conDataFileAction)
        drawPoints = menu.addMenu("Drawing")
        drawPoints.addAction(drawPointsAction)

        self.setGeometry(300, 300, 800, 500)
        self.setWindowTitle("Magic Image Annotator")
        self.show()

    def importImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.image, _ = QFileDialog.getOpenFileName(self,"Image selection", self.imagesDirectory,"Images (*.png *.jpeg *.jpg)", options=options)
        if self.image != "":
            self.statusBar().showMessage("Processing image %s"%self.image)
            self.imagesDirectory = "/".join(self.image.split("/")[:-1])
            self.centralWidget = QWidget()
            self.setCentralWidget(self.centralWidget)
            lay = QVBoxLayout(self.centralWidget)
            self.imageLabel = QLabel(self)
            pixmap = QPixmap(self.image)
            self.imageLabel.setPixmap(pixmap)
            self.imageLabel.setAlignment(Qt.AlignCenter)
            if self.width() < pixmap.width() or self.height() < pixmap.height():
                self.resize(pixmap.width(), pixmap.height())
            lay.addWidget(self.imageLabel)

    def createDataFileWin(self):
        dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if dir != "":
            self.dataDirectory = dir
            dialog = QDialog(self)
            dialog.setWindowTitle("New data file options")

            vbox = QVBoxLayout()

            filehbox = QHBoxLayout()
            fileLabel = QLabel("File name:")
            fileLabel.setMargin(20)
            fileInput = QLineEdit()
            self.fileNameInput = fileInput
            filehbox.addWidget(fileLabel)
            filehbox.addWidget(fileInput)
            vbox.addLayout(filehbox)

            createButton = QPushButton("Create")
            createButton.clicked.connect(self.createDataFile)
            vbox.addWidget(createButton)
            dialog.setLayout(vbox)
            self.createFileDialog = dialog
            dialog.exec_()

    def createDataFile(self):
        if self.fileNameInput.text() == "":
            QMessageBox.about(self,
            "Impossible action",
            "You must enter a file name"
            )
        else:
            files = os.listdir(self.dataDirectory)
            fileName = self.fileNameInput.text()
            print(files)
            if fileName in files:
                QMessageBox.about(self,
                "Impossible action",
                "This file name already exist"
                )
                self.createDataFileWin()
            else:
                self.dataFile = "%s/%s"%(self.dataDirectory, fileName)
                print(self.dataFile)
                self.dataFileObject = open(self.dataFile, "w+")
                self.dataFileObject.write("imageFile, type, x1, y1, x2, y2")
                self.statusBar().showMessage("New data file %s created"%self.dataFile)
            self.createFileDialog.close()

    def connectToDataFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.dataFile, _ = QFileDialog.getOpenFileName(self,"Data file selection", self.dataDirectory,"CSV (*.csv)", options=options)
        if self.dataFile != "":
            self.statusBar().showMessage("Writing to file %s"%self.dataFile)
            self.dataDirectory = "/".join(self.dataFile.split("/")[:-1])
            self.dataFileObject = open(self.dataFile, "w+")

    def enablePointsDrawing(self):
        if self.image == "":
            QMessageBox.about(self,
            "Enable to draw points",
            "You must import an image to be able to draw points"
            )
        else:
            self.statusBar().showMessage("Points drawing enable")
            self.imageLabel.mousePressEvent = self.drawPoint

    # Position isn't correct
    # point drawing isn't working
    def drawPoint(self, event):
        self.pointCount += 1
        x = event.pos().x()
        y = event.pos().y()
        print(x, y)
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.red)
        qp.drawPoint(x, y)
        if self.pointCount == 2:
            print(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Read and set style
    with open("app.css") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    sys.exit(app.exec_())
