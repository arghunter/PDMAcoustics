from DelayandSumBeamformer import Beamformer
import numpy as np
from IOStream import IOStream
from SignalGen import SignalGen
from Signal import Sine
spacing=np.array([[-0.06,-0.24,0],[-0.18,-0.24,0],[-0.06,-0.12,0],[-0.18,-0.12,0],[-0.06,0,0],[-0.18,0,0],[-0.06,0.12,0],[-0.18,0.12,0],[0.18,-0.24,0],[0.06,-0.24,0],[0.18,-0.12,0],[0.06,-0.12,0],[0.18,0,0],[0.06,0,0],[0.18,0.12,0],[0.06,0.12,0]])
sig_gen=SignalGen(16,spacing)
beam=Beamformer(n_channels=16,coord=spacing)

rms_data=0
import time
sine=Sine(1500,1,48000)
speech=sine.generate_wave(1)
speech=np.reshape(speech,(-1,1))
print(speech.shape)
print(speech.shape)
sig_gen.update_delays(0,0)
print(speech.shape)
angled_speech=sig_gen.delay_and_gain(speech)
print(angled_speech.shape)

        
io=IOStream()
io.arrToStream(angled_speech,48000)

t1=time.time()
beam.update_delays(90,0)
k=0
while(not io.complete()):
    
    sample=io.getNextSample()
    # sample[np.abs(sample) < (0.00063)] = 0
    outdata=beam.beamform(sample)
    rms_data+=np.mean(outdata**2)
    k+=1
        
print(time.time()-t1)

print(rms_data)