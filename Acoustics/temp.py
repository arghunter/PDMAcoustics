import numpy as np

def estimate_pdm_energy(pdm_signal, window_size):
    """
    Estimate the energy of a PDM bitstream without full PCM reconstruction.
    
    Args:
        pdm_signal (numpy array): Binary PDM bitstream (array of 0s and 1s).
        window_size (int): Number of samples per energy estimation window.
    
    Returns:
        energy_values (numpy array): Estimated energy values over time.
    """
    # Convert PDM {0,1} to {-1,1} for zero-mean assumption
    pdm_centered = 2 * pdm_signal - 1  
    
    # Compute the running sum over window_size
    print(pdm_centered)
    energy_values = np.convolve(pdm_centered, np.ones(window_size), mode='valid') 
    
    # Square the values to get energy
    energy_values = energy_values ** 2  
    
    return energy_values

# Example usage:
np.random.seed(42)  # For reproducibility
pdm_stream = np.random.choice([0, 1], size=10000, p=[0.5, 0.5])  # Simulated PDM signal
window_size = 64  # Choose a reasonable window size
energy_estimates = estimate_pdm_energy(pdm_stream, window_size)

# Print first few values
print(energy_estimates[:10])

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
                # data[j]=v
                if(v==-1):
                    data[j]=0
                else:
                    data[j]=1
                j += 1  # Increment output index
            
            i += 1  # Increment bit index

    return data




samplerate=48000*64
duration=2

data= np.zeros((16,int(samplerate*(duration))))


# print(False==False)
length=int(samplerate*duration)
data[0]=get_data("./Acoustics/PDMTests/171/output_bit_1.txt",1,length)

print("Stream 1 Complete")

energy_estimates = estimate_pdm_energy(data[0], 128)
import matplotlib.pyplot as plt

# # Print first few values
# for i in range(len(energy_estimates)):
#     print(energy_estimates[i])
plt.figure(figsize=(10, 5))
plt.plot(energy_estimates, label="Estimated Energy", color='b')
plt.xlabel("Time (samples)")
plt.ylabel("Energy Estimate")
plt.title("PDM Energy Estimation Over Time")
plt.legend()
plt.grid(True)
plt.show()