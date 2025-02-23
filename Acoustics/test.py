import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.ndimage import zoom
from queue import Queue
import threading
import time

# Global queue for real-time RMS data updates
rms_queue = Queue()

def enqueue_rms_data(rms_data):
    """ Add new RMS data to the queue for real-time visualization """
    rms_queue.put(rms_data)

def real_time_anim(segments, subduration, testNum, interpScale, fov):
    os.makedirs(f"./Acoustics/PDMTests/{testNum}/rms_frames{segments}_{subduration}", exist_ok=True)

    # Placeholder for first frame
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

    def update(_):
        """ Updates the plot with new RMS data from the queue. """
        if not rms_queue.empty():
            rms_data = rms_queue.get()

            # Interpolate new data
            rms_data_interp = zoom(rms_data, zoom_factors, order=1)

            # Normalize (avoid division by zero)
            if np.max(rms_data_interp) > 0:
                rms_data_interp /= np.max(rms_data_interp)

            # Ensure the shape matches (reduce by 1 in both dimensions)
            rms_data_interp = rms_data_interp[:-1, :-1]

            # Update heatmap
            im.set_array(rms_data_interp.ravel())

            # Find and update maximum power point
            max_idx = np.unravel_index(np.argmax(rms_data_interp), rms_data_interp.shape)
            max_azi = azi_angles[max_idx[1]]
            max_ele = ele_angles[max_idx[0]]
            max_point.set_data([max_azi], [max_ele])

            ax.set_title(f"Real-Time RMS Power Distribution")

        return im, max_point

    ani = animation.FuncAnimation(fig, update, interval=200 / interpScale, blit=False)
    plt.show()

# Example usage (in a separate thread to simulate real-time updates)
def simulate_real_time_data():
    while True:
        new_rms = np.random.rand(10, 10)  # Example: New 10x10 RMS power array
        enqueue_rms_data(new_rms)
        time.sleep(0.5)  # Simulate new data every 0.5s

# Start real-time animation
threading.Thread(target=simulate_real_time_data, daemon=True).start()
real_time_anim(segments=10, subduration=5, testNum=1, interpScale=2, fov=60)
