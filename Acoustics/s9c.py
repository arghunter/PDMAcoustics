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
    values = [0]
    hpvalues = [0,0]
    hpvalues2 = [0,0]
    hpvalues3 = [0,0]
    evalues=[0]
    zvalues = [0]
    a=0.5
    b=0.5
    c=0.995
    with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Sequence Number", "Value"])
        
        lines = [int(line.strip()) for line in infile]  # Read bytes as decimal values
        
        for i in range(0, len(lines) - 3, 4):  # Process in chunks of 4 bytes
            seq_num = lines[i]
            value = twos_complement_24bit(lines[i+1], lines[i+2], lines[i+3])
            csv_writer.writerow([seq_num, value])
            # e_avg=evalues[len(evalues)-1]+evalues[len(evalues)-2]+evalues[len(evalues)-3]+evalues[len(evalues)-4]+evalues[len(evalues)-5]+evalues[len(evalues)-6]+evalues[len(evalues)-7]+evalues[len(evalues)-8]
            hpvalues.append(hpvalues[len(hpvalues)-1]*a+(1)*(value-values[len(values)-1]))
            hpvalues2.append(hpvalues2[len(hpvalues2)-1]*a+(1)*(hpvalues[len(hpvalues)-1]-hpvalues[len(hpvalues)-2]))
            hpvalues3.append(hpvalues3[len(hpvalues3)-1]*a+(1)*(hpvalues2[len(hpvalues2)-1]-hpvalues2[len(hpvalues2)-2]))
            evalues.append(np.mean(evalues[len(evalues)-1])*b+(1-b)*np.abs(hpvalues[len(hpvalues)-1]))
            zvalues.append(np.mean(zvalues[len(zvalues)-1])*c+(1-c)*np.abs(evalues[len(evalues)-1]))
            values.append(value)
            
    
    # Normalize values to 16-bit PCM range (-32768 to 32767)
    hpvalues = np.array(hpvalues, dtype=np.float32)
    max_val = max(abs(hpvalues.min()), abs(hpvalues.max()))
    if max_val > 0:
        hpvalues = (hpvalues / max_val) * 32767
    hpvalues = hpvalues.astype(np.int16)
    
    
    hpvaluesbutter = np.array(hpvalues, dtype=np.float32)
    import scipy.signal as signal
    fs = 16000
    # Design a high-pass filter with a cutoff frequency of 400 Hz
    cutoff_freq = 500  # Cutoff frequency in Hz
    nyquist_rate = fs / 2.0  # Nyquist rate is half of the sampling rate
    normalized_cutoff = cutoff_freq / nyquist_rate

    # Butterworth high-pass filter
    b, a = signal.butter(2, normalized_cutoff, btype='high')

    # Apply the high-pass filter to the signal
    filtered_signal = signal.filtfilt(b, a, hpvaluesbutter)
    
    max_val = max(abs(filtered_signal.min()), abs(filtered_signal.max()))
    if max_val > 0:
        filtered_signal = (filtered_signal / max_val) * 32767
    filtered_signal = filtered_signal.astype(np.int16)
    
    
    
    values = np.array(values, dtype=np.float32)
    max_val = max(abs(values.min()), abs(values.max()))
    if max_val > 0:
        values = (values / max_val) * 32767
    values = values.astype(np.int16)
    
    evalues = np.array(evalues, dtype=np.float32)
    max_val = max(abs(evalues.min()), abs(evalues.max()))
    if max_val > 0:
        evalues = (evalues / max_val) * 32767
    evalues = evalues.astype(np.int16)
    
    zvalues = np.array(zvalues, dtype=np.float32)
    max_val = max(abs(zvalues.min()), abs(zvalues.max()))
    if max_val > 0:
        zvalues = (zvalues / max_val) * 32767
    zvalues = zvalues.astype(np.int16)
    
    hpvalues2 = np.array(hpvalues2, dtype=np.float32)
    max_val = max(abs(hpvalues2.min()), abs(hpvalues2.max()))
    if max_val > 0:
        hpvalues2 = (hpvalues2 / max_val) * 32767
    hpvalues2 = hpvalues2.astype(np.int16)
    
    hpvalues3 = np.array(hpvalues3, dtype=np.float32)
    max_val = max(abs(hpvalues3.min()), abs(hpvalues3.max()))
    if max_val > 0:
        hpvalues3 = (hpvalues3 / max_val) * 32767
    hpvalues3 = hpvalues3.astype(np.int16)
    
    
    
    
    # Save as WAV file
    with wave.open("1out"+wav_filename, 'w') as wavfile:
        wavfile.setnchannels(1)  # Mono
        wavfile.setsampwidth(2)  # 16-bit samples
        wavfile.setframerate(16000)  # Standard audio sample rate
        wavfile.writeframes(values.tobytes())
    with wave.open("1hpb"+wav_filename, 'w') as wavfile:
        wavfile.setnchannels(1)  # Mono
        wavfile.setsampwidth(2)  # 16-bit samples
        wavfile.setframerate(16000)  # Standard audio sample rate
        wavfile.writeframes(filtered_signal.tobytes())
    with wave.open("1hp22"+wav_filename, 'w') as wavfile:
        wavfile.setnchannels(1)  # Mono
        wavfile.setsampwidth(2)  # 16-bit samples
        wavfile.setframerate(16000)  # Standard audio sample rate
        wavfile.writeframes(hpvalues2.tobytes())
    with wave.open("1hp33"+wav_filename, 'w') as wavfile:
        wavfile.setnchannels(1)  # Mono
        wavfile.setsampwidth(2)  # 16-bit samples
        wavfile.setframerate(16000)  # Standard audio sample rate
        wavfile.writeframes(hpvalues3.tobytes())
    with wave.open("1hp"+wav_filename, 'w') as wavfile:
        wavfile.setnchannels(1)  # Mono
        wavfile.setsampwidth(2)  # 16-bit samples
        wavfile.setframerate(16000)  # Standard audio sample rate
        wavfile.writeframes(hpvalues.tobytes())
    with wave.open("1e"+wav_filename, 'w') as wavfile:
        wavfile.setnchannels(1)  # Mono
        wavfile.setsampwidth(2)  # 16-bit samples
        wavfile.setframerate(16000)  # Standard audio sample rate
        wavfile.writeframes(evalues.tobytes())
    with wave.open("1z"+wav_filename, 'w') as wavfile:
        wavfile.setnchannels(1)  # Mono
        wavfile.setsampwidth(2)  # 16-bit samples
        wavfile.setframerate(16000)  # Standard audio sample rate
        wavfile.writeframes(zvalues.tobytes())

    
    
if __name__ == "__main__":
    input_file = "output_pdm52.csv"  # Change this to your actual filename
    output_file = "output_53.csv"
    wav_file = "output134hp.wav"
    process_file(input_file, output_file, wav_file)
    print(f"Data saved to {output_file} and {wav_file}")