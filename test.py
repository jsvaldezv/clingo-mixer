from soundfile import SoundFile
from pysndfx import AudioEffectsChain
import soundfile as sf

file = SoundFile('Stems_Mixer/guitOne.wav')
samples = file.read()

reverb = AudioEffectsChain().reverb(reverberance=90)
delay = (AudioEffectsChain().delay(delays=list((500, 500+500)), decays=list((0.5, 0.1))))

delayAudio = delay(samples)
reverbAudio = reverb(samples)

sf.write('mixes/delay.wav', delayAudio, 44100, 'PCM_24')
sf.write('mixes/rev.wav', reverbAudio, 44100, 'PCM_24')
