import serial
import numpy as np
import time
ser = serial.Serial('COM5', 921600, timeout=1)
past=np.zeros(4,dtype=int)
pt=0
times=0
pdata= np.zeros((16,16,60))  
while times<60:
    byte = ser.read(1)
    past=np.roll(past,1)
    past[0]=(byte[0])
    # print(str(past[0])+" "+str(pt))
    pt+=1
    if(pt<256):
        pdata[int(pt/16)][int(pt %16)][times]+=np.abs(past[0])
    if np.all(past==88):
        pt=0
        times+=1
        print(times)

import Visual
Visual.gen_anim(pdata,16,2.191,1000,1,120)
