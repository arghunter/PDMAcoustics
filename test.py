import numpy as np

def get_data(filename, channel, length):
    """
    Extracts channel-specific PDM data from a DDR bitstream.
    
    Parameters:
        filename (str): The name of the file containing the DDR bitstream.
        channel (int): The channel to extract (0 for first channel, 1 for second channel).
        length (int): The maximum number of samples to extract.
    
    Returns:
        np.ndarray: Extracted data for the specified channel.
    """
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

channel_0_data = get_data("pdm_data.txt", channel=0, length=4)
print(channel_0_data)  # Output: [1.  1. -1.  1.]
channel_1_data = get_data("pdm_data.txt", channel=1, length=4)
print(channel_1_data)  # Output: [-1.  1. -1. -1.]
