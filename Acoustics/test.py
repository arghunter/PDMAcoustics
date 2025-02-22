import numpy as np

import numpy as np
from scipy.io.wavfile import write,read

import numpy as np

def get_data(filename, channel, length):

    i = 0  # Track the bit index in the file
    j = 0  # Track the index in the output data array
    data = np.zeros((length,))
    
    with open(filename, 'r') as file:
        while j < length:  # Stop when the desired length is reached
            line = file.readline()
            if not line:  # End of file
                break
            
            # Extract data for the specified channel
            if i % 2 == channel:  # Select bits based on DDR format
                
                v=int(line.strip())  # Convert line to int and store in data
                data[j]=v
                # if(v==-1):
                #     data[j]=0
                # else:
                #     data[j]=1
                j += 1  # Increment output index
            
            i += 1  # Increment bit index

    return data




samplerate=48000*64
duration=2

data= np.zeros((16,int(samplerate*(duration))))


# print(False==False)
length=int(samplerate*duration)
data[0]=get_data("./Acoustics/PDMTests/56/output_bit_1.txt",0,length)

print("Stream 1 Complete")


# length = 10  # Change to your actual length
# data = np.random.randint(0, 2, (16, length), dtype=np.uint8)  # Binary data (0s and 1s)
# d1=np.zeros((16,length),dtype=np.uint8)
# d1r=np.random.randint(0, 2, (length), dtype=np.uint8)
for i in range(16):
    data[i] = np.roll(data[0],3000*i)
# data=d1
print(data)
# Perform XOR across each row (channel)
xor_results = np.zeros(length)
for i in range(length):
    xor_results[i]=(data[0][i]+data[1][i]+data[2][i]+data[3][i]+data[4][i]+data[5][i]+data[6][i]+data[7][i]+data[8][i]+data[9][i]+data[10][i]+data[11][i]+data[12][i]+data[13][i]+data[14][i]+data[15][i])**2
    # xor_results[i]=(data[0][i]^data[1][i])
print(xor_results)
print(np.sum(xor_results))
