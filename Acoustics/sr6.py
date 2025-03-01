import serial
import time

# Configure the serial port
SERIAL_PORT = 'COM9'  # Change this to your actual serial port (e.g., COM3 on Windows)
BAUD_RATE = 3000000  # Adjust to match your device's baud rate
OUTPUT_FILE = 'serial_output.txt'

def read_serial(port, baud_rate, output_file):
    try:
        with serial.Serial(port, baud_rate, timeout=1) as ser, open(output_file, 'w') as file:
            print(f"Reading from {port} at {baud_rate} baud... (Press Ctrl+C to stop)")
            expected_value = None
            start_time = time.time()
            total_bytes = 0
            while True:
                data = ser.read(ser.in_waiting or 1)  # Read available bytes
                if data:
                    int_values = [b for b in data]
                    total_bytes += len(int_values)
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 0:
                        bps = total_bytes / elapsed_time
                        print(f"Bytes per second: {bps:.2f}", end='\r')
                    for value in int_values:
                        if expected_value is not None and value != expected_value:
                            print(f"Discontinuity detected: Expected {expected_value}, but got {value}")
                        expected_value = (value + 1) % 256  # Wrap around at 255
                    # print(" ".join(map(str, int_values)), flush=True)
                    file.write(" ".join(map(str, int_values)) + "\n")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_serial(SERIAL_PORT, BAUD_RATE, OUTPUT_FILE)

