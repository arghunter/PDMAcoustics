
import numpy as np
from OldBitstreamBeamformer import Beamformer

spacing=np.array([[-0.06,-0.24,0],[-0.18,-0.24,0],[-0.06,-0.12,0],[-0.18,-0.12,0],[-0.06,0,0],[-0.18,0,0],[-0.06,0.12,0],[-0.18,0.12,0],[0.18,-0.24,0],[0.06,-0.24,0],[0.18,-0.12,0],[0.06,-0.12,0],[0.18,0,0],[0.06,0,0],[0.18,0.12,0],[0.06,0.12,0]])

n_channels=16
samplerate=16000*64
segments=16
fov=120

beam=Beamformer(n_channels=n_channels,coord=spacing,sample_rate=samplerate)


azi=-fov/2
ele=-fov/2
shifts=np.zeros((segments,segments,n_channels))
for i in range(segments):
    for j in range(segments):


        print(i)
        beam.update_delays(azi+(fov/segments)/2,ele+(fov/segments)/2)
        shifts[i][j] = np.round(beam.calculate_channel_shift()).astype(int)

        
        
        
        
        ele+=fov/segments
        
    ele=-fov/2
    azi+=fov/segments

for ch in range(n_channels):
    with open(f"shiftsthurd_channel_{ch}.txt", "w") as f:
        for i in range(segments):
            for j in range(segments):
                f.write(str(hex(int(shifts[i][j][ch])))+",\n")

# Print min and max values
print(f"Max shift value: {np.max(shifts)}")
print(f"Min shift value: {np.min(shifts)}")