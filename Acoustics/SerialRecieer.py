import serial
import numpy as np
import time


ser = serial.Serial('COM5', 921600, timeout=1)

past = np.zeros(4, dtype=int)  # Preamble buffer
pt = 0
times = 0
pdata = np.zeros((16, 16, 60), dtype=int)

while times < 60:
    byte_pair = ser.read(2)  # Read 2 bytes at a time
    if len(byte_pair) < 2:
        continue  # Skip if not enough bytes received
    
    value = int.from_bytes(byte_pair, byteorder='little')  # Convert to 16-bit value
    past = np.roll(past, 2)
    past[:2] = [byte_pair[0], byte_pair[1]]

    # Detect preamble (88 88 88 88)
    if np.all(past == 88):
        pt = 0  # Reset index
        times += 1
        print(f"Frame {times} received")
        continue

    # Store data after preamble
    if pt < 256:
        pdata[int(pt / 16)][int(pt % 16)][times] = np.abs(value)
        pt += 1


import Visual
Visual.gen_anim(pdata,16,2.191,1000,1,120)
