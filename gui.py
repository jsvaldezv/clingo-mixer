import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QWidget, QLabel, QVBoxLayout
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt, QUrl
import loadTracks
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi = 200)
        super().__init__(fig)
        self.setParent(parent)

        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)

        self.ax.plot(t, s)

        self.ax.set(xlabel='time (s)', ylabel="mV", title="YES")
        self.ax.grid()

        fig.savefig("test.png")
        plt.show()

class ListboxWidget(QListWidget):

    def __init__(self,  parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))

            self.addItems(links)
        else:
            event.ignore()

    def setPos(self, posX, posY):
        self.setGeometry(posX, posY, 200, 50)

class AppDemo(QMainWindow, QWidget):
    
    def __init__(self):
        super().__init__()
        self.resize(1200, 600)
        self.todos = []

        audioTwoLabel = qtw.QLabel("Drums", self)
        audioTwoLabel.setGeometry(210, 5, 40, 30)

        self.audioOne = ListboxWidget(self)
        self.audioOne.setPos(10, 40)
        audioOneLabel = qtw.QLabel("Kick", self)
        audioOneLabel.setGeometry(95, 90, 30, 30)
        self.todos.append(self.audioOne)

        self.audioTwo = ListboxWidget(self)
        self.audioTwo.setPos(10, 130)
        audioTwoLabel = qtw.QLabel("Snare", self)
        audioTwoLabel.setGeometry(95, 180, 40, 30)
        self.todos.append(self.audioTwo)

        self.audioTres = ListboxWidget(self)
        self.audioTres.setPos(10, 230)
        audioTresLabel = qtw.QLabel("HiHat", self)
        audioTresLabel.setGeometry(95, 280, 40, 30)
        self.todos.append(self.audioTres)

        '''self.audioTwo = ListboxWidget(self)
        self.audioTwo.setPos(10, 230)
        audioTwoLabel = qtw.QLabel("HiHat", self)
        audioTwoLabel.setGeometry(95, 280, 40, 30)

        self.audioTwo = ListboxWidget(self)
        self.audioTwo.setPos(10, 330)
        audioTwoLabel = qtw.QLabel("Tom 1", self)
        audioTwoLabel.setGeometry(95, 380, 40, 30)

        self.audioTwo = ListboxWidget(self)
        self.audioTwo.setPos(10, 430)
        audioTwoLabel = qtw.QLabel("Tom 2", self)
        audioTwoLabel.setGeometry(95, 480, 40, 30)

        self.audioTwo = ListboxWidget(self)
        self.audioTwo.setPos(10, 530)
        audioTwoLabel = qtw.QLabel("Tom 3", self)
        audioTwoLabel.setGeometry(95, 580, 40, 30)

        self.audioTwo = ListboxWidget(self)
        self.audioTwo.setPos(10, 630)
        audioTwoLabel = qtw.QLabel("Over", self)
        audioTwoLabel.setGeometry(95, 680, 40, 30)

        self.audioTwo = ListboxWidget(self)
        self.audioTwo.setPos(10, 710)
        audioTwoLabel = qtw.QLabel("Cymbal", self)
        audioTwoLabel.setGeometry(95, 760, 60, 40)'''

        self.audioFour = ListboxWidget(self)
        self.audioFour.setPos(250, 40)
        audioFourLabel = qtw.QLabel("Shaker", self)
        audioFourLabel.setGeometry(325, 90, 50, 30)
        self.todos.append(self.audioFour)

        self.audioFive = ListboxWidget(self)
        self.audioFive.setPos(250, 130)
        audioFiveLabel = qtw.QLabel("Clap", self)
        audioFiveLabel.setGeometry(325, 180, 50, 30)
        self.todos.append(self.audioFive)

        self.audioSix = ListboxWidget(self)
        self.audioSix.setPos(250, 230)
        audioSixLabel = qtw.QLabel("Cymbal", self)
        audioSixLabel.setGeometry(325, 280, 50, 30)
        self.todos.append(self.audioSix)

        self.btnMix = QPushButton('Mix', self)
        self.btnMix.setGeometry(0, 500, 200, 50)
        self.btnMix.clicked.connect(lambda: self.getSelectedItem())

        # self.btnAdd = QPushButton('Añadir instrumento', self)
        # self.btnAdd.setGeometry(500, 30, 200, 50)
        # self.btnAdd.clicked.connect(lambda: self.createNewBox())

        #chart = Canvas(self)

    def getSelectedItem(self):
        paths = []
        for item in self.todos:
            path = QListWidgetItem(item.item(0))
            if path.text():
                paths.append(path.text())
        loadTracks.loadTrackswithPath(paths)

    def createNewBox(self):
        self.newBox = ListboxWidget()
        self.newBox.setPos(10, 630)
        print("CREATE NEW BOX")

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())