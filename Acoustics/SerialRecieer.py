import serial
import numpy as np
import time
ser = serial.Serial('COM5', 921600, timeout=1)
past=np.zeros(4,dtype=int)
pt=0
while True:
    byte = ser.read(1)
    past=np.roll(past,1)
    past[0]=(byte[0])
    print(str(past[0])+" "+str(pt))
    pt+=1
    if np.all(past==88):
        pt=0
        
        
          # Detect start marker
    #     data = ser.read(256)  # Read the full array
    #     bytearray()
    #     print(len(data))
    #     byte_array = np.frombuffer(data, dtype=np.uint8)  # Convert to numpy array of integers
    #     print("Received as integer array:", byte_array)
