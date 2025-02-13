import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
segments_azi = 30  # Number of azimuth segments
segments_ele = 30  # Number of elevation segments
time_steps = 50    # Number of time frames

azi_angles = np.linspace(-90, 90, segments_azi)  # Azimuth angles
ele_angles = np.linspace(-90, 90, segments_ele)  # Elevation angles
azi_grid, ele_grid = np.meshgrid(azi_angles, ele_angles)

# Generate synthetic RMS data with a moving peak
rms_data = np.zeros((segments_ele, segments_azi, time_steps))  # (elevation, azimuth, time)
for t in range(time_steps):
    peak_azi = -60 + 120 * (t / time_steps)  # Moves from -60° to 60° azimuth
    peak_ele = -30 + 60 * np.sin(2 * np.pi * t / time_steps)  # Oscillates in elevation
    rms_data[:, :, t] = np.exp(-((azi_grid - peak_azi) ** 2 + (ele_grid - peak_ele) ** 2) / (2 * 20 ** 2))

# Normalize RMS data
rms_data /= np.max(rms_data)

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 7))
im = ax.pcolormesh(azi_grid, ele_grid, rms_data[:, :, 0], shading='auto', cmap='viridis', vmin=0, vmax=1)
cbar = fig.colorbar(im, ax=ax, label="Normalized RMS Power")

# Scatter point for max RMS power (initialize, update later)
max_point, = ax.plot([], [], 'ro', markersize=8, label="Strongest RMS Power")
ax.legend()

def update(frame):
    im.set_array(rms_data[:, :, frame].ravel())  # Update heatmap data

    # Find and update maximum power point
    max_idx = np.unravel_index(np.argmax(rms_data[:, :, frame]), rms_data[:, :, frame].shape)
    max_azi = azi_angles[max_idx[1]]  # Fixing indexing order
    max_ele = ele_angles[max_idx[0]]
    max_point.set_data([max_azi], [max_ele])  # Wrap values in lists

    ax.set_title(f"RMS Power Distribution (Time Step {frame})")

# Create animation
ani = animation.FuncAnimation(fig, update, frames=time_steps, interval=32, repeat=True)

plt.show()
