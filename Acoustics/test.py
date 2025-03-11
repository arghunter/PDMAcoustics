

import DataGatherer
import numpy as np


spacing=np.array([[-0.06,-0.24,0],[-0.18,-0.24,0],[-0.06,-0.12,0],[-0.18,-0.12,0],[-0.06,0,0],[-0.18,0,0],[-0.06,0.12,0],[-0.18,0.12,0],[0.18,-0.24,0],[0.06,-0.24,0],[0.18,-0.12,0],[0.06,-0.12,0],[0.18,0,0],[0.06,0,0],[0.18,0.12,0],[0.06,0.12,0]])
testNum=185
n_channels=16
samplerate=48000*64
duration=2
subduration=2
segments=16
fov=180
data=DataGatherer.get_multi_channel_data(testNum,samplerate,duration,subduration)

import numpy as np
import matplotlib.pyplot as plt

def sliding_xor_sum(a, b):
    """Computes the sliding XOR operation and sums the XOR results at each shift."""
    len_a, len_b = len(a), len(b)
    result_length = len_a + len_b - 1
    shifts = np.arange(-len_a + 1, len_b)  # Shift indices
    result = np.zeros(result_length, dtype=int)
    
    # Pad 'b' with zeros to slide across 'a'
    b_padded = np.pad(b, (len_a - 1, len_a - 1), mode='constant', constant_values=0)
    
    # Perform point-by-point XOR at each shift and sum the results
    for i in range(result_length):
        print(i)
        shifted_b = b_padded[i:i+len_a]  # Take a sliding window of 'b'
        xor_values = a ^ shifted_b       # Element-wise XOR
        result[i] = np.sum(xor_values)   # Sum of XOR results
    
    return shifts, result

# Example Usage
a = data[1]
b = data[3]

shifts, xor_sum_result = sliding_xor_sum(a, b)

# Save to CSV
data = np.column_stack((shifts, xor_sum_result))
np.savetxt("xor_result.csv", data, delimiter=",", fmt="%d", header="Shift,XOR_Sum", comments="")

# Plotting
plt.figure(figsize=(8, 4))
plt.plot(shifts, xor_sum_result, marker='o', linestyle='-', color='b', label="XOR Sum")
plt.xlabel("Shift")
plt.ylabel("Sum of XORs")
plt.title("Sliding XOR Sum vs. Shift")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.show()

print("Saved to xor_result.csv and plotted successfully!")




