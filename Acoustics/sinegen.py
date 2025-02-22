import numpy as np
import wave
import struct

# Parameters
sample_rate = 16000  # Standard audio sample rate
frequency = 440.0  # Frequency of the sine wave (A4 note)
duration_on = 3  # 10 ms
duration_off = 3  # 20 ms
total_duration = 6.0  # 1 second total duration

# Generate wave and silence segments
samples_on = int(sample_rate * duration_on)
samples_off = int(sample_rate * duration_off)
num_repeats = int(total_duration / (duration_on + duration_off))

time = np.linspace(0, duration_on, samples_on, endpoint=False)
sine_wave = 0.5 * np.sin(2 * np.pi * frequency * time)  # Amplitude scaled to 0.5
silence = np.zeros(samples_off)

# Create one full cycle of sine + silence
segment = np.concatenate((sine_wave, silence))
import soundfile as sf
# Repeat the pattern for the total duration
# waveform_mono,sample_rate = sf.read("C:\\Users\\arg\\Documents\\Datasets\\dev-clean.tar\\dev-clean\\LibriSpeech\\dev-clean\\3000\\15664\\3000-15664-0008.flac")
# waveform_mono2,sample_rate2 = sf.read("C:\\Users\\arg\\Documents\\Datasets\\dev-clean.tar\\dev-clean\\LibriSpeech\\dev-clean\\3853\\163249\\3853-163249-0018.flac")
waveform_mono = 0.5 * np.sin(2 * np.pi * 1500 * time)
waveform_mono2= 0.5 * np.sin(2 * np.pi * 900 * time)
min_length = min(len(waveform_mono), len(waveform_mono2))
waveform_mono = waveform_mono[:min_length]
waveform_mono2 = waveform_mono2[:min_length]

# Stack the two mono channels into a stereo waveform
stereo_waveform = np.stack((waveform_mono, waveform_mono2), axis=-1)

# Save as a stereo WAV file
sf.write("output_stereo.wav", stereo_waveform, sample_rate)

print("Stereo WAV file created successfully!")
