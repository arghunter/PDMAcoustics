
import serial
import time

# Configure the serial port
SERIAL_PORT = 'COM9'  # Change this to your actual serial port (e.g., COM3 on Windows)
BAUD_RATE = 6000000  # Adjust to match your device's baud rate
OUTPUT_FILE = 'serial_output.txt'

def twos_complement_24bit(msb, mid, lsb):
    value = (msb << 16) | (mid << 8) | lsb
    if msb & 0x80:  # Check if the sign bit is set
        value -= 1 << 24  # Convert to negative value
    return value


def read_serial(port, baud_rate, output_file):
    try:
        with serial.Serial(port, baud_rate, timeout=1) as ser, open(output_file, 'w') as file:
            print(f"Reading from {port} at {baud_rate} baud... (Press Ctrl+C to stop)")
            expected_value = None
            start_time = time.time()
            bytes_received = 0

            while True:
                data = ser.read(ser.in_waiting or 1)  # Read available bytes
                bytes_received += len(data)
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    print(f"Bytes per second: {bytes_received / elapsed_time:.2f}", end='\r')
                
                if data:
                    int_values = [b for b in data]
                    i = 0
                    while i < len(int_values) - 3:
                        counter = int_values[i]
                        msb, mid, lsb = int_values[i + 1], int_values[i + 2], int_values[i + 3]
                        number = twos_complement_24bit(msb, mid, lsb)
                        
                        if expected_value is not None and counter != expected_value:
                            print(f"Discontinuity detected: Expected {expected_value}, but got {counter}")
                        expected_value = (counter + 1) % 256  # Wrap around at 255
                        
                        print(f"{counter} -> {number}", flush=True)
                        file.write(f"{counter} {number}\n")
                        i += 4
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    read_serial(SERIAL_PORT, BAUD_RATE, OUTPUT_FILE)
