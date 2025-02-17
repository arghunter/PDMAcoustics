import numpy as np

from Preprocessor import Preprocessor
from time import time
import sounddevice as sd
from scipy import signal
from DelayApproximation import DelayAproximator
from IOStream import IOStream
from VAD import VAD
v=340.3 # speed of sound at sea level m/s

class Beamformer:
    def __init__(self,n_channels=8,coord=np.array([[-0.08,0.042],[-0.08,0.014],[-0.08,-0.028],[-0.08,-0.042],[0.08,0.042],[0.08,0.014],[0.08,-0.028],[0.08,-0.042]]),sample_rate=48000):
        self.n_channels = n_channels
        self.coord = coord
        self.sample_rate = sample_rate
        self.delays = np.zeros(n_channels) #in microseconds
        self.gains = np.ones(n_channels) # multiplier
        self.sample_dur= 1/sample_rate *10**6 #Duration of a sample in microseconds
        self.delay_approx=DelayAproximator(self.coord)
        self.doa=0
        self.update_delays(0,0)
        self.locked=False
    def beamform(self,samples):

        sample_save=samples
        # outdata= np.zeros((self.n_channels))
        # for i in range(self.n_channels):
        #     outdata[i]=np.mean(samples[i][0:2048])
        #     if(outdata[i]>=0.002):
        #         samples.T[i]=0
        # # for i in range(self.n_channels-1):
        # #     outdata[i]=np.mean(data[i][0:2048])
        # #     if(outdata[i]>outdata[i+1]):
        # #         samples.T[i]=0
        # #     else:
        # #         samples.T[i]=0
        # if(outdata[0]<=outdata[1]):
        #     samples=np.roll(samples.T,1).T
        # print(samples)
        # shifts=(self.calculate_channel_shift()).astype(int)

        # max_sample_shift=int(max(shifts))
        # summed=np.zeros(samples.shape[0])
        # for j in range(samples.shape[0]-max_sample_shift):
        #     for i in range(self.n_channels):
        #         summed[j] += samples[j+shifts[i]][i].sum()

        samples,max_sample_shift=self.delay_and_gain(samples)

        samples=self.sum_channels(samples)
        # if hasattr(self,'last_overlap'):
        #     for i in range(self.last_overlap.shape[0]):
        #         samples[i]+=self.last_overlap[i]

        # self.last_overlap=samples[samples.shape[0]-max_sample_shift:samples.shape[0]]



        return samples[0:samples.shape[0]-max_sample_shift]

    def sum_channels(self,samples):
        summed=np.zeros(samples.shape[0])
        # for j in range(samples.shape[1]):
        #     summed+=samples.T[j]
        for j in range(samples.shape[0]):
            summed[j] = samples[j].sum()
        return summed
    def delay_and_gain(self, samples):
        #backwards interpolations solves every prblem
        shifts=self.calculate_channel_shift()
        delayed=np.zeros(samples.shape)
        max_sample_shift=int(max(shifts))

        for i in range(self.n_channels):

            delayed.T[i]=np.roll(samples.T[i],-int(shifts[i]))# make pos if wierd


        return delayed,max_sample_shift
    #calculates number of samples to delay
    def calculate_channel_shift(self):
        channel_shifts=np.round((self.delays/self.sample_dur))
        return channel_shifts

    def update_delays(self,azimuth,elevation): #doa in degrees, assuming plane wave as it is a far-field source
        self.delays=np.array(self.delay_approx.get_flat_delays(azimuth,elevation))*10**6
        print(self.delays)
        shift=min(self.delays)
        self.delays+=-shift
        print("azi ele")
        print(str(azimuth)+" "+str(elevation))
        print("channel shift")
        print(self.calculate_channel_shift())


from SignalGen import SignalGen
from Preprocessor import Preprocessor
import soundfile as sf
import PDMGenerator as pdm

def get_data(filename,channel,length):
    i=0
    j=0
    data=np.zeros((length))
    with open(filename, 'r') as file:
        line="  "

        while(line!=""):
            line=file.readline()
            if(line==""):
                break
            i+=1

            if(i%2==channel):
                continue
            data[j]=int(line.strip())
            j+=1
    return data
# # spacing=np.array([[-0.1,-0.1,0],[-0.1,0.0,0],[-0.1,0.1,0],[0,-0.1,0],[0,0,0],[0,0.1,0],[0.1,-0.1,0],[0.1,0,0],[0.1,0.1,0]])
# # spacing=np.array([[-0.2,-0.2,0],[-0.2,-0.1,0],[-0.2,0.1,0],[-0.2,0.2,0],[-0.1,-0.2,0],[-0.1,-0.1,0],[-0.1,0.1,0],[-0.1,0.2,0],[0.1,-0.2,0],[0.1,-0.1,0],[0.1,0.1,0],[0.1,0.2,0],[0.2,-0.2,0],[0.2,-0.1,0],[0.2,0.1,0],[0.2,0.2,0]])
# # spacing=np.array([[-0.18,0.12,0],[-0.06,0.12,0],[0.06,0.12,0],[0.18,0.12,0],[-0.18,0,0],[-0.06,0,0],[0.06,0,0],[0.18,0,0],[-0.18,-0.12,0],[-0.06,-0.12,0],[0.06,-0.12,0],[0.18,-0.12,0]])
# # spacing=np.array([[-0.08,0.042],[-0.08,0.014],[-0.08,-0.028],[-0.08,-0.042],[0.08,0.042],[0.08,0.014],[0.08,-0.028],[0.08,-0.042]])
# # spacing=np.array([[0,0],[0.028,0],[0.056,0],[0.084,0],[0.112,0],[0.14,0],[0.168,0],[0.196,0]])
# spacing=np.array([[-0.06,-0.24,0],[-0.18,-0.24,0],[-0.06,-0.12,0],[-0.18,-0.12,0],[-0.06,0,0],[-0.18,0,0],[-0.06,0.12,0],[-0.18,0.12,0],[0.18,-0.24,0],[0.06,-0.24,0],[0.18,-0.12,0],[0.06,-0.12,0],[0.18,0,0],[0.06,0,0],[0.18,0.12,0],[0.06,0.12,0]])

# import CICFilter as cic

# # sig=Sine(1500,0.5,48000)
# azimuth=60
# elevation=60
# beam=Beamformer(n_channels=16,coord=spacing,sample_rate=48000*64)
# samplerate=48000*64
# duration=2
# subduration=1
# data= np.zeros((16,int(samplerate*(subduration))))


# length=int(samplerate*duration)
# data[0]=(get_data("./Acoustics/PDMTests/57/output_bit_1.txt",0,length))[0:int(48000*64*subduration)]
# print("Stream 1 Complete")
# data[1]=get_data("./Acoustics/PDMTests/57/output_bit_1.txt",1,length)[0:int(48000*64*subduration)]
# print("Stream 2 Complete")
# data[2]=get_data("./Acoustics/PDMTests/57/output_bit_2.txt",0,length)[0:int(48000*64*subduration)]
# print("Stream 3 Complete")
# data[3]=get_data("./Acoustics/PDMTests/57/output_bit_2.txt",1,length)[0:int(48000*64*subduration)]
# print("Stream 4 Complete")
# data[4]=get_data("./Acoustics/PDMTests/57/output_bit_3.txt",0,length)[0:int(48000*64*subduration)]
# print("Stream 5 Complete")
# data[5]=get_data("./Acoustics/PDMTests/57/output_bit_3.txt",1,length)[0:int(48000*64*subduration)]
# print("Stream 6 Complete")
# data[6]=get_data("./Acoustics/PDMTests/57/output_bit_4.txt",0,length)[0:int(48000*64*subduration)]
# print("Stream 7 Complete")
# data[7]=get_data("./Acoustics/PDMTests/57/output_bit_4.txt",1,length)[0:int(48000*64*subduration)]
# print("Stream 8 Complete")
# data[8]=get_data("./Acoustics/PDMTests/57/output_bit_8.txt",0,length)[0:int(48000*64*subduration)]
# print("Stream 9 Complete")
# data[9]=get_data("./Acoustics/PDMTests/57/output_bit_8.txt",1,length)[0:int(48000*64*subduration)]
# print("Stream 10 Complete")
# data[10]=get_data("./Acoustics/PDMTests/57/output_bit_9.txt",0,length)[0:int(48000*64*subduration)]
# print("Stream 11 Complete")
# data[11]=get_data("./Acoustics/PDMTests/57/output_bit_9.txt",1,length)[0:int(48000*64*subduration)]
# print("Stream 12 Complete")
# data[12]=get_data("./Acoustics/PDMTests/57/output_bit_10.txt",0,length)[0:int(48000*64*subduration)]
# print("Stream 13 Complete")
# data[13]=get_data("./Acoustics/PDMTests/57/output_bit_10.txt",1,length)[0:int(48000*64*subduration)]
# print("Stream 14 Complete")
# data[14]=get_data("./Acoustics/PDMTests/57/output_bit_11.txt",0,length)[0:int(48000*64*subduration)]
# print("Stream 15 Complete")
# data[15]=get_data("./Acoustics/PDMTests/57/output_bit_11.txt",1,length)[0:int(48000*64*subduration)]
# print("Stream 16 Complete")
# print("Data Collected")
# segments=7
# time_segs=int(np.ceil(subduration*10))
# rms_data=np.zeros((segments,segments,int(time_segs)))
# azi=-90
# ele=-90

# import time
# # # beam.update_delays(30,0)
# # outdata=beam.beamform(data.T)
# # print(data.shape)
# # print("sfsgfdjkh")
# # print(outdata.shape)
# # outdatapcm=cic.cic(outdata)
# # print("fjkhsjkdfhjkhs")
# # print(outdatapcm.shape)
# # outdatapcm/=np.max(outdatapcm)

# # from scipy.io.wavfile import write,read
# # write("./Acoustics/PDMTests/1/beamformedchannel.wav", 48000,outdatapcm)
# for i in range(segments):
#     for j in range(segments):

#         # io=IOStream()
#         # io.arrToStream(speech,48000)
#         print(i)
#         beam.update_delays(azi+(180/segments)/2,ele+(180/segments)/2)
#         outdata=beam.beamform(data.T)
#         outdatapcm=cic.cic(outdata)
#         for k in range(time_segs-1):
            
#             rms_data[i][j][k]=np.mean(outdatapcm[k*1*960:(k+1)*1*960]**2)
#         rms_data[i][j][time_segs-1]=np.mean(outdatapcm[(time_segs-1)*1*960:]**2)
#         # for k in range(time_segs-1):
            
#         #     rms_data[i][j][k]=np.mean(outdatapcm**2)
#         # rms_data[i][j][time_segs-1]=np.mean(outdatapcm**2)
        
        
#         ele+=180/segments
#         print(rms_data)
#     ele=-90
#     azi+=180/segments
# print(rms_data)
# import os
# os.makedirs("./Acoustics/PDMTests/57/rms_frames"+str(segments)+"_"+str(subduration), exist_ok=True)
# np.save("./Acoustics/PDMTests/57/rms_data_"+str(segments)+"_"+str(subduration)+".npy", rms_data)
# import numpy as np
# import matplotlib.pyplot as plt

# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

# # Assuming rms_data has shape (azimuth, elevation, time)
# segments_azi = rms_data.shape[0]
# segments_ele = rms_data.shape[1]
# time_steps = rms_data.shape[2]
# azi_angles = np.linspace(-90, 90, segments_azi)  # Azimuth angles
# ele_angles = np.linspace(-90, 90, segments_ele)  # Elevation angles
# azi_grid, ele_grid = np.meshgrid(azi_angles, ele_angles)



# # Normalize RMS data
# rms_data /= np.max(rms_data)

# # Create figure and axis
# fig, ax = plt.subplots(figsize=(10, 7))
# im = ax.pcolormesh(azi_grid, ele_grid, rms_data[:, :, 0], shading='auto', cmap='viridis', vmin=0, vmax=1)
# cbar = fig.colorbar(im, ax=ax, label="Normalized RMS Power")

# # Scatter point for max RMS power (initialize, update later)
# max_point, = ax.plot([], [], 'ro', markersize=8, label="Strongest RMS Power")
# ax.legend()

# def update(frame):
#     im.set_array(rms_data[:, :, frame].ravel())  # Update heatmap data

#     # Find and update maximum power point
#     max_idx = np.unravel_index(np.argmax(rms_data[:, :, frame]), rms_data[:, :, frame].shape)
#     max_azi = azi_angles[max_idx[1]]  # Fixing indexing order
#     max_ele = ele_angles[max_idx[0]]
#     max_point.set_data([max_azi], [max_ele])  # Wrap values in lists

#     ax.set_title(f"RMS Power Distribution (Time Step {frame})")
#     plt.savefig(os.path.join("./Acoustics/PDMTests/57/rms_frames"+str(segments)+"_"+str(subduration), f"frame_{frame:03d}.png"))

# # Create animation
# ani = animation.FuncAnimation(fig, update, frames=time_steps, interval=100, repeat=True)
# ani.save("./Acoustics/PDMTests/57/rms_animation"+str(segments)+"_"+str(subduration)+".gif", writer="Pillow", fps=10)
# plt.show()



# interpolator=Preprocessor(mirrored=False,interpolate=int(np.ceil(target_samplerate/16000)))
# print(speech.shape)
# speech=np.reshape(speech,(-1,1))
# print(speech.shape)
# speech=interpolator.process(speech)
# print(speech.shape)
# sig_gen.update_delays(azimuth,elevation)
# print(speech.shape)
# angled_speech=sig_gen.delay_and_gain(speech)
# print(angled_speech.shape)
# speech1,samplerate=sf.read(("C:/Users/arg/Documents/Datasets/dev-clean.tar/dev-clean/LibriSpeech/dev-clean/652/130737/652-130737-0005.flac"))
# interpolator=Preprocessor(mirrored=False,interpolate=int(np.ceil(target_samplerate/16000)))
# speech1=np.reshape(speech1,(-1,1))
# speech1=interpolator.process(speech1)
# sig_gen.update_delays(50,-80)
# # angled_speech=angled_speech[0:min(len(speech),len(speech1))]+sig_gen.delay_and_gain(speech1)[0:min(len(speech),len(speech1))]*1.2
# angled_speech=sig_gen.delay_and_gain(speech1)


# spacing=np.array([[-0.1,-0.1,0],[-0.1,0.0,0],[-0.1,0.1,0],[0,-0.1,0],[0,0,0],[0,0.1,0],[0.1,-0.1,0],[0.1,0,0],[0.1,0.1,0]])
# segments=7
# rms_data=np.zeros((segments,segments))
# azi=-90
# ele=-90
# for i in range(segments):
#     for j in range(segments):

#         io=IOStream()
#         io.arrToStream(speech,48000)
#         print(i)
#         beam.update_delays(azi+(180/segments)/2,ele+(180/segments)/2)
#         while(not io.complete()):

#             sample=io.getNextSample()
#             sample[np.abs(sample) < (0.00063)] = 0
#             outdata=beam.beamform(sample)
#             rms_data[i][j]+=np.mean(outdata**2)
#         ele+=180/segments
#         print(rms_data)
#     ele=-90
#     azi+=180/segments
# print(rms_data)
# # rms_data=np.array([[37.09039681, 37.09039732, 37.09039732, 37.09039732], [26.2475326,  37.46160062, 64.05876732, 75.13930766], [37.09039713, 64.0587671,  99.82955105, 55.64336452], [45.31064137, 70.59155776, 55.64336426, 29.43501057]])

# import numpy as np
# import matplotlib.pyplot as plt


# segments = rms_data.shape[0]
# azi_angles = np.linspace(-90, 90, segments)  # Azimuth angles
# ele_angles = np.linspace(-90, 90, segments)  # Elevation angles

# # Create a meshgrid for azimuth and elevation
# azi_grid, ele_grid = np.meshgrid(azi_angles, ele_angles)

# # Normalize RMS data for visualization
# rms_data_normalized = rms_data / np.max(rms_data)

# # Plot the heatmap
# plt.figure(figsize=(10, 7))
# plt.pcolormesh(azi_grid, ele_grid, rms_data_normalized, shading='auto', cmap='viridis')
# plt.colorbar(label="Normalized RMS Power")
# plt.xlabel("Azimuth (°)")
# plt.ylabel("Elevation (°)")
# plt.title("RMS Power Distribution (Azimuth-Elevation Plane)")

# # Highlight maximum RMS power point
# max_idx = np.unravel_index(np.argmax(rms_data), rms_data.shape)
# max_azi = azi_angles[max_idx[1]]
# max_ele = ele_angles[max_idx[0]]
# plt.scatter(max_azi, max_ele, color='red', label="Strongest RMS Power", zorder=5)
# plt.legend()

# plt.show()
