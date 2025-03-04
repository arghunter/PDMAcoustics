def bytes_to_bits(input_file, output_file):
    with open(input_file, "r") as f:
        byte_values = [int(line.strip()) for line in f if line.strip().isdigit()]
    
    with open(output_file, "w") as f:
        for byte in byte_values:
            bits = format(byte, '08b')  # Convert byte to 8-bit binary string
            for bit in bits:
                f.write("1\n" if bit == "1" else "-1\n")

if __name__ == "__main__":
    input_filename = "output_pdm27.csv"  # Change as needed
    output_filename = "bits3.txt"  # Change as needed
    bytes_to_bits(input_filename, output_filename)
    print(f"Converted bits written to {output_filename}")