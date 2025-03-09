import csv
import wave
import numpy as np

def twos_complement_24bit(msb, mid, lsb):
    """Convert 3 bytes (MSB, MID, LSB) to a signed 24-bit integer."""
    value = (msb << 16) | (mid << 8) | lsb
    if value & 0x800000:  # Check if the sign bit is set
        value -= 0x1000000  # Convert to negative
    return value

def process_file(input_filename, output_filename, wav_filename):
    values = []
    with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Sequence Number", "Value"])
        
        lines = [int(line.strip()) for line in infile]  # Read bytes as decimal values
        
        for i in range(0, len(lines) - 3, 4):  # Process in chunks of 4 bytes
            seq_num = lines[i]
            value = twos_complement_24bit(lines[i+1], lines[i+2], lines[i+3])
            csv_writer.writerow([seq_num, value])
            values.append(value)
    
    # Normalize values to 16-bit PCM range (-32768 to 32767)
    values = np.array(values, dtype=np.float32)
    print(np.average(np.abs(values)))
    max_val = max(abs(values.min()), abs(values.max()))
    if max_val > 0:
        values = (values / max_val) * 32767
    values = values.astype(np.int16)
    
    # Save as WAV file
    with wave.open(wav_filename, 'w') as wavfile:
        wavfile.setnchannels(1)  # Mono
        wavfile.setsampwidth(2)  # 16-bit samples
        wavfile.setframerate(16000)  # Standard audio sample rate
        wavfile.writeframes(values.tobytes())
    


    
    
if __name__ == "__main__":
    input_file = "output_pixel87.csv"  # Change this to your actual filename
    output_file = "output_87.csv"
    wav_file = "output167.wav"
    process_file(input_file, output_file, wav_file)
    print(f"Data saved to {output_file} and {wav_file}")