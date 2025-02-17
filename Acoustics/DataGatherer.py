import numpy as np
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

            if(i%2==channel):
                continue
            data[j]=int(line.strip())
            j+=1
    return data





def get_multi_channel_data(testNum,samplerate,duration,subduration):
    data= np.zeros((16,int(samplerate*(subduration))))
    length=int(samplerate*duration)
    data[0]=(get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_1.txt",0,length))[0:int(samplerate*subduration)]
    print("Stream 1 Complete")
    data[1]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_1.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 2 Complete")
    data[2]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_2.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 3 Complete")
    data[3]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_2.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 4 Complete")
    data[4]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_3.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 5 Complete")
    data[5]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_3.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 6 Complete")
    data[6]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_4.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 7 Complete")
    data[7]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_4.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 8 Complete")
    data[8]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_8.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 9 Complete")
    data[9]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_8.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 10 Complete")
    data[10]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_9.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 11 Complete")
    data[11]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_9.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 12 Complete")
    data[12]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_10.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 13 Complete")
    data[13]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_10.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 14 Complete")
    data[14]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_11.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 15 Complete")
    data[15]=get_data("./Acoustics/PDMTests/"+str(testNum)+"/output_bit_11.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 16 Complete")
    print("Data Collected")
    data1= np.zeros((16,int(samplerate*(subduration))))
    data1[0]=get_data("./Acoustics/PDMTests/63/output_bit_1.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 1 Complete")
    data1[1]=get_data("./Acoustics/PDMTests/63/output_bit_1.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 2 Complete")
    data1[2]=get_data("./Acoustics/PDMTests/63/output_bit_2.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 3 Complete")
    data1[3]=get_data("./Acoustics/PDMTests/63/output_bit_2.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 4 Complete")
    data1[4]=get_data("./Acoustics/PDMTests/63/output_bit_3.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 5 Complete")
    data1[5]=get_data("./Acoustics/PDMTests/63/output_bit_3.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 6 Complete")
    data1[6]=get_data("./Acoustics/PDMTests/63/output_bit_4.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 7 Complete")
    data1[7]=get_data("./Acoustics/PDMTests/63/output_bit_4.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 8 Complete")
    data1[8]=get_data("./Acoustics/PDMTests/63/output_bit_8.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 9 Complete")
    data1[9]=get_data("./Acoustics/PDMTests/63/output_bit_8.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 10 Complete")
    data1[10]=get_data("./Acoustics/PDMTests/63/output_bit_9.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 11 Complete")
    data1[11]=get_data("./Acoustics/PDMTests/63/output_bit_9.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 12 Complete")
    data1[12]=get_data("./Acoustics/PDMTests/63/output_bit_10.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 13 Complete")
    data1[13]=get_data("./Acoustics/PDMTests/63/output_bit_10.txt",1,length)[0:int(samplerate*subduration)]
    print("Stream 14 Complete")
    data1[14]=get_data("./Acoustics/PDMTests/63/output_bit_11.txt",0,length)[0:int(samplerate*subduration)]
    print("Stream 15 Complete")
    data1[15]=get_data("./Acoustics/PDMTests/63/output_bit_11.txt",1,length)[0:int(samplerate*subduration)]
    for i in range(16):
        data[i]+=-data1[i]
    return data