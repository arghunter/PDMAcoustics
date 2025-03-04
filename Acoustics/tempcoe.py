
import numpy as np
from OldBitstreamBeamformer import Beamformer

spacing=np.array([[-0.06,-0.24,0],[-0.18,-0.24,0],[-0.06,-0.12,0],[-0.18,-0.12,0],[-0.06,0,0],[-0.18,0,0],[-0.06,0.12,0],[-0.18,0.12,0],[0.18,-0.24,0],[0.06,-0.24,0],[0.18,-0.12,0],[0.06,-0.12,0],[0.18,0,0],[0.06,0,0],[0.18,0.12,0],[0.06,0.12,0]])

n_channels=1


for ch in range(n_channels):
    with open(f"tempmembig.txt", "w") as f:
        for i in range(16384):
            if i<4:
                
                f.write(str(hex(int(1)))+",\n")
            else:
                f.write(str(hex(int(0)))+",\n")
        

# Print min and max values
# print(f"Max shift value: {np.max(shifts)}")
# print(f"Min shift value: {np.min(shifts)}")