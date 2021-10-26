import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QWidget, QLabel, QVBoxLayout, QInputDialog
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


class Main(QMainWindow, QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1200, 600)
        self.todosWidgets = []
        self.tracks = ["kick", "snare", "hihat", "tomOne", "tomTwo", "tomThree", "over", "bass", "piano", "vox"]

        self.initXBox = 240
        self.initYBox = 15
        self.initXLabel = 330
        self.initYBoxLabel = 65
        self.sizeTextX = 70

        # LOAD AUDIOS #
        self.btnMix = QPushButton('Mix', self)
        self.btnMix.setGeometry(10, 10, 200, 50)
        self.btnMix.clicked.connect(lambda: self.loadPathAudios())

        # CREATE NEW BOX #
        self.btnAdd = QPushButton('Añadir instrumento', self)
        self.btnAdd.setGeometry(10, 70, 200, 50)
        self.btnAdd.clicked.connect(lambda: self.showModalWindow())

        for track in self.tracks:

            self.checkDimensions()

            globals()['string%s' % track] = ListboxWidget(self)
            globals()['string%s' % track].setPos(self.initXBox, self.initYBox)
            globals()['string%s' % track + 'label'] = qtw.QLabel(track, self)
            globals()['string%s' % track + 'label'].setGeometry(self.initXLabel, self.initYBoxLabel, self.sizeTextX, 30)
            self.todosWidgets.append(globals()['string%s' % track])

            #trackWithName = [track, globals()['string%s' % track]]
            #self.todos.append(trackWithName)

            self.initYBox += 80
            self.initYBoxLabel += 80

        # TITLE
        # audioTwoLabel = qtw.QLabel("Drums", self)
        # audioTwoLabel.setGeometry(210, 5, 40, 30)

        #chart = Canvas(self)

    def loadPathAudios(self):
        infoFinal = []
        cont = 0
        for item in self.todosWidgets:
            path = QListWidgetItem(item.item(0))
            if path.text():
                path = path.text()
                pista = self.tracks[cont]
                infoFinal.append([pista, path])

            cont += 1

        loadedTracks = loadTracks.loadTrackswithPath(infoFinal)
        print(loadedTracks)

    def showModalWindow(self):
        text, ok = QInputDialog.getText(self, 'Añadir Instrumento', 'Escribe el nombre de tu instrumento:')
        if ok:
            self.createNewBox(text)

    def checkDimensions(self):

        if self.initYBox >= 575 and self.initXBox == 240:
            self.initYBox = 15
            self.initYBoxLabel = 65
            self.initXBox = 470
            self.initXLabel = 550

        if self.initYBox >= 575 and self.initXBox == 470:
            self.initYBox = 15
            self.initYBoxLabel = 65
            self.initXBox = 700
            self.initXLabel = 780

        if self.initYBox >= 575 and self.initXBox == 700:
            self.initYBox = 15
            self.initYBoxLabel = 65
            self.initXBox = 920
            self.initXLabel = 1020

    def createNewBox(self, inName):

        self.checkDimensions()

        globals()['string%s' % inName] = ListboxWidget(self)
        globals()['string%s' % inName].setPos(self.initXBox, self.initYBox)
        globals()['string%s' % inName].show()

        trackWithName = [inName, globals()['string%s' % inName]]
        self.todos.append(trackWithName)
        #self.todos.append(globals()['string%s' % inName])

        globals()['string%s' % inName + 'label'] = qtw.QLabel(inName, self)
        globals()['string%s' % inName + 'label'].setGeometry(self.initXLabel, self.initYBoxLabel, self.sizeTextX, 30)
        globals()['string%s' % inName + 'label'].show()

        self.initYBox += 80
        self.initYBoxLabel += 80

        print(inName, "añadido")

app = QApplication(sys.argv)
demo = Main()
demo.show()
sys.exit(app.exec_())