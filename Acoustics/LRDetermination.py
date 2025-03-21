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
                data[j] = int(line.strip())  # Convert line to int and store in data
                j += 1  # Increment output index
            
            i += 1  # Increment bit index

    return data



samplerate=48000*64
duration=2

data= np.zeros((16,int(samplerate*(duration))))

print(False==False)
length=int(samplerate*duration)
data[0]=get_data("./Acoustics/PDMTests/54/output_bit_1.txt",0,length)
print("Stream 1 Complete")
# with open("./Acoustics/PDMTests/17/output_bit_1_sdr.txt", 'w') as file:
#     for integer in data[0]:
#         file.write(f"{integer}\n")
data[1]=get_data("./Acoustics/PDMTests/54/output_bit_1.txt",1,length)
print("Stream 2 Complete")
data[2]=get_data("./Acoustics/PDMTests/54/output_bit_2.txt",0,length)
print("Stream 3 Complete")
data[3]=get_data("./Acoustics/PDMTests/54/output_bit_2.txt",1,length)
print("Stream 4 Complete")
data[4]=get_data("./Acoustics/PDMTests/54/output_bit_3.txt",0,length)
print("Stream 5 Complete")
data[5]=get_data("./Acoustics/PDMTests/54/output_bit_3.txt",1,length)
print("Stream 6 Complete")
data[6]=get_data("./Acoustics/PDMTests/54/output_bit_4.txt",0,length)
print("Stream 7 Complete")
data[7]=get_data("./Acoustics/PDMTests/54/output_bit_4.txt",1,length)
print("Stream 8 Complete")
data[8]=get_data("./Acoustics/PDMTests/54/output_bit_8.txt",0,length)
print("Stream 9 Complete")
data[9]=get_data("./Acoustics/PDMTests/54/output_bit_8.txt",1,length)
print("Stream 10 Complete")
data[10]=get_data("./Acoustics/PDMTests/54/output_bit_9.txt",0,length)
print("Stream 11 Complete")
data[11]=get_data("./Acoustics/PDMTests/54/output_bit_9.txt",1,length)
print("Stream 12 Complete")
data[12]=get_data("./Acoustics/PDMTests/54/output_bit_10.txt",0,length)
print("Stream 13 Complete")
data[13]=get_data("./Acoustics/PDMTests/54/output_bit_10.txt",1,length)
print("Stream 14 Complete")
data[14]=get_data("./Acoustics/PDMTests/54/output_bit_11.txt",0,length)
print("Stream 15 Complete")
data[15]=get_data("./Acoustics/PDMTests/54/output_bit_11.txt",1,length)
print("Stream 16 Complete")
print("Data Collected")

import CICFilter as cic
outdata= np.zeros((16))
for i in range(16):
    outdata[i]=np.mean(data[i][0:2048])
    print("Channel"+str(i)+" Complete")
# outdata/=np.max(outdata)
print(outdata)
# write("./Acoustics/PDMTests/54/channel.wav", 48000,outdata.T)
