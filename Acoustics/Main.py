import numpy as np
import CICFilter as cic
import DataGatherer
from OldBitstreamBeamformer import Beamformer
import Visual
spacing=np.array([[-0.06,-0.24,0],[-0.18,-0.24,0],[-0.06,-0.12,0],[-0.18,-0.12,0],[-0.06,0,0],[-0.18,0,0],[-0.06,0.12,0],[-0.18,0.12,0],[0.18,-0.24,0],[0.06,-0.24,0],[0.18,-0.12,0],[0.06,-0.12,0],[0.18,0,0],[0.06,0,0],[0.18,0.12,0],[0.06,0.12,0]])
testNum=186
n_channels=16
samplerate=48000*64
duration=2
subduration=2
segments=7
fov=180
interpScale=4
time_segs=int(np.ceil(subduration*10))
sample_count=960
rms_data=np.zeros((segments,segments,int(time_segs)))

beam=Beamformer(n_channels=n_channels,coord=spacing,sample_rate=samplerate)
data=DataGatherer.get_multi_channel_data(testNum,samplerate,duration,subduration)
tarr=np.zeros(49)
ik=0
azi=-fov/2
ele=-fov/2
import time
for i in range(segments):
    for j in range(segments):


        # print(i)
        t1=time.time()
        beam.update_delays(azi+(fov/segments)/2,ele+(fov/segments)/2)
        outdata=beam.beamform(data.T)
        outdatapcm=cic.cic(outdata)
        # print(time.time()-t1)
        tarr[ik]=time.time()-t1
        ik+=1
        for k in range(time_segs-1):
            
            rms_data[i][j][k]=np.mean(outdatapcm[k*sample_count:(k+1)*sample_count]**2)
        rms_data[i][j][time_segs-1]=np.mean(outdatapcm[(time_segs-1)*sample_count:]**2)
        
        
        ele+=fov/segments
        print(str(i)+","+str(j))
    ele=-fov/2
    azi+=fov/segments
print(tarr)
np.save("./Acoustics/PDMTests/"+str(testNum)+"/rms_data_"+str(segments)+"_"+str(subduration)+".npy", rms_data)

Visual.gen_anim(rms_data,segments,subduration,testNum,interpScale,fov)