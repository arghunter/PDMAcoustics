import serial

def read_serial_and_write_to_file(port, baudrate, output_file):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser, open(output_file, 'w') as file:
            print(f"Reading from {port} and writing to {output_file}...")
            while True:
                byte = ser.read(1)  # Read one byte
                if byte:
                    file.write(f"{int.from_bytes(byte, 'big')}\n")  # Write decimal representation of byte
                    file.flush()  # Ensure data is written immediately
                    print(int.from_bytes(byte, 'big'))  # Optional: Print to console
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Stopping...")

if __name__ == "__main__":
    port = "COM9"  # Change this to your serial port (e.g., "/dev/ttyUSB0" on Linux)
    baudrate = 3000000  # Adjust as needed
    output_file = "output_ser2.txt"
    read_serial_and_write_to_file(port, baudrate, output_file)
