from soundfile import SoundFile
import numpy as np


def loadTracks(inInstrumentos):
    print("Add stems...")
    tracks = []
    for track in inInstrumentos:
        if track == "kick":
            file = SoundFile("stems/kick.wav")
        elif track == "snare":
            file = SoundFile("stems/snare.wav")
        elif track == "hihat":
            file = SoundFile("stems/hihat.wav")
        elif track == "tomOne":
            file = SoundFile("stems/tomOne.wav")
        elif track == "tomTwo":
            file = SoundFile("stems/tomTwo.wav")
        elif track == "tomThree":
            file = SoundFile("stems/tomThree.wav")
        elif track == "over":
            file = SoundFile("stems/over.wav")
        elif track == "bass":
            file = SoundFile("stems/bass.wav")
        elif track == "guitOne":
            file = SoundFile("stems/guitOne.wav")
        elif track == "guitTwo":
            file = SoundFile("stems/guitTwo.wav")
        elif track == "piano":
            file = SoundFile("stems/piano.wav")
        else:
            file = SoundFile("stems/vox.wav")

        if file.channels == 1:
            stereoSamples = []
            samples = file.read()
            for sample in samples:
                stereoSample = [sample, sample]
                stereoSamples.append(stereoSample)

            stereoSound = np.append([[0.0, 0.0]], stereoSamples, axis=0)
            stereoSound = np.delete(stereoSound, 0, 0)
            tracks.append([track, stereoSound])
            print(track + " added")

        else:
            tracks.append([track, file.read()])
            print(track + " added")

    return tracks


def checkStems(inPaths):
    print("---------")
    print("Checking stems...")
    mayor = 0
    for path in inPaths:
        file = SoundFile(path[1])
        if len(file) > mayor:
            mayor = len(file)
    print("---------")
    return mayor


def loadTrackswithPath(inPaths, inLen):
    print("Adding stems...")
    tracks = []

    for path in inPaths:
        track = path[0]
        file = SoundFile(path[1])

        if file.channels == 1:
            stereoSamples = []
            samples = file.read()

            for i in range(inLen):
                if i >= len(samples):
                    stereoSample = [0.0, 0.0]
                else:
                    stereoSample = [samples[i], samples[i]]

                stereoSamples.append(stereoSample)

            stereoSound = np.append([[0.0, 0.0]], stereoSamples, axis=0)
            stereoSound = np.delete(stereoSound, 0, 0)
            tracks.append([track, stereoSound])
            print(track + " added")

        else:
            stereoSamples = []
            samples = file.read()
            for i in range(inLen):
                if i >= len(samples):
                    stereoSample = [0.0, 0.0]
                else:
                    stereoSample = [samples[i][0], samples[i][1]]

                stereoSamples.append(stereoSample)

            stereoSound = np.append([[0.0, 0.0]], stereoSamples, axis=0)
            stereoSound = np.delete(stereoSound, 0, 0)
            tracks.append([track, stereoSound])

            print(track + " added")

    print("----------")
    return tracks
