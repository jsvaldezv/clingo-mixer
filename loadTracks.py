from soundfile import SoundFile
import numpy as np

def loadTracks(inInstrumentos):
    print("Agregando stems...")
    tracks = []
    for track in inInstrumentos:
        if track == "kick":
            file = SoundFile('Stems_Mixer/kick.wav')
        elif track == "snare":
            file = SoundFile('Stems_Mixer/snare.wav')
        elif track == "hihat":
            file = SoundFile('Stems_Mixer/hihat.wav')
        elif track == "tomOne":
            file = SoundFile('Stems_Mixer/tomOne.wav')
        elif track == "tomTwo":
            file = SoundFile('Stems_Mixer/tomTwo.wav')
        elif track == "tomThree":
            file = SoundFile('Stems_Mixer/tomThree.wav')
        elif track == "over":
            file = SoundFile('Stems_Mixer/over.wav')
        elif track == "bass":
            file = SoundFile('Stems_Mixer/bass.wav')
        elif track == "guitOne":
            file = SoundFile('Stems_Mixer/guitOne.wav')
        elif track == "guitTwo":
            file = SoundFile('Stems_Mixer/guitTwo.wav')
        elif track == "piano":
            file = SoundFile('Stems_Mixer/piano.wav')
        else:
            file = SoundFile('Stems_Mixer/vox.wav')

        if file.channels == 1:
            stereoSamples = []
            samples = file.read()
            for sample in samples:
                stereoSample = [sample, sample]
                stereoSamples.append(stereoSample)

            stereoSound = np.append([[0.0, 0.0]], stereoSamples, axis=0)
            stereoSound = np.delete(stereoSound, 0, 0)
            tracks.append([track, stereoSound])
            print(track + " agregado")

        else:
            tracks.append([track, file.read()])
            print(track + " agregado")

    return tracks

def loadTrackswithPath(inPaths):
    print("Agregando stems...")
    tracks = []
    for path in inPaths:
        print(path)

        track = path[0]
        file = SoundFile(path[1])

        if file.channels == 1:
            stereoSamples = []
            samples = file.read()
            for sample in samples:
                stereoSample = [sample, sample]
                stereoSamples.append(stereoSample)

            stereoSound = np.append([[0.0, 0.0]], stereoSamples, axis=0)
            stereoSound = np.delete(stereoSound, 0, 0)
            tracks.append([track, stereoSound])
            print(track + " agregado")

        else:
            tracks.append([track, file.read()])
            print(track + " agregado")

    print("AUDIOS CARGADOS")
    return tracks

'''textfile = open('mixes/dato' + str(answer) + str(cont) + '.txt', "w")
for elem in tracksModified[cont][1]:
    textfile.write(str(elem[0]) + ', ' + str(elem[1]) + '\n')
    #print("elem:", elem)
textfile.close()'''