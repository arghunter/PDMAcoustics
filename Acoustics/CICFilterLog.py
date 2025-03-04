import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write, read
import soundfile as sf
import scipy

filename = "./bits3.txt"

def binary_to_decimal(binary_str):
    if binary_str[0] == '1':  # negative number
        inverted_str = ''.join('1' if b == '0' else '0' for b in binary_str)
        return -1 * (int(inverted_str, 2) + 1)
    else:
        return int(binary_str, 2)

def decimal_to_binary(decimal, bits=24):
    if decimal < 0:
        decimal = (1 << bits) + decimal
    return bin(decimal)[2:].zfill(bits)

def twos_complement_addition(bin1, bin2, bits=24):
    bin1, bin2 = bin1.zfill(bits), bin2.zfill(bits)
    dec1, dec2 = binary_to_decimal(bin1), binary_to_decimal(bin2)
    result_decimal = dec1 + dec2
    max_value = 1 << (bits - 1)
    min_value = -max_value
    if result_decimal >= max_value:
        result_decimal -= 2 * max_value
    elif result_decimal < min_value:
        result_decimal += 2 * max_value
    return decimal_to_binary(result_decimal, bits)

def binary_not(binary_str, bits=24):
    return ''.join('1' if b == '0' else '0' for b in binary_str.zfill(bits))

def twos_complement_subtraction(bin1, bin2, bits=24):
    bin2_not = binary_not(bin2, bits)
    bin2_neg = twos_complement_addition(bin2_not, '1'.zfill(bits), bits)
    return twos_complement_addition(bin1, bin2_neg, bits)

# Initialize values
int1 = int2 = int3 = dif1 = dif2 = dif3 = out = pdif1=pdif2=pdif3= "0"
counter = 0
out_array = []
in_array = []

# Open CSV file for writing
with open("output_log_cic.csv", mode="w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Iteration","data_in", "int1", "int2", "int3", "dif1", "dif2", "dif3", "out","64is"])

    with open(filename, 'r') as file:
        i = -1
        while True:
            line = file.readline()
            if not line:
                break
            i += 1
            if counter >= 64:
                
                out=dif3=twos_complement_subtraction(dif2,pdif3)
                pdif3=dif2
                dif2=twos_complement_subtraction(dif1,pdif2)
                pdif2=dif1
                dif1=twos_complement_subtraction(int3,pdif1)
                pdif1=int3
                
                
                # out = twos_complement_subtraction(twos_complement_subtraction(twos_complement_subtraction(int3, dif1), dif2), dif3)
                # dif3 = twos_complement_subtraction(twos_complement_subtraction(int3, dif1), dif2)
                # dif2 = twos_complement_subtraction(int3, dif1)
                # dif1 = int3
                counter = 0
                out_array.append(binary_to_decimal(out))
                print(binary_to_decimal(out))
            in_array.append(decimal_to_binary(int(line.strip())))
            int3 = twos_complement_addition(int2, int3)
            int2 = twos_complement_addition(int1, int2)
            int1 = twos_complement_addition(int1, decimal_to_binary(int(line)))
            
            

           
            greeting="bye"
            if(counter==0):
                    greeting="hello"
            # Log data to CSV
            csv_writer.writerow([i,int(line.strip()), binary_to_decimal(int1), binary_to_decimal(int2), binary_to_decimal(int3), 
                                 binary_to_decimal(dif1), binary_to_decimal(dif2), binary_to_decimal(dif3), binary_to_decimal(out), greeting])

            counter += 1

# Process and plot results
nparr = np.array(out_array, dtype=float)
nparr /= max(nparr)
print(np.sqrt(np.mean(nparr**2)))
write("cictest2048c.wav", 16000, nparr)

plt.plot(nparr[:2000])
plt.show()

# FFT Analysis
N = 4096
T = 1.0 / 48000.0
x = np.linspace(0.0, N*T, N)
y = nparr
yf = scipy.fftpack.fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

fig, ax = plt.subplots()
ax.plot(xf[:300], (2.0/N * np.abs(yf[:N//2]))[:300])
plt.show()
