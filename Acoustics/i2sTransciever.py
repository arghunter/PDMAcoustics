# so track lr clock and when it flip wait two and then process cic
import numpy as np
from scipy.io.wavfile import write,read
def get_data(filename, length):

    i = 0  # Track the bit index in the file
    j = 0  # Track the index in the output data array
    data = np.zeros((length,))
    
    with open(filename, 'r') as file:
        while j < length:  # Stop when the desired length is reached
            line = file.readline()
            if not line:  # End of file
                break
            
            # Extract data for the specified channel
            # if i % 2 == channel:  # Select bits based on DDR format
                
            data[j] = int(line.strip())  # Convert line to int and store in data
            if(data[j]==-1):
                data[j]=0
            j += 1  # Increment output index
            
            i += 1  # Increment bitdfasfasdfasdfadf index

    return data


samplerate=48000*64
duration=2

i2s= np.zeros((int(samplerate*(duration))))
lr_clk=np.zeros((int(samplerate*(duration))))


# print(False==False)
length=int(samplerate*duration)
# data[0]=get_data("./Acoustics/PDMTests/162/output_bit_1.txt",0,length)
# print("Stream 1 Complete")

# data[1]=get_data("./Acoustics/PDMTests/162/output_bit_1.txt",1,length)
# print("Stream 2 Complete")
# data[2]=get_data("./Acoustics/PDMTests/162/output_bit_2.txt",0,length)
# print("Stream 3 Complete")
# data[3]=get_data("./Acoustics/PDMTests/162/output_bit_2.txt",1,length)
# print("Stream 4 Complete")
# data[4]=get_data("./Acoustics/PDMTests/162/output_bit_3.txt",0,length)
# print("Stream 5 Complete")
# data[5]=get_data("./Acoustics/PDMTests/162/output_bit_3.txt",1,length)
# print("Stream 6 Complete")
# data[6]=get_data("./Acoustics/PDMTests/162/output_bit_4.txt",0,length)
# print("Stream 7 Complete")
# data[7]=get_data("./Acoustics/PDMTests/162/output_bit_4.txt",1,length)
# print("Stream 8 Complete")
# data[8]=get_data("./Acoustics/PDMTests/162/output_bit_8.txt",0,length)
# print("Stream 9 Complete")
# data[9]=get_data("./Acoustics/PDMTests/162/output_bit_8.txt",1,length)
# print("Stream 10 Complete")
# data[10]=get_data("./Acoustics/PDMTests/162/output_bit_9.txt",0,length)
# print("Stream 11 Complete")
# data[11]=get_data("./Acoustics/PDMTests/162/output_bit_9.txt",1,length)
# print("Stream 12 Complete")
lr_clk=get_data("./Acoustics/PDMTests/162/output_bit_10.txt",length)
print("Stream 13 Complete")
# data[13]=get_data("./Acoustics/PDMTests/162/output_bit_10.txt",1,length)
# print("Stream 14 Complete")
i2s=get_data("./Acoustics/PDMTests/162/output_bit_11.txt",length)
print("Stream 15 Complete")
cntr=get_data("./Acoustics/PDMTests/162/output_bit_12.txt",length)
print("Stream 16 Complete")
print("Data Collected")


outdata= np.zeros((int(samplerate/64*(duration))))

k=0
import time
sub_diff=2**32

t1=time.time()


bin_powers = 2**np.arange(31, -1, -1)  # Precompute powers of 2
pdata= np.zeros((16,16,50))
times=0
init_val=-1
p_cnt=-1
for i in range(1, len(lr_clk) - 34):
    if lr_clk[i] == 1 and lr_clk[i - 1] == 0:
        bin_val = i2s[i + 2 : i + 34]  # Extract binary values
        bin_int = np.dot(bin_val, bin_powers)
        if bin_val[0] == 1:
            bin_int -= sub_diff
        
        
        outdata[k] = np.abs(bin_int)
        bin_val = cntr[i + 2 : i + 34]  # Extract binary values
        bin_int = np.dot(bin_val, bin_powers)
        if bin_val[0] == 1:
            bin_int -= sub_diff
        bin_int+=128
        if bin_int==init_val and p_cnt!=bin_int:
            times+=1
        if(init_val==-1):
            init_val=bin_int
        
        p_cnt=bin_int
        # print(str(bin_int)+" "+str(int(bin_int/16))+" "+str(int(bin_int%16)))
        
        pdata[int(bin_int/16)][int(bin_int %16)][times]+=outdata[k]
        # if (k>1024):
        #     pdata[k]=outdata[k]-np.mean(outdata[k-1025:k-1])
        k += 1
print(time.time()-t1)
xdata=np.zeros((16,16,1))
for i in range(16):
    for j in range(16):
        for k in range(1,times):
            xdata[i,j,0]+=pdata[i,j,k]

print(pdata)

# print(pdata/np.max(pdata))
# pdata=np.log2(pdata)

# print(np.max(outdata))
print(np.mean(pdata))
print(np.max(pdata))
write("./Acoustics/PDMTests/162/channelbfri2sr.wav", 48000,outdata.T)
import Visual
Visual.gen_anim(pdata,16,2.162,162,1,120)