import sounddevice as sd
import wave
import numpy as np

def play_wav(filename):
    # Open the WAV file
    with wave.open(filename, 'rb') as wf:
        sample_rate = wf.getframerate()
        num_channels = wf.getnchannels()
        num_frames = wf.getnframes()
        
        # Read and convert data to NumPy array
        audio_data = np.frombuffer(wf.readframes(num_frames), dtype=np.int16)
        
        # If stereo, reshape the data
        if num_channels > 1:
            audio_data = audio_data.reshape(-1, num_channels)
        
        # Play audio
        sd.play(audio_data, samplerate=sample_rate)
        sd.wait()

# Example usage
play_wav("sine_wave_pattern.wav")