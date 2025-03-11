

import DataGatherer
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
spacing=np.array([[-0.06,-0.24,0],[-0.18,-0.24,0],[-0.06,-0.12,0],[-0.18,-0.12,0],[-0.06,0,0],[-0.18,0,0],[-0.06,0.12,0],[-0.18,0.12,0],[0.18,-0.24,0],[0.06,-0.24,0],[0.18,-0.12,0],[0.06,-0.12,0],[0.18,0,0],[0.06,0,0],[0.18,0.12,0],[0.06,0.12,0]])
testNum=185
n_channels=16
samplerate=48000*64
duration=2
subduration=2
segments=16
fov=180
data=DataGatherer.get_multi_channel_data(testNum,samplerate,duration,subduration)
speech,samplerate=sf.read(("C:/Users/arg/Documents/GitHub/PDMAcoustics/Acoustics/PDMTests/185/data.wav"))
data=data[0]+data[1]+data[2]+data[3]+data[4]+data[5]+data[6]+data[7]+data[8]+data[9]+data[10]+data[11]+data[12]+data[13]+data[14]+data[15]
signal = data
fs = 3.072*10**6  
N = len(signal)
fft_output = np.fft.fft(signal)
freqs = np.fft.fftfreq(N, 1/fs)


plt.figure(figsize=(8, 4))
plt.plot(freqs[1:N//2], np.abs(fft_output[1:N//2]) * 2 / N)  # Normalize and plot positive frequencies
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("FFT of the Beamformed PDM")
plt.grid()
import CICFilter as cic

outdatapcm=cic.cic(signal)

speech=speech.T[0]+speech.T[1]+speech.T[2]+speech.T[3]+speech.T[4]+speech.T[5]+speech.T[6]+speech.T[7]+speech.T[8]+speech.T[9]+speech.T[10]+speech.T[11]+speech.T[12]+speech.T[13]+speech.T[14]+speech.T[15]
fs = 48000
N = len(speech)
fft_output = np.fft.fft(speech)
freqs = np.fft.fftfreq(N, 1/fs)
print(freqs)

plt.figure(figsize=(8, 4))
plt.plot(freqs[1:N//2], np.abs(fft_output[1:N//2]) * 2 / N)  # Normalize and plot positive frequencies
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("FFT of the Beamformed PCM")
plt.grid()



outdatapcm=cic.cic(signal)
fs = samplerate
N = len(outdatapcm)
fft_output = np.fft.fft(outdatapcm)
freqs = np.fft.fftfreq(N, 1/fs)
plt.figure(figsize=(8, 4))
plt.plot(freqs[1:N//2], np.abs(fft_output[1:N//2]) * 2 / N)  # Normalize and plot positive frequencies
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("FFT of the Beamformed PDM post PCM Conversion")
plt.grid()
plt.show()
plt.show()
plt.show()
