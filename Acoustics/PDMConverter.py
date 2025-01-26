import numpy as np
from scipy.io.wavfile import write,read

def get_data(filename,channel,length):
    i=0
    j=0
    data=np.zeros((length))
    with open(filename, 'r') as file:
        line="  "

        while(line!=""):
            line=file.readline()
            if(line==""):
                break
            i+=1
            
            if(i%2!=channel):
                continue
            data[j]=int(line.strip())
            j+=1
    return data


samplerate=48000*64
duration=3

data= np.zeros((16,int(samplerate*(duration))))


length=int(samplerate*duration)
data[0]=get_data("./Acoustics/PDMTests/1/output_bit_1.txt",0,length)
print("Stream 1 Complete")
data[1]=get_data("./Acoustics/PDMTests/1/output_bit_1.txt",1,length)
print("Stream 2 Complete")
data[2]=get_data("./Acoustics/PDMTests/1/output_bit_2.txt",0,length)
print("Stream 3 Complete")
data[3]=get_data("./Acoustics/PDMTests/1/output_bit_2.txt",1,length)
print("Stream 4 Complete")
data[4]=get_data("./Acoustics/PDMTests/1/output_bit_3.txt",0,length)
print("Stream 5 Complete")
data[5]=get_data("./Acoustics/PDMTests/1/output_bit_3.txt",1,length)
print("Stream 6 Complete")
data[6]=get_data("./Acoustics/PDMTests/1/output_bit_4.txt",0,length)
print("Stream 7 Complete")
data[7]=get_data("./Acoustics/PDMTests/1/output_bit_4.txt",1,length)
print("Stream 8 Complete")
data[8]=get_data("./Acoustics/PDMTests/1/output_bit_8.txt",0,length)
print("Stream 9 Complete")
data[9]=get_data("./Acoustics/PDMTests/1/output_bit_8.txt",1,length)
print("Stream 10 Complete")
data[10]=get_data("./Acoustics/PDMTests/1/output_bit_9.txt",0,length)
print("Stream 11 Complete")
data[11]=get_data("./Acoustics/PDMTests/1/output_bit_9.txt",1,length)
print("Stream 12 Complete")
data[12]=get_data("./Acoustics/PDMTests/1/output_bit_10.txt",0,length)
print("Stream 13 Complete")
data[13]=get_data("./Acoustics/PDMTests/1/output_bit_10.txt",1,length)
print("Stream 14 Complete")
data[14]=get_data("./Acoustics/PDMTests/1/output_bit_11.txt",0,length)
print("Stream 15 Complete")
data[15]=get_data("./Acoustics/PDMTests/1/output_bit_11.txt",1,length)
print("Stream 16 Complete")
print("Data Collected")

import CICFilter as cic
outdata= np.zeros((16,int(samplerate/64*(duration))))
for i in range(16):
    outdata[i]=cic.cic(data[i])
    print("Channel"+str(i)+" Complete")

write("./Acoustics/PDMTests/1/channel.wav", 48000,outdata.T)
