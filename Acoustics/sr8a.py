import serial
import csv

def read_serial_and_write_csv(port, baudrate, output_file):
    ser = serial.Serial(port, baudrate, timeout=1)
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        while True:
            data = ser.read(4)  # Read 4 bytes
            if len(data) < 4:
                continue  # Ignore incomplete reads
            
            # writer.writerow([data[0], data[1], data[2], data[3]])
            writer.writerow([data[0]])
            writer.writerow([data[1]])
            writer.writerow([data[2]])
            writer.writerow([data[3]])
            csvfile.flush()  # Ensure data is written to file

if __name__ == "__main__":
    port = "COM9"  # Change this to match your system
    baudrate = 3000000
    output_file = "output_pixel82.csv"
    
    try:
        read_serial_and_write_csv(port, baudrate, output_file)
    except KeyboardInterrupt:
        print("Stopped by user.")
