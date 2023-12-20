import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QWidget,
)
from PyQt5.QtWidgets import QLabel, QInputDialog, QSpinBox, QMessageBox, QTextEdit
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt
import clingo, random, math, loadTracks, copy
import soundfile as sf
from pysndfx import AudioEffectsChain
import numpy as np

clingo_args = [
    "--warn=none",
    "--sign-def=rnd",
    "--sign-fix",
    "--rand-freq=1",
    "--seed=%s" % random.randint(0, 32767),
    "--restart-on-model",
    "--enum-mode=record",
]


class ListboxWidget(QListWidget):
    def __init__(self, parent=None):
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
        self.models = []
        self.validNames = [
            "kick",
            "snare",
            "hihat",
            "tomOne",
            "tomTwo",
            "tomThree",
            "over",
            "bass",
            "guitOne",
            "guitTwo",
            "piano",
            "vox",
            "clap",
            "cymbal",
            "shaker",
            "acouguit",
            "synth",
            "strings",
            "arp",
            "drums",
            "lead",
            "subbass",
            "fx",
            "violin",
        ]
        self.tracks = [
            "kick",
            "snare",
            "hihat",
            "tomOne",
            "tomTwo",
            "tomThree",
            "over",
            "bass",
            "piano",
            "vox",
        ]

        self.initXBox = 240
        self.initYBox = 15
        self.initXLabel = 330
        self.initYBoxLabel = 65
        self.sizeTextX = 70

        # Load audios
        self.btnMix = QPushButton("Mix", self)
        self.btnMix.setGeometry(10, 10, 200, 50)
        self.btnMix.clicked.connect(lambda: self.loadPathAudios())

        # Add
        self.btnAdd = QPushButton("Add instruments", self)
        self.btnAdd.setGeometry(10, 70, 200, 50)
        self.btnAdd.clicked.connect(lambda: self.showModalWindow())

        # Clean
        self.btnAdd = QPushButton("Clean", self)
        self.btnAdd.setGeometry(10, 130, 200, 50)
        self.btnAdd.clicked.connect(lambda: self.clear())

        self.numMixes = QLabel(self)
        self.numMixes.setText("Mixes number")
        self.numMixes.setGeometry(15, 200, 190, 30)

        self.sp = QSpinBox(self)
        self.sp.setGeometry(15, 230, 190, 30)
        self.sp.setValue(1)
        self.sp.show()

        self.label = QLabel(self)
        self.label.setText("Valid instruments:")
        self.label.setGeometry(15, 260, 190, 30)
        self.label.show()

        self.inicioX = 15
        self.inicioY = 285

        for name in self.validNames:
            globals()["string%s" % name] = QLabel(self)
            globals()["string%s" % name].setText(name)
            globals()["string%s" % name].setGeometry(
                self.inicioX, self.inicioY, 190, 30
            )
            self.inicioY += 20

            if self.inicioY >= 575:
                self.inicioY = 285
                self.inicioX = 100

        for track in self.tracks:
            self.checkDimensions()
            globals()["string%s" % track] = ListboxWidget(self)
            globals()["string%s" % track].setPos(self.initXBox, self.initYBox)
            globals()["string%s" % track + "label"] = qtw.QLabel(track, self)
            globals()["string%s" % track + "label"].setGeometry(
                self.initXLabel, self.initYBoxLabel, self.sizeTextX, 30
            )
            self.todosWidgets.append(globals()["string%s" % track])
            self.initYBox += 80
            self.initYBoxLabel += 80

        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(930, 15, 250, 575)

    def clear(self):
        for track in self.tracks:
            globals()["string%s" % track].clear()

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

        longitudMax = loadTracks.checkStems(infoFinal)
        self.loadedTracks = loadTracks.loadTrackswithPath(infoFinal, longitudMax)
        self.solveWithClingo()

    def solveWithClingo(self):
        self.textEdit.clear()
        self.printText("Starting...")
        self.printText("-------------")

        # Configure clingo
        control = clingo.Control(clingo_args)
        control.configuration.solve.models = self.sp.value()
        control.load("mixer.lp")
        models = []

        # Add facts to LP
        for instrumento in self.loadedTracks:
            fact = "track(" + instrumento[0] + ", on)."
            control.add("base", [], str(fact))

        # Grounding
        print("Grounding...")
        self.printText("Grounding...")
        control.ground([("base", [])])
        print("------")
        self.printText("-------------")

        # Solve
        print("Solving...")
        self.printText("Solving...")
        with control.solve(yield_=True) as solve_handle:
            for model in solve_handle:
                models.append(model.symbols(shown=True))
        print("------")
        self.printText("-------------")

        cont = 0
        resultados = []
        for model in models:
            resp = []
            print("MIX ", cont + 1)
            self.printText("MIX " + str(cont + 1))
            for atom in model:
                instrumento = str(atom.arguments[0])
                pan = int(str(atom.arguments[1]))
                vol = int(str(atom.arguments[2]))
                rev = int(str(atom.arguments[3]))

                resul = []
                resul.append(instrumento)
                resul.append(pan)
                resul.append(vol)
                resul.append(rev)

                resp.append(resul)

                print(
                    " - Add",
                    pan,
                    "of pan to",
                    instrumento,
                    "with gain of",
                    vol,
                    "and reverb mix of",
                    rev * 10,
                )
                self.printText(
                    " - Add",
                    +str(pan)
                    + "of pan to"
                    + str(instrumento)
                    + "with gain of"
                    + str(vol)
                    + "and reverb mix of"
                    + str(rev * 10),
                )

            resultados.append(resp)
            cont += 1
            self.printText("-------------")

        # Order results and audios
        self.loadedTracks = sorted(self.loadedTracks)
        self.resultadosPre = sorted(resultados)
        resultados = []
        for result in self.resultadosPre:
            resultados.append(sorted(result))

        # Mix
        print("---------")
        print("Mixing...")
        self.printText("Rendering...")
        for answer in range(self.sp.value()):
            # Check if there is no more answers required
            if (answer + 1) <= len(resultados):
                tracksModified = copy.deepcopy(self.loadedTracks)
                trackFinal = 0
                cont = 0

                for track in resultados[answer]:
                    numeroPista = 0
                    for numPista in range(len(tracksModified)):
                        nombre = track[0]

                        if nombre == tracksModified[numPista][0]:
                            numeroPista = numPista
                            break

                    # ********************* Pan ****************** #
                    factor = track[1] / 10
                    left_factor = math.cos(3.141592 * (factor + 1) / 4)
                    right_factor = math.sin(3.141592 * (factor + 1) / 4)

                    # ******************** Gain ****************** #
                    vol = track[2]
                    vol = vol / 10

                    # ********************* Reverb ****************** #
                    rev = track[3] * 10
                    reverb = AudioEffectsChain().reverb(reverberance=rev)

                    withReverb = copy.deepcopy(tracksModified[numeroPista][1])
                    left = []
                    right = []

                    for sample in withReverb:
                        left.append(sample[0])
                        right.append(sample[1])

                    forEffect = []
                    forEffect.append(left)
                    forEffect.append(right)
                    arr = np.array(forEffect)
                    reverbAudio = reverb(arr)
                    stereoSamples = []
                    for sample in reverbAudio[0]:
                        stereoSample = [sample, sample]
                        stereoSamples.append(stereoSample)

                    reverbSound = np.append([[0.0, 0.0]], stereoSamples, axis=0)
                    reverbSound = np.delete(reverbSound, 0, 0)

                    # ***************** Operations with tracks **************** #
                    tracksModified[numeroPista][1][:, 0] *= left_factor * vol
                    tracksModified[numeroPista][1][:, 1] *= right_factor * vol
                    reverbSound[:, 0] *= left_factor * vol * 0.5
                    reverbSound[:, 1] *= right_factor * vol * 0.5

                    # *********************** Sum tracks ******************** #
                    trackFinal += tracksModified[numeroPista][1] + reverbSound

                    cont += 1

                # ************************** Render mix **************************** #
                sf.write(
                    "mixes/mix_" + str(answer + 1) + ".wav", trackFinal, 44100, "PCM_24"
                )
                print("Mix", answer + 1, "created")
                self.printText("Mix " + str(answer + 1) + " created")
            else:
                print("There is no more mixes available")
                self.printText("There is no more mixes available")
                break

        # *** END *** #
        print("-------")
        self.printText("-------------")
        print("Listen your mixes!")
        self.printText("Listen your mixes!")

    def showModalWindow(self):
        text, ok = QInputDialog.getText(
            self, "Add instrument", "Type the name of the instrument:"
        )
        if ok:
            if text in self.validNames:
                self.createNewBox(text)
            else:
                dialog = QMessageBox()
                dialog.setWindowTitle("Error")
                dialog.setText("Not valid name")
                dialog.setIcon(QMessageBox.Critical)
                dialog.exec_()

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

        globals()["string%s" % inName] = ListboxWidget(self)
        globals()["string%s" % inName].setPos(self.initXBox, self.initYBox)
        globals()["string%s" % inName].show()
        self.todosWidgets.append(globals()["string%s" % inName])

        globals()["string%s" % inName + "label"] = qtw.QLabel(inName, self)
        globals()["string%s" % inName + "label"].setGeometry(
            self.initXLabel, self.initYBoxLabel, self.sizeTextX, 30
        )
        globals()["string%s" % inName + "label"].show()
        self.tracks.append(inName)

        self.initYBox += 80
        self.initYBoxLabel += 80

        print(inName, "added")

    def printText(self, inText):
        cursor = self.textEdit.textCursor()
        cursor.atEnd()
        cursor.insertText(inText + "\n")


app = QApplication(sys.argv)
demo = Main()
demo.show()
sys.exit(app.exec_())
