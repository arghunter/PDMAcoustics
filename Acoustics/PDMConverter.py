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


# print(False==False)
length=int(samplerate*duration)
data[0]=get_data("./Acoustics/PDMTests/115/output_bit_1.txt",0,length)
print("Stream 1 Complete")

data[1]=get_data("./Acoustics/PDMTests/115/output_bit_1.txt",1,length)
print("Stream 2 Complete")
data[2]=get_data("./Acoustics/PDMTests/115/output_bit_2.txt",0,length)
print("Stream 3 Complete")
data[3]=get_data("./Acoustics/PDMTests/115/output_bit_2.txt",1,length)
print("Stream 4 Complete")
data[4]=get_data("./Acoustics/PDMTests/115/output_bit_3.txt",0,length)
print("Stream 5 Complete")
data[5]=get_data("./Acoustics/PDMTests/115/output_bit_3.txt",1,length)
print("Stream 6 Complete")
data[6]=get_data("./Acoustics/PDMTests/115/output_bit_4.txt",0,length)
print("Stream 7 Complete")
data[7]=get_data("./Acoustics/PDMTests/115/output_bit_4.txt",1,length)
print("Stream 8 Complete")
data[8]=get_data("./Acoustics/PDMTests/115/output_bit_8.txt",0,length)
print("Stream 9 Complete")
data[9]=get_data("./Acoustics/PDMTests/115/output_bit_8.txt",1,length)
print("Stream 10 Complete")
data[10]=get_data("./Acoustics/PDMTests/115/output_bit_9.txt",0,length)
print("Stream 11 Complete")
data[11]=get_data("./Acoustics/PDMTests/115/output_bit_9.txt",1,length)
print("Stream 12 Complete")
data[12]=get_data("./Acoustics/PDMTests/115/output_bit_10.txt",0,length)
print("Stream 13 Complete")
data[13]=get_data("./Acoustics/PDMTests/115/output_bit_10.txt",1,length)
print("Stream 14 Complete")
data[14]=get_data("./Acoustics/PDMTests/115/output_bit_11.txt",0,length)
print("Stream 15 Complete")
data[15]=get_data("./Acoustics/PDMTests/115/output_bit_11.txt",1,length)
print("Stream 16 Complete")
print("Data Collected")
data1= np.zeros((16,int(samplerate*(duration))))
# data1[0]=get_data("./Acoustics/PDMTests/63/output_bit_1.txt",0,length)
# print("Stream 1 Complete")
# data1[1]=get_data("./Acoustics/PDMTests/63/output_bit_1.txt",1,length)
# print("Stream 2 Complete")
# data1[2]=get_data("./Acoustics/PDMTests/63/output_bit_2.txt",0,length)
# print("Stream 3 Complete")
# data1[3]=get_data("./Acoustics/PDMTests/63/output_bit_2.txt",1,length)
# print("Stream 4 Complete")
# data1[4]=get_data("./Acoustics/PDMTests/63/output_bit_3.txt",0,length)
# print("Stream 5 Complete")
# data1[5]=get_data("./Acoustics/PDMTests/63/output_bit_3.txt",1,length)
# print("Stream 6 Complete")
# data1[6]=get_data("./Acoustics/PDMTests/63/output_bit_4.txt",0,length)
# print("Stream 7 Complete")
# data1[7]=get_data("./Acoustics/PDMTests/63/output_bit_4.txt",1,length)
# print("Stream 8 Complete")
# data1[8]=get_data("./Acoustics/PDMTests/63/output_bit_8.txt",0,length)
# print("Stream 9 Complete")
# data1[9]=get_data("./Acoustics/PDMTests/63/output_bit_8.txt",1,length)
# print("Stream 10 Complete")
# data1[10]=get_data("./Acoustics/PDMTests/63/output_bit_9.txt",0,length)
# print("Stream 11 Complete")
# data1[11]=get_data("./Acoustics/PDMTests/63/output_bit_9.txt",1,length)
# print("Stream 12 Complete")
# data1[12]=get_data("./Acoustics/PDMTests/63/output_bit_10.txt",0,length)
# print("Stream 13 Complete")
# data1[13]=get_data("./Acoustics/PDMTests/63/output_bit_10.txt",1,length)
# print("Stream 14 Complete")
# data1[14]=get_data("./Acoustics/PDMTests/63/output_bit_11.txt",0,length)
# print("Stream 15 Complete")
# data1[15]=get_data("./Acoustics/PDMTests/63/output_bit_11.txt",1,length)
print("Stream 16 Complete")
print("Data Collected")
import CICFilter as cic
outdata= np.zeros((16,int(samplerate/64*(duration))))
for i in range(16):
    data[i]+=-data1[i]
    if data[i][0]!=0:
        outdata[i]=cic.cic(data[i])
    print("Channel"+str(i)+" Complete")
outdata/=np.max(outdata)
write("./Acoustics/PDMTests/115/channel1.wav", 48000,outdata.T)
