#!/usr/bin/env python3
import serial
import time
import argparse
import csv
import numpy as np
from datetime import datetime

def receive_and_process_uart_data(port, baudrate=9600, timeout=1, output_file=None, num_words_to_print=180, visualize=True):
    """
    Receives data from the specified serial port, prints the first N words,
    then lets the user select a starting byte and processes the data.
    
    Args:
        port (str): Serial port name
        baudrate (int): Baud rate
        timeout (int): Serial timeout in seconds
        output_file (str): CSV file name
        num_words_to_print (int): Number of words to print before selecting start byte
        visualize (bool): Whether to generate visualization
    """
    # Generate default output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"uart_data_{timestamp}.csv"
    
    # Initialize data arrays and counters
    word_counter = 0
    words_data = []  # Store the first N words
    
    try:
        # Open the serial port
        ser = serial.Serial(port, baudrate, timeout=timeout)
        print(f"Connected to {port} at {baudrate} baud")
        
        # Open CSV file
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['packet_num', 'byte0', 'byte1', 'byte2', 'byte3', 'full_word']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Read first N words
            print(f"Reading first {num_words_to_print} words...")
            byte_position = 0
            current_word = {}
            
            while word_counter < num_words_to_print:
                # Read available bytes
                bytes_to_read = max(1, ser.in_waiting)
                data = ser.read(bytes_to_read)
                
                for byte in data:
                    # Process the byte based on its position
                    position = byte_position % 4
                    
                    if position == 0:
                        # Start of a new word
                        current_word = {'packet_num': word_counter, 'byte0': byte}
                        print(f"Word {word_counter}, Byte 0: {byte}", end=" | ")
                    elif position == 1:
                        current_word['byte1'] = byte
                        print(f"Byte 1: {byte}", end=" | ")
                    elif position == 2:
                        current_word['byte2'] = byte
                        print(f"Byte 2: {byte}", end=" | ")
                    elif position == 3:
                        current_word['byte3'] = byte
                        
                        # Calculate full word
                        full_word = (current_word['byte0'] << 24) | (current_word['byte1'] << 16) | \
                                  (current_word['byte2'] << 8) | byte
                        current_word['full_word'] = f"0x{full_word:08X}"
                        
                        # Write to CSV
                        writer.writerow(current_word)
                        csvfile.flush()
                        
                        # Store word data
                        words_data.append(current_word.copy())
                        
                        print(f"Byte 3: {byte} | Word: {current_word['full_word']}")
                        
                        word_counter += 1
                        if word_counter >= num_words_to_print:
                            break
                    
                    byte_position += 1
                
                # Small delay to prevent 100% CPU usage
                time.sleep(0.001)
            
            # Let user choose a starting byte
            print("\nFirst 180 words printed. Now select a byte position as the starting byte:")
            print("0: First byte of each word")
            print("1: Second byte of each word")
            print("2: Third byte of each word")
            print("3: Fourth byte of each word")
            
            starting_byte_pos = int(input("Enter your choice (0-3): "))
            
            # Initialize data structures
            # raw_pdata will store all values for each position
            raw_pdata = [[[] for _ in range(16)] for _ in range(16)]
            # uniform_pdata is a fixed-size array (for compatibility with your code)
            uniform_pdata = np.zeros((16, 16, 1000), dtype=np.int32)  # Assuming max 1000 occurrences
            counters = np.zeros((16, 16), dtype=np.int32)  # Count occurrences for each position
            
            # Process the already received words based on user's choice
            for word in words_data:
                pt = word[f'byte{starting_byte_pos}']  # The selected byte
                row = int(pt / 16)
                col = int(pt % 16)
                time_idx = counters[row][col]
                
                # Get next 3 bytes as 24-bit two's complement
                if starting_byte_pos == 0:
                    msb = word['byte1']
                    mid = word['byte2']
                    lsb = word['byte3']
                elif starting_byte_pos == 1:
                    msb = word['byte2']
                    mid = word['byte3']
                    lsb = word['byte0']
                elif starting_byte_pos == 2:
                    msb = word['byte3']
                    mid = word['byte0']
                    lsb = word['byte1']
                else:  # starting_byte_pos == 3
                    msb = word['byte0']
                    mid = word['byte1']
                    lsb = word['byte2']
                
                # Combine bytes into a 24-bit value
                value = (msb << 16) | (mid << 8) | lsb
                
                # Convert to two's complement if needed
                if value & 0x800000:  # Check if sign bit is set
                    value = value - 0x1000000
                
                # Store value in both data structures
                raw_pdata[row][col].append(value)
                if time_idx < uniform_pdata.shape[2]:
                    uniform_pdata[row][col][time_idx] = value
                counters[row][col] += 1
            
            print("\nContinuing to read and process data...")
            
            # Continue reading and processing data
            while True:
                # Read available bytes
                bytes_to_read = max(1, ser.in_waiting)
                data = ser.read(bytes_to_read)
                
                for byte in data:
                    # Process the byte based on its position
                    position = byte_position % 4
                    
                    if position == 0:
                        # Start of a new word
                        current_word = {'packet_num': word_counter, 'byte0': byte}
                    elif position == 1:
                        current_word['byte1'] = byte
                    elif position == 2:
                        current_word['byte2'] = byte
                    elif position == 3:
                        current_word['byte3'] = byte
                        
                        # Calculate full word
                        full_word = (current_word['byte0'] << 24) | (current_word['byte1'] << 16) | \
                                  (current_word['byte2'] << 8) | byte
                        current_word['full_word'] = f"0x{full_word:08X}"
                        
                        # Write to CSV
                        writer.writerow(current_word)
                        csvfile.flush()
                        
                        # Process data for pdata array
                        pt = current_word[f'byte{starting_byte_pos}']  # The selected byte
                        row = int(pt / 16)
                        col = int(pt % 16)
                        time_idx = counters[row][col]
                        
                        # Get next 3 bytes as 24-bit two's complement
                        if starting_byte_pos == 0:
                            msb = current_word['byte1']
                            mid = current_word['byte2']
                            lsb = current_word['byte3']
                        elif starting_byte_pos == 1:
                            msb = current_word['byte2']
                            mid = current_word['byte3']
                            lsb = current_word['byte0']
                        elif starting_byte_pos == 2:
                            msb = current_word['byte3']
                            mid = current_word['byte0']
                            lsb = current_word['byte1']
                        else:  # starting_byte_pos == 3
                            msb = current_word['byte0']
                            mid = current_word['byte1']
                            lsb = current_word['byte2']
                        
                        # Combine bytes into a 24-bit value
                        value = (msb << 16) | (mid << 8) | lsb
                        
                        # Convert to two's complement if needed
                        if value & 0x800000:  # Check if sign bit is set
                            value = value - 0x1000000
                        
                        # Store value in both data structures
                        raw_pdata[row][col].append(value)
                        if time_idx < uniform_pdata.shape[2]:
                            uniform_pdata[row][col][time_idx] = value
                        counters[row][col] += 1
                        
                        word_counter += 1
                        
                        # Print progress and update visualization every 1000 words
                        if word_counter % 1000 == 0:
                            print(f"Processed {word_counter} words")
                            
                            # Update visualization every 1000 words if enabled
                            if visualize:
                                try:
                                    update_visualization(raw_pdata)
                                except Exception as e:
                                    print(f"Visualization error: {e}")
                    
                    byte_position += 1
                
                # Small delay to prevent 100% CPU usage
                time.sleep(0.001)
                
    except KeyboardInterrupt:
        print("\nReceiver stopped by user")
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed")
        
        # Print summary
        print("\nReceived data summary:")
        print(f"Total words received: {word_counter}")
        print(f"Data saved to {output_file}")
        
        # Print occurrence statistics
        print("\nOccurrence statistics:")
        for row in range(16):
            for col in range(16):
                if counters[row][col] > 0:
                    print(f"Starting byte value {row*16+col} occurred {counters[row][col]} times")
        
        # Save pdata to file
        np.save('uniform_pdata.npy', uniform_pdata)
        print("\nProcessed data saved to uniform_pdata.npy")
        
        # Final visualization
        if visualize:
            try:
                update_visualization(raw_pdata, final=True)
            except Exception as e:
                print(f"Final visualization error: {e}")
        
        return uniform_pdata, raw_pdata, counters


def update_visualization(raw_pdata, final=False):
    """Create visualizations of the data including average energy heatmap"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec
        
        # Create a figure with 2 subplots (side by side)
        fig = plt.figure(figsize=(18, 8))
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
        
        # Calculate latest values
        latest_values = np.zeros((16, 16))
        for row in range(16):
            for col in range(16):
                if len(raw_pdata[row][col]) > 0:
                    latest_values[row, col] = raw_pdata[row][col][-1]
        
        # Calculate average energy (magnitude of values)
        avg_energy = np.zeros((16, 16))
        for row in range(16):
            for col in range(16):
                if len(raw_pdata[row][col]) > 0:
                    # Calculate average of absolute values to represent energy
                    avg_energy[row, col] = np.mean(np.abs(raw_pdata[row][col]))
        
        # First subplot: Latest values
        ax1 = plt.subplot(gs[0])
        im1 = ax1.imshow(latest_values, cmap='viridis')
        plt.colorbar(im1, ax=ax1, label='Value')
        ax1.set_title('Latest 24-bit Values')
        ax1.set_xlabel('Column')
        ax1.set_ylabel('Row')
        
        # Second subplot: Average energy
        ax2 = plt.subplot(gs[1])
        im2 = ax2.imshow(avg_energy, cmap='inferno')
        plt.colorbar(im2, ax=ax2, label='Average Energy (magnitude)')
        ax2.set_title('Average Signal Energy')
        ax2.set_xlabel('Column')
        ax2.set_ylabel('Row')
        
        plt.tight_layout()
        
        # Save the figure
        if final:
            plt.savefig('final_visualization.png')
        else:
            plt.savefig('current_visualization.png')
            
        # Show the plot if it's the final one
        if final:
            plt.show()
        else:
            plt.close()  # Close to avoid too many open figures
            
    except ImportError:
        print("Matplotlib not installed. Skipping visualization.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UART Receiver with data processing and visualization')
    parser.add_argument('port', help='Serial port (e.g., COM3 or /dev/ttyUSB0)')
    parser.add_argument('-b', '--baudrate', type=int, default=921600, 
                        help='Baud rate (default: 921600)')
    parser.add_argument('-t', '--timeout', type=int, default=1, 
                        help='Serial timeout in seconds (default: 1)')
    parser.add_argument('-o', '--output', help='Output CSV file')
    parser.add_argument('-n', '--num_words', type=int, default=2000,
                        help='Number of words to print before selecting start byte (default: 180)')
    parser.add_argument('--no-viz', action='store_true',
                        help='Disable visualization')
    
    args = parser.parse_args()
    
    try:
        receive_and_process_uart_data(args.port, args.baudrate, args.timeout, args.output, 
                                       args.num_words, not args.no_viz)
    except Exception as e:
        print(f"Error: {e}")