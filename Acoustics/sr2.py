#!/usr/bin/env python3
import serial
import time
import argparse
import csv
from datetime import datetime

def receive_uart_data_to_csv(port, baudrate=9600, timeout=1, output_file=None):
    """
    Receives data from the specified serial port and writes to CSV.
    Implements a basic realignment strategy.
    
    Args:
        port (str): Serial port name
        baudrate (int): Baud rate
        timeout (int): Serial timeout in seconds
        output_file (str): CSV file name
    """
    # Generate default output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"uart_data_{timestamp}.csv"
    
    # Initialize data arrays and counters
    byte_arrays = [[], [], [], []]  # Arrays for each byte position
    word_counter = 0
    realignment_count = 0
    current_word = {}
    
    try:
        # Open the serial port
        ser = serial.Serial(port, baudrate, timeout=timeout)
        print(f"Connected to {port} at {baudrate} baud")
        print(f"Data will be saved to {output_file}")
        
        # Open CSV file
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['packet_num', 'byte0', 'byte1', 'byte2', 'byte3', 'full_word', 'realigned']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Read bytes until interrupted
            byte_position = 0
            last_bytes = [0, 0, 0, 0]  # Keep track of last 4 bytes
            
            while True:
                # Read available bytes
                bytes_to_read = max(1, ser.in_waiting)
                data = ser.read(bytes_to_read)
                
                for byte in data:
                    # Update last bytes buffer
                    last_bytes.pop(0)
                    last_bytes.append(byte)
                    
                    # Check for misalignment pattern after we have a full word
                    if byte_position % 4 == 3:
                        # If we see [4,1,2,3] instead of [1,2,3,4], we have a misalignment
                        if last_bytes == [4, 1, 2, 3]:
                            print(f"\nDetected misalignment at word {word_counter}")
                            # Adjust byte position to realign
                            byte_position = 1  # Set to position 1 as we've seen a "1" already
                            realignment_count += 1
                            current_word = {'packet_num': word_counter, 'byte0': 1, 'realigned': True}
                            byte_arrays[0].append(1)
                            continue
                    
                    # Process the byte based on its position
                    position = byte_position % 4
                    byte_arrays[position].append(byte)
                    
                    if position == 0:
                        # Start of a new word
                        current_word = {'packet_num': word_counter, 'byte0': byte, 'realigned': False}
                        print(f"Byte 0: {byte}", end=" | ")
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
                        
                        print(f"Byte 3: {byte} | Word: {current_word['full_word']}")
                        
                        # Check if next sequence might be problematic (detect the unusual [4,1,2,4] pattern)
                        if byte == 4 and ser.in_waiting >= 3:
                            peek = ser.read(3)
                            if list(peek) == [1, 2, 4]:
                                print("\nDetected unusual [4,1,2,4] pattern - skipping a byte")
                                ser.read(1)  # Skip one byte
                                realignment_count += 1
                            # Put the peeked bytes back into the stream processing
                            data = peek + ser.read(bytes_to_read - 3)
                        
                        word_counter += 1
                    
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
        print(f"Realignments performed: {realignment_count}")
        print(f"Data saved to {output_file}")
        
        return byte_arrays


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UART Receiver for 32-bit data')
    parser.add_argument('port', help='Serial port (e.g., COM3 or /dev/ttyUSB0)', default="COM9")
    parser.add_argument('-b', '--baudrate', type=int, default=3000000, 
                        help='Baud rate (default: 921600)')
    parser.add_argument('-t', '--timeout', type=int, default=1, 
                        help='Serial timeout in seconds (default: 1)')
    parser.add_argument('-o', '--output', help='Output CSV file')
    
    args = parser.parse_args()
    
    try:
        receive_uart_data_to_csv(args.port, args.baudrate, args.timeout, args.output)
    except Exception as e:
        print(f"Error: {e}")