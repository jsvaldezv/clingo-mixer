import clingo
import random
import math
import loadTracks
import copy
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

# **** NUMERO DE MEZCLAS POR HACER ***** #
numMixes = 3

# **** CONFIGURAR Y CARGAR CLINGO ***** #
control = clingo.Control(clingo_args)
control.configuration.solve.models = numMixes
control.load("mixer.lp")
models = []

# **** INSTRUMENTOS A MEZCLAR ***** #
instrumentosOri = ["kick", "snare", "hihat", "tomOne", "tomTwo", "tomThree", "over", "bass", "guitOne", "guitTwo",
                   "piano", "vox"]

# *** CARGAR AUDIOS **** #
loadedTracks = loadTracks.loadTracks(instrumentosOri)
print("------")

# DISPONIBLES: kick, snare, hihat, tomOne, tomTwo, tomThree, over, bass, guitOne, guitTwo, piano, vox
## SE PUDE MODIFICAR
instrumentosClingo = ["kick", "snare", "hihat", "tomOne", "tomTwo", "tomThree", "over", "bass", "guitOne", "guitTwo", "piano", "vox"]

# **** AÑADIR HECHOS A LP ***** #
for instrumento in instrumentosClingo:
    fact = "track(" + instrumento + ", on)."
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

# **** OBTENER RESULTADOS ***** #
cont = 0
resultados = []
for model in models:
    resp = []
    print("MIX ", cont+1)
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

        print("Aplicar", pan, "de paneo a", instrumento, "con un volumen de", vol, "y reverb de", rev*10)

    resultados.append(resp)
    cont += 1

# *** ORDENAR RESULTADOS Y AUDIOS **** #
loadedTracks = sorted(loadedTracks)
resultadosPre = sorted(resultados)
resultados = []
for result in resultadosPre:
    resultados.append(sorted(result))

# *** MIXING *** #
print("---------")
print("Mixing...")
for answer in range(numMixes):
    # ******** CHECAR SI HAY O NO MÁS ANSWERS DE LAS REQUERIDAS ******** #
    if (answer+1) <= len(resultados):
        tracksModified = copy.deepcopy(loadedTracks)
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
            #trackFinal += tracksModified[numeroPista][1]
            trackFinal += tracksModified[numeroPista][1] + reverbSound

            cont += 1

        # ************************** RENDER MIX **************************** #
        sf.write('mixes/mix_' + str(answer+1) + '.wav', trackFinal, 44100, 'PCM_24')
        print("Mezcla", answer+1, "creada")
    else:
        print("Ya no hay más mezclas disponibles")
        break

# *** END *** #
print("-------")
print("¡Ya puedes escuchar tus mezclas!")