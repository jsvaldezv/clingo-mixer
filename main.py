import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QWidget
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QInputDialog, QSpinBox, QMessageBox
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt, QUrl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import clingo, random, math, loadTracks, copy
import soundfile as sf
from pysndfx import AudioEffectsChain
import numpy as np

clingo_args = [ "--warn=none",
                "--sign-def=rnd",
                "--sign-fix",
                "--rand-freq=1",
                "--seed=%s"%random.randint(0,32767),
                "--restart-on-model",
                "--enum-mode=record"]


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
        self.models = []
        self.validNames = ["kick", "snare", "hihat", "tomOne", "tomTwo", "tomThree", "over", "bass", "guitOne",
                           "guitTwo", "piano", "vox", "clap", "cymbal", "shaker", "acouguit", "synth", "strings",
                           "arp", "drums"]
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

        # AÑADIR #
        self.btnAdd = QPushButton('Añadir instrumento', self)
        self.btnAdd.setGeometry(10, 70, 200, 50)
        self.btnAdd.clicked.connect(lambda: self.showModalWindow())

        # LIMPIAR #
        self.btnAdd = QPushButton('Limpiar', self)
        self.btnAdd.setGeometry(10, 130, 200, 50)
        self.btnAdd.clicked.connect(lambda: self.clear())

        self.numMixes = QLabel(self)
        self.numMixes.setText("Numero de mezclas")
        self.numMixes.setGeometry(15, 200, 190, 30)

        self.sp = QSpinBox(self)
        self.sp.setGeometry(15, 230, 190, 30)
        self.sp.setValue(1)
        self.sp.show()

        self.label = QLabel(self)
        self.label.setText("Instrumentos validos:")
        self.label.setGeometry(15, 260, 190, 30)
        self.label.show()

        self.inicioX = 15
        self.inicioY = 285

        for name in self.validNames:
            globals()['string%s' % name] = QLabel(self)
            globals()['string%s' % name].setText(name)
            globals()['string%s' % name].setGeometry(self.inicioX,  self.inicioY, 190, 30)
            self.inicioY += 20

            if self.inicioY >= 575:
                self.inicioY = 285
                self.inicioX = 100

        for track in self.tracks:
            self.checkDimensions()
            globals()['string%s' % track] = ListboxWidget(self)
            globals()['string%s' % track].setPos(self.initXBox, self.initYBox)
            globals()['string%s' % track + 'label'] = qtw.QLabel(track, self)
            globals()['string%s' % track + 'label'].setGeometry(self.initXLabel, self.initYBoxLabel, self.sizeTextX, 30)
            self.todosWidgets.append(globals()['string%s' % track])
            self.initYBox += 80
            self.initYBoxLabel += 80

        #chart = Canvas(self)

    def clear(self):
        for track in self.tracks:
            globals()['string%s' % track].clear()

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
        # **** CONFIGURAR Y CARGAR CLINGO ***** #
        control = clingo.Control(clingo_args)
        print(self.sp.value())
        control.configuration.solve.models = self.sp.value()
        control.load("mixer.lp")
        models = []

        # **** AÑADIR HECHOS A LP ***** #
        for instrumento in self.loadedTracks:
            fact = "track(" + instrumento[0] + ", on)."
            control.add("base", [], str(fact))

        # **** GROUNDING ***** #
        print("Grounding...")
        control.ground([("base", [])])
        print("------")

        # **** SOLVE ***** #
        print("Solving...")
        with control.solve(yield_=True) as solve_handle:
            for model in solve_handle:
                models.append(model.symbols(shown=True))
        print("------")

        cont = 0
        resultados = []
        for model in models:
            resp = []
            print("MIX ", cont + 1)
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

                print("Aplicar", pan, "de paneo a", instrumento, "con un volumen de", vol, "y reverb de", rev * 10)

            resultados.append(resp)
            cont += 1

        # *** ORDENAR RESULTADOS Y AUDIOS **** #
        self.loadedTracks = sorted(self.loadedTracks)
        self.resultadosPre = sorted(resultados)
        resultados = []
        for result in self.resultadosPre:
            resultados.append(sorted(result))

        # *** MIXING *** #
        print("---------")
        print("Mixing...")
        for answer in range(self.sp.value()):
            # ******** CHECAR SI HAY O NO MÁS ANSWERS DE LAS REQUERIDAS ******** #
            if (answer + 1) <= len(resultados):
                tracksModified = copy.deepcopy(self.loadedTracks)
                trackFinal = 0
                cont = 0

                for track in resultados[answer]:

                    # ****** CHECAR QUE PISTA SE VA A MODIFICAR ****** #
                    numeroPista = 0
                    for numPista in range(len(tracksModified)):

                        nombre = track[0]

                        if nombre == tracksModified[numPista][0]:
                            numeroPista = numPista
                            break

                    # ********************* PANEO ****************** #
                    factor = track[1] / 10
                    left_factor = math.cos(3.141592 * (factor + 1) / 4)
                    right_factor = math.sin(3.141592 * (factor + 1) / 4)

                    # ******************** VOLUMEN ****************** #
                    vol = track[2]
                    vol = vol / 10

                    # ********************* REVERB ****************** #
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

                    # ***************** OPERACIONES CON TRACKS **************** #
                    tracksModified[numeroPista][1][:, 0] *= left_factor * vol
                    tracksModified[numeroPista][1][:, 1] *= right_factor * vol

                    # *********************** SUMAR TRACKS ******************** #
                    # trackFinal += tracksModified[numeroPista][1]
                    trackFinal += tracksModified[numeroPista][1] + reverbSound

                    cont += 1

                # ************************** RENDER MIX **************************** #
                sf.write('mixes/mix_' + str(answer + 1) + '.wav', trackFinal, 44100, 'PCM_24')
                print("Mezcla", answer + 1, "creada")
            else:
                print("Ya no hay más mezclas disponibles")
                break

        # *** END *** #
        print("-------")
        print("¡Ya puedes escuchar tus mezclas!")

    def showModalWindow(self):
        text, ok = QInputDialog.getText(self, 'Añadir Instrumento', 'Escribe el nombre de tu instrumento:')
        if ok:
            if text in self.validNames:
                self.createNewBox(text)
            else:
                dialog = QMessageBox()
                dialog.setWindowTitle("Error")
                dialog.setText("Nombre no valido")
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

        globals()['string%s' % inName] = ListboxWidget(self)
        globals()['string%s' % inName].setPos(self.initXBox, self.initYBox)
        globals()['string%s' % inName].show()
        self.todosWidgets.append(globals()['string%s' % inName])

        globals()['string%s' % inName + 'label'] = qtw.QLabel(inName, self)
        globals()['string%s' % inName + 'label'].setGeometry(self.initXLabel, self.initYBoxLabel, self.sizeTextX, 30)
        globals()['string%s' % inName + 'label'].show()
        self.tracks.append(inName)

        self.initYBox += 80
        self.initYBoxLabel += 80

        print(inName, "añadido")


app = QApplication(sys.argv)
demo = Main()
demo.show()
sys.exit(app.exec_())