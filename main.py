#!/usr/bin/python3

from ImageWidget import ImageWidget
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication,QFileDialog, QDialog, QLineEdit, QAction, qApp, QDesktopWidget
from PyQt5.QtWidgets import  QInputDialog, QWidget, QVBoxLayout, QLabel, QMessageBox, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image = ""
        self.imagesDirectory = ""
        self.dataDirectory = ""
        self.dataFile = ""
        self.dataFileObject = None
        self.imageLabel = None
        self.imageCount = 0
        self.pointCount = 0
        self.fileNameInput = None
        self.createFileDialog = None
        self.menu = None
        self.mainWidget = None
        self.imageWidget = None
        self.imageLayout = None
        self.sideWidget = None
        self.painter = None
        self.initUI()

    def initUI(self):
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

        drawPointsAction = QAction(QIcon("./drawRectangleIcon.png"), "Draw rectangle", self)
        drawPointsAction.setShortcut("Ctrl+P")
        drawPointsAction.setStatusTip("Draw edges points of object")

        self.menu = self.menuBar()
        imageImport = self.menu.addMenu("Import image")
        imageImport.addAction(importAction)
        dataFile = self.menu.addMenu("Data File")
        dataFile.addAction(emptyDataFileAction)
        dataFile.addAction(conDataFileAction)
        drawPoints = self.menu.addMenu("Drawing")
        drawPoints.addAction(drawPointsAction)

        screen = QDesktopWidget().screenGeometry(-1)
        self.setGeometry(0, 0, screen.width() , screen.height())
        self.setWindowTitle("Magic Image Annotator")

        self.mainWidget = QWidget(self)
        self.mainWidget.setObjectName("main-widget")
        self.mainWidget.setFixedSize(screen.width(), screen.height())
        self.mainWidget.move(0, self.menu.height()-6)
        self.mainWidget.setContentsMargins(0, 0, 0, 0)

        hLayout = QHBoxLayout(self.mainWidget)
        hLayout.setContentsMargins(0, 0, 0, 0)

        self.imageWidget = ImageWidget(QColor(51, 51, 51), self)
        self.imageWidget.setObjectName("image-widget")
        self.imageWidget.setFixedSize(0.8*screen.width()-1, screen.height())
        self.imageWidget.move(0, self.menu.height())
        self.imageWidget.setContentsMargins(0, 0, 0, 0)
        drawPointsAction.triggered.connect(self.imageWidget.enablePointsDrawing)

        self.sideWidget = QWidget()
        self.sideWidget.setObjectName("side-widget")
        self.sideWidget.setFixedSize(0.2*screen.width()-1, screen.height())
        self.sideWidget.setContentsMargins(0, 0, 0, 0)
        sideLayout = QVBoxLayout(self.sideWidget)

        hLayout.addWidget(self.imageWidget)
        hLayout.addWidget(self.sideWidget)

        self.resizeEvent = self.resizer
        self.show()

    def resizer(self, event):
        if self.mainWidget and self.imageWidget and self.sideWidget:
            w = event.size().width()
            h = event.size().height()
            self.mainWidget.setFixedSize(w,h)
            self.imageWidget.setFixedSize(0.8*w-1, h)
            self.sideWidget.setFixedSize(0.2*w-1, h)

    def importImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.image, _ = QFileDialog.getOpenFileName(self,"Image selection", self.imagesDirectory,"Images (*.png *.jpeg *.jpg)", options=options)
        if self.image != "":
            self.statusBar().showMessage("Processing image %s"%self.image)
            self.imageWidget.setImage(self.image)

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
                self.dataFileObject.write("imageFile, type, x, y, w, h")
                self.statusBar().showMessage("New data file %s created"%self.dataFile)
        self.createFileDialog.close()

    def connectToDataFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.dataFile, _ = QFileDialog.getOpenFileName(
            self,"Data file selection",
            self.dataDirectory,"CSV (*.csv)",
            options=options
        )
        if self.dataFile != "":
            self.statusBar().showMessage("Writing to file %s"%self.dataFile)
            self.dataDirectory = "/".join(self.dataFile.split("/")[:-1])
            self.dataFileObject = open(self.dataFile, "w+")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Read and set style
    with open("app.css") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    sys.exit(app.exec_())
