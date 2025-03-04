import csv

import csv

def twos_complement_24bit(msb, mid, lsb):
    """Convert 3 bytes (MSB, MID, LSB) to a signed 24-bit integer."""
    value = (msb << 16) | (mid << 8) | lsb
    if value & 0x800000:  # Check if the sign bit is set
        value -= 0x1000000  # Convert to negative
    return value

def process_file(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Sequence Number", "Value"])
        
        lines = [int(line.strip()) for line in infile]  # Read bytes as decimal values
        
        for i in range(0, len(lines) - 3, 4):  # Process in chunks of 4 bytes
            seq_num = lines[i]
            value = twos_complement_24bit(lines[i+1], lines[i+2], lines[i+3])
            csv_writer.writerow([seq_num, value])
    
if __name__ == "__main__":
    input_file = "output_ser.csv"  # Change this to your actual filename
    output_file = "output_2.csv"
    process_file(input_file, output_file)
    print(f"Data saved to {output_file}")
