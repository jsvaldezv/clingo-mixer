import clingo
import random
import math
import loadTracks
import copy
import soundfile as sf

clingo_args = [ "--warn=none",
                "--sign-def=rnd",
                "--sign-fix",
                "--rand-freq=1",
                "--seed=%s"%random.randint(0,32767),
                "--restart-on-model",
                "--enum-mode=record"]

# **** NUMERO DE MEZCLAS POR HACER ***** #
numMixes = 10

# **** CONFIGURAR Y CARGAR CLINGO ***** #
control = clingo.Control(clingo_args)
control.configuration.solve.models = numMixes
control.load("mixer.lp")
models = []

# **** INSTRUMENTOS A MEZCLAR ***** #
instrumentos = ["kick", "guitOne", "guitTwo", "tomOne"]

# *** CARGAR AUDIOS **** #
loadedTracks = loadTracks.loadTracks(instrumentos)
print("------")

# **** AÑADIR HECHOS A LP ***** #
for instrumento in instrumentos:
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
        #print(atom)

        instrumento = str(atom.arguments[0])
        pan = int(str(atom.arguments[1]))
        # vol = int(str(atom.arguments[2]))

        resul = []
        resul.append(instrumento)
        resul.append(pan)
        # resul.append(vol)

        resp.append(resul)

        print("APLICAR", pan, "de paneo a", instrumento)
        # print("Aplicar", pan, "de paneo a", instrumento, "con un volumen de", vol)

    resultados.append(resp)
    cont += 1

print("------")

# ORDERNAR RESULTADOS Y AUDIOS #
resultados = sorted(resultados)
loadedTracks = sorted(loadedTracks)

# HACER OPERACIONES DE PANEO #
tracksFinales = []

for answer in range(numMixes):

    if (answer+1) <= len(resultados):
        tracksModified = copy.deepcopy(loadedTracks)
        trackFinal = 0
        cont = 0

        for track in resultados[answer]:
            # PANEO
            factor = track[1] / 10
            left_factor = math.cos(3.141592 * (factor + 1) / 4)
            right_factor = math.sin(3.141592 * (factor + 1) / 4)

            # VOLUMEN
            #vol = track[2]

            # OPERACIONES CON TRACKS
            tracksModified[cont][1][:, 0] *= left_factor
            tracksModified[cont][1][:, 1] *= right_factor

            # SUMAR TRACKS
            trackFinal += tracksModified[cont][1]

            cont += 1

        sf.write('mixes/mix_' + str(answer+1) + '.wav', trackFinal, 44100, 'PCM_24')
    else:
        print("Ya no hay más mezclas disponibles")



'''textfile = open('mixes/dato' + str(answer) + str(cont) + '.txt', "w")
for elem in tracksModified[cont][1]:
    textfile.write(str(elem[0]) + ', ' + str(elem[1]) + '\n')
    #print("elem:", elem)
textfile.close()'''