import numpy as np
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.ndimage import zoom
def gen_anim(rms_data,segments,subduration,testNum, interpScale,fov):
    os.makedirs("./Acoustics/PDMTests/"+str(testNum)+"/rms_frames"+str(segments)+"_"+str(subduration), exist_ok=True)
    # Assuming rms_data_interp has shape (azimuth, elevation, time)
    zoom_factors = (interpScale, interpScale, interpScale)

    # Apply interpolation
    rms_data_interp = zoom(rms_data, zoom_factors, order=1)
    segments_azi = rms_data_interp.shape[0]
    segments_ele = rms_data_interp.shape[1]
    time_steps = rms_data_interp.shape[2]
    azi_angles = np.linspace(-int(fov/2), int(fov/2), segments_azi)
    ele_angles = np.linspace(-int(fov/2), int(fov/2), segments_ele)
    azi_grid, ele_grid = np.meshgrid(azi_angles, ele_angles)



    # Normalize RMS data
    rms_data_interp /= np.max(rms_data_interp)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 7))
    im = ax.pcolormesh(azi_grid, ele_grid, rms_data_interp[:, :, 0], shading='auto', cmap='viridis', vmin=0, vmax=1)
    cbar = fig.colorbar(im, ax=ax, label="Normalized RMS Powerncic")

    # Scatter point for max RMS power (initialize, update later)
    max_point, = ax.plot([], [], 'ro', markersize=8, label="Strongest RMS Power")
    ax.legend()

    def update(frame):
        im.set_array(rms_data_interp[:, :, frame].ravel())  # Update heatmap data

        # Find and update maximum power point
        max_idx = np.unravel_index(np.argmax(rms_data_interp[:, :, frame]), rms_data_interp[:, :, frame].shape)
        max_azi = azi_angles[max_idx[1]]  # Fixing indexing order
        max_ele = ele_angles[max_idx[0]]
        max_point.set_data([max_azi], [max_ele])  # Wrap values in lists

        ax.set_title(f"RMS Power Distribution (Time Step {frame})")
        plt.savefig(os.path.join("./Acoustics/PDMTests/"+str(testNum)+"/rms_frames"+str(segments)+"_"+str(subduration), f"frame_{frame:03d}.png"))

    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=time_steps, interval=200/interpScale, repeat=True)
    ani.save("./Acoustics/PDMTests/"+str(testNum)+"/rms_animation"+str(segments)+"_"+str(subduration)+".gif", writer="Pillow", fps=10)
    plt.show()
    
# rms_data = np.load("./Acoustics/PDMTests/57/rms_data_16_0.9.npy")
# gen_anim(rms_data,16,0.9,57,4)