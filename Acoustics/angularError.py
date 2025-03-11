import numpy as np
samplerate=16000
d=0.025
c=340.3
avg=0
d0=[]
d1=[]
for i in range(90):
    ini_tdoa=d*np.cos(np.deg2rad(i))/c
    f_tdoa0=ini_tdoa+1/samplerate
    f_tdoa1=ini_tdoa-1/samplerate
    f0= f_tdoa0*c/d
    f1=f_tdoa1*c/d
    
    f_ang0=np.rad2deg(np.arccos(np.maximum(f_tdoa0*c/d,0)))
    f_ang1=np.rad2deg(np.arccos(np.maximum(f_tdoa1*c/d,0)))
    d0.append(f_ang0)
    d1.append(f_ang1)
    if(not np.isnan(f_ang0)):
        avg+=np.abs((i-f_ang0)/2)
    else:
        avg+=np.abs(i-f_ang1)/2
    

    if(not np.isnan(f_ang1)):
        avg+=np.abs(i-f_ang1)/2
    else: 
        avg+=np.abs(i-f_ang0)/2
        
print(avg/90)
# print(d0)
# print(d1)
    