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
            
            if(i%2!=channel):
                continue
            data[j]=int(line.strip())
            j+=1
    return data
            