import numpy as np
import wave
import struct

# Parameters
sample_rate = 48000  # Standard audio sample rate
frequency = 5000  # Frequency of the sine wave (A4 note)
duration_on = 0.01  # 10 ms
duration_off = 0.02  # 20 ms
total_duration = 2.0  # 1 second total duration

# Generate wave and silence segments
samples_on = int(sample_rate * duration_on)
samples_off = int(sample_rate * duration_off)
num_repeats = int(total_duration / (duration_on + duration_off))

time = np.linspace(0, duration_on, samples_on, endpoint=False)
sine_wave = 0.5 * np.sin(2 * np.pi * frequency * time)  # Amplitude scaled to 0.5
silence = np.zeros(samples_off)

# Create one full cycle of sine + silence
segment = np.concatenate((sine_wave, silence))

# Repeat the pattern for the total duration
waveform = np.tile(segment, num_repeats)

# Convert to 16-bit PCM format
waveform_int16 = np.int16(waveform * 32767)

# Write to a WAV file
output_file = "sine_wave_pattern.wav"
with wave.open(output_file, "w") as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16-bit PCM
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(struct.pack("<" + "h" * len(waveform_int16), *waveform_int16))

print(f"WAV file generated: {output_file}")
