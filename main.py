import clingo
import random
import math
import loadTracks
import soundfile as sf

def calculteFactor(inPan):
    factor = inPan / 10
    return factor

clingo_args = [ "--warn=none",
                "--sign-def=rnd",
                "--sign-fix",
                "--rand-freq=1",
                "--seed=%s"%random.randint(0,32767),
                "--restart-on-model",
                "--enum-mode=record"]

# **** NUMERO DE MEZCLAS POR HACER ***** #
numMixes = 1

# **** CONFIGURAR Y CARGAR CLINGO ***** #
control = clingo.Control(clingo_args)
control.configuration.solve.models = numMixes
control.load("mixer.lp")
models = []

# **** INSTRUMENTOS A MEZCLAR ***** #
instrumentos = ["kick", "over", "guitOne", "bass", "guitTwo", "tomOne", "tomTwo", "tomThree"]

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
with control.solve(yield_=True) as solve_handle:
    for model in solve_handle:
        models.append(model.symbols(shown=True))

# **** OBTENER RESULTADOS ***** #
cont = 1

resultados = []
for model in models:
    print("MIX ", cont)
    for atom in model:
        #print(atom)

        instrumento = str(atom.arguments[0])
        pan = int(str(atom.arguments[1]))
        # vol = int(str(atom.arguments[2]))

        resul = []
        resul.append(instrumento)
        resul.append(pan)
        # resul.append(vol)

        resultados.append(resul)
        print("APLICAR", pan, "de paneo a", instrumento)
        # print("APLICAR", pan, "de paneo a", instrumento, "con un volumen de", vol)

    cont += 1

print("------")

# ORDERNAR RESULTADOS Y AUDIOS #
resultados = sorted(resultados)
loadedTracks = sorted(loadedTracks)

# HACER OPERACIONES DE PANEO #
cont = 0
trackFinal = 0

for track in resultados:
    # PANEO
    factor = calculteFactor(track[1])
    left_factor = math.cos(3.141592 * (factor + 1) / 4)
    right_factor = math.sin(3.141592 * (factor + 1) / 4)

    # VOLUMEN
    #vol = track[2]

    # OPERACIONES CON TRACKS
    loadedTracks[cont][1][:, 0] *= left_factor
    loadedTracks[cont][1][:, 1] *= right_factor

    # SUMAR TRACKS
    trackFinal += loadedTracks[cont][1]
    cont += 1

# CREAR AUDIOS
for mixes in range(numMixes):
    sf.write('mixes/mix_' + str(mixes) + '.wav', trackFinal, 44100, 'PCM_24')