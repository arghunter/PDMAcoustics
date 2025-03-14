import serial
import numpy as np
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize serial connection
ser = serial.Serial('COM5', 921600, timeout=1)

# Preamble buffer
pt = 0
times = 0
pdata = np.zeros((16, 16, 600))  # Storage for frames
segments = 16
interpScale = 1
fov = 120
lock = threading.Lock()  # Lock to ensure thread safety

# Matplotlib figure setup
initial_data = np.zeros((segments, segments))  # Assuming square grid
zoom_factors = (interpScale, interpScale)

# Interpolated grid dimensions
segments_azi, segments_ele = [int(dim * interpScale) for dim in initial_data.shape]
azi_angles = np.linspace(-int(fov / 2), int(fov / 2), segments_azi)
ele_angles = np.linspace(-int(fov / 2), int(fov / 2), segments_ele)
azi_grid, ele_grid = np.meshgrid(azi_angles, ele_angles)

# Ensure azi_grid and ele_grid match the expected shape for pcolormesh
azi_grid = azi_grid[:-1, :-1]  # Reduce by 1 in both dimensions
ele_grid = ele_grid[:-1, :-1]

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 7))

# Generate a properly shaped initial heatmap
initial_rms_data = np.zeros((segments_azi - 1, segments_ele - 1))
im = ax.pcolormesh(azi_grid, ele_grid, initial_rms_data, shading='auto', cmap='viridis', vmin=0, vmax=1)
cbar = fig.colorbar(im, ax=ax, label="Normalized RMS Power")

# Scatter point for max RMS power
max_point, = ax.plot([], [], 'ro', markersize=8, label="Strongest RMS Power")
ax.legend()

def read_serial():
    """ Reads serial data and updates `pdata` in real-time """
    global times, pt
    global pdata
    ovals=np.zeros(300)

    past = np.zeros(4, dtype=int)
    while True:
        byte = ser.read(1)
        if int.from_bytes(byte, byteorder="little") == 88:
            past = np.roll(past, 1)
            past[0] = int.from_bytes(byte, byteorder="little")

            byte_pair = ser.read(3)
            if len(byte_pair) < 3:
                continue  # Skip if not enough bytes received

            value = int.from_bytes(byte_pair, byteorder='little')
            past = np.roll(past, 3)
            past[:3] = [byte_pair[0], byte_pair[1], byte_pair[2]]
            oval=0
            # Detect preamble (88 88 88 88)
            if np.all(past == 88):
                pt = 0  # Reset index
                times += 1
                # print(f"Frame {times} received")
                if(times == 600):
                    times = 0
                # Store data after preamble
                while pt < 256:
                    byte_pair = ser.read(2)
                    if len(byte_pair) < 2:
                        continue  # Ensure we read 2 bytes
                    
                    value = int.from_bytes(byte_pair, byteorder='little')
                    
                    # Use a lock to prevent race conditions
                    with lock:
                        pdata[int(pt / 16)][int(pt % 16)][times] = value
                    pt += 1
                    
                    oval=value
            ovals=np.roll(ovals,1)
            ovals[0]=value
            print(np.mean(ovals))        
                

def update(_):
    """ Update function for animation """
    global times
    global pdata
    # pdata[0][0][times-1]=0
    # pdata[0][1][times-1]=300
    if times > 0:  # Ensure there's at least one frame
        # Use a lock to access the latest data
        with lock:
            im.set_array(pdata[:-1, :-1, times - 1]/np.max(pdata))  # Show latest frame
    return im,

# Start serial reading in a separate thread
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

# Start animation
ani = animation.FuncAnimation(fig, update, interval=100, blit=False)
plt.show()
