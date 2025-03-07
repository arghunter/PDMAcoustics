import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

def twos_complement_24bit(msb, mid, lsb):
    """Convert 3 bytes (MSB, MID, LSB) to a signed 24-bit integer."""
    value = (msb << 16) | (mid << 8) | lsb
    if value & 0x800000:  # Check if the sign bit is set
        value -= 0x1000000  # Convert to negative
    return value

class SerialHeatmapVisualizer:
    def __init__(self, port, baudrate=3000000, grid_size=16):
        self.port = port
        self.baudrate = baudrate
        self.grid_size = grid_size
        self.ser = None
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.heatmap_data = np.zeros((grid_size, grid_size))
        self.values_buffer = []
        self.seq_count = 0
        
        # Create initial heatmap
        self.heatmap = self.ax.imshow(
            self.heatmap_data, 
            cmap='viridis', 
            interpolation='nearest',
            vmin=-32768,  # Initial scale for 16-bit values
            vmax=32767
        )
        
        self.fig.colorbar(self.heatmap, ax=self.ax)
        self.ax.set_title('Real-time Sensor Heatmap')
        self.ax.set_xlabel('Column Index (0-15)')
        self.ax.set_ylabel('Row Index (0-15)')
        
    def connect_serial(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Connected to {self.port} at {self.baudrate} baud")
            self.ser.read(1)
            return True
        except Exception as e:
            print(f"Error connecting to serial port: {e}")
            return False
            
    def read_data(self):
        """Read data from serial port and update values_buffer"""
        if not self.ser or not self.ser.is_open:
            return False
            
        # Try to read enough bytes to fill our buffer
        bytes_needed = 4 * (256 - len(self.values_buffer)//4)
        if bytes_needed > 0:
            data = self.ser.read(bytes_needed)
            
            # Process incoming bytes
            for byte in data:
                self.values_buffer.append(byte)
        
        # Check if we have complete set of 256 values (1024 bytes total)
        return len(self.values_buffer) >= 1024
    
    def process_frame(self):
        """Process a complete frame of 256 values"""
        processed_values = []
        
        # Process in chunks of 4 bytes (seq_num, msb, mid, lsb)
        for i in range(0, 1024, 4):
            if i+3 >= len(self.values_buffer):
                break
                
            seq_num = self.values_buffer[i]
            value = twos_complement_24bit(
                self.values_buffer[i+1],
                self.values_buffer[i+2],
                self.values_buffer[i+3]
            )
            processed_values.append((seq_num, value))
            # print(value)
        # Clear processed bytes from buffer
        self.values_buffer = self.values_buffer[4*len(processed_values):]
        
        # Update heatmap data
        for seq_num, value in processed_values:
            row = seq_num // self.grid_size
            col = seq_num % self.grid_size
            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                self.heatmap_data[row, col] = np.log((value)+0.0001)        
        # Dynamically adjust color scale
        vmin = 0.1
        vmax = 5
        # print(vmax)
        self.heatmap.set_clim(vmin, vmax)
        
        # Update plot data
        self.heatmap.set_array(self.heatmap_data)
        self.seq_count += 1
        self.ax.set_title(f'Real-time Sensor Heatmap (Frame {self.seq_count})')
        
        return True
            
    def update(self, frame):
        """Animation update function"""
        if self.read_data():
            self.process_frame()
        return [self.heatmap]
        
    def run(self):
        """Start the visualization"""
        if not self.connect_serial():
            print("Failed to connect to serial port. Exiting.")
            return
            
        # Set up animation
        self.animation = FuncAnimation(
            self.fig, 
            self.update, 
            interval=40,  # Update every 50ms (20 fps)
            blit=True
        )
        
        plt.tight_layout()
        plt.show()
        
    def close(self):
        """Clean up resources"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed")

if __name__ == "__main__":
    port = "COM9"  # Change this to match your system
    
    try:
        visualizer = SerialHeatmapVisualizer(port)
        visualizer.run()
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        if 'visualizer' in locals():
            visualizer.close()
            
            
            
            
# import serial
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from scipy.ndimage import gaussian_filter
# import time

# def twos_complement_24bit(msb, mid, lsb):
#     """Convert 3 bytes (MSB, MID, LSB) to a signed 24-bit integer."""
#     value = (msb << 16) | (mid << 8) | lsb
#     if value & 0x800000:  # Check if the sign bit is set
#         value -= 0x1000000  # Convert to negative
#     return value

# class SerialHeatmapVisualizer:
#     def __init__(self, port, baudrate=3000000, grid_size=16, smoothing_sigma=1.0, interpolation_method='bicubic'):
#         self.port = port
#         self.baudrate = baudrate
#         self.grid_size = grid_size
#         self.ser = None
#         self.fig, self.ax = plt.subplots(figsize=(10, 8))
#         self.heatmap_data = np.zeros((grid_size, grid_size))
#         self.values_buffer = []
#         self.seq_count = 0
        
#         # Smoothing and interpolation parameters
#         self.smoothing_sigma = smoothing_sigma
#         self.interpolation_method = interpolation_method
        
#         # Create initial heatmap
#         self.heatmap = self.ax.imshow(
#             self.apply_smoothing(self.heatmap_data), 
#             cmap='viridis', 
#             interpolation=self.interpolation_method,
#             vmin=-32768,  # Initial scale for 16-bit values
#             vmax=32767
#         )
        
#         self.fig.colorbar(self.heatmap, ax=self.ax)
#         self.ax.set_title('Real-time Sensor Heatmap (Smoothed)')
#         self.ax.set_xlabel('Column Index (0-15)')
#         self.ax.set_ylabel('Row Index (0-15)')
        
#         # Add controls for smoothing
#         plt.subplots_adjust(bottom=0.15)
#         from matplotlib.widgets import Slider
#         self.slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])
#         self.slider = Slider(
#             self.slider_ax, 'Smoothing', 0.0, 3.0, 
#             valinit=self.smoothing_sigma, valstep=0.1
#         )
#         self.slider.on_changed(self.update_smoothing)
        
#     def update_smoothing(self, val):
#         """Update the smoothing parameter when slider is adjusted"""
#         self.smoothing_sigma = val
#         self.update_display()
        
#     def apply_smoothing(self, data):
#         """Apply Gaussian smoothing to the data"""
#         if self.smoothing_sigma > 0:
#             return gaussian_filter(data, sigma=self.smoothing_sigma)
#         return data
        
#     def connect_serial(self):
#         try:
#             self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
#             print(f"Connected to {self.port} at {self.baudrate} baud")
#             self.ser.read(3)
#             return True
#         except Exception as e:
#             print(f"Error connecting to serial port: {e}")
#             return False
            
#     def read_data(self):
#         """Read data from serial port and update values_buffer"""
#         if not self.ser or not self.ser.is_open:
#             return False
            
#         # Try to read enough bytes to fill our buffer
#         bytes_needed = 4 * (256 - len(self.values_buffer)//4)
#         if bytes_needed > 0:
#             data = self.ser.read(bytes_needed)
            
#             # Process incoming bytes
#             for byte in data:
#                 self.values_buffer.append(byte)
        
#         # Check if we have complete set of 256 values (1024 bytes total)
#         return len(self.values_buffer) >= 1024
    
#     def process_frame(self):
#         """Process a complete frame of 256 values"""
#         processed_values = []
        
#         # Process in chunks of 4 bytes (seq_num, msb, mid, lsb)
#         for i in range(0, 1024, 4):
#             if i+3 >= len(self.values_buffer):
#                 break
                
#             seq_num = self.values_buffer[i]
#             value = twos_complement_24bit(
#                 self.values_buffer[i+1],
#                 self.values_buffer[i+2],
#                 self.values_buffer[i+3]
#             )
#             processed_values.append((seq_num, value))
        
#         # Clear processed bytes from buffer
#         self.values_buffer = self.values_buffer[4*len(processed_values):]
        
#         # Update heatmap data
#         for seq_num, value in processed_values:
#             row = seq_num // self.grid_size
#             col = seq_num % self.grid_size
#             if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
#                 self.heatmap_data[row, col] = value
        
#         self.update_display()
#         self.seq_count += 1
#         self.ax.set_title(f'Real-time Sensor Heatmap (Frame {self.seq_count})')
        
#         return True
    
#     def update_display(self):
#         """Update the display with current data and smoothing settings"""
#         # Apply smoothing
#         smoothed_data = self.apply_smoothing(self.heatmap_data)
        
#         # Dynamically adjust color scale
#         vmin = np.min(smoothed_data)
#         vmax = np.max(smoothed_data)
#         self.heatmap.set_clim(vmin, vmax)
        
#         # Update plot data
#         self.heatmap.set_array(smoothed_data)
#         self.heatmap.set_interpolation(self.interpolation_method)
            
#     def update(self, frame):
#         """Animation update function"""
#         if self.read_data():
#             self.process_frame()
#         return [self.heatmap]
        
#     def run(self):
#         """Start the visualization"""
#         if not self.connect_serial():
#             print("Failed to connect to serial port. Exiting.")
#             return
            
#         # Set up animation
#         self.animation = FuncAnimation(
#             self.fig, 
#             self.update, 
#             interval=50,  # Update every 50ms (20 fps)
#             blit=True
#         )
        
#         # Add interpolation dropdown
#         from matplotlib.widgets import RadioButtons
#         rax = plt.axes([0.02, 0.7, 0.12, 0.15])
#         interpolation_options = ['none', 'bilinear', 'bicubic', 'gaussian', 'spline16']
#         self.radio = RadioButtons(rax, interpolation_options, active=interpolation_options.index(self.interpolation_method))
        
#         def interpolation_changed(label):
#             self.interpolation_method = label
#             self.update_display()
        
#         self.radio.on_clicked(interpolation_changed)
        
#         plt.tight_layout(rect=[0, 0.15, 1, 1])  # Adjust for slider
#         plt.show()
        
#     def close(self):
#         """Clean up resources"""
#         if self.ser and self.ser.is_open:
#             self.ser.close()
#             print("Serial connection closed")

# if __name__ == "__main__":
#     port = "COM9"  # Change this to match your system
    
#     try:
#         visualizer = SerialHeatmapVisualizer(
#             port=port,
#             smoothing_sigma=1.0,          # Initial Gaussian smoothing sigma
#             interpolation_method='bicubic' # Initial interpolation method
#         )
#         visualizer.run()
#     except KeyboardInterrupt:
#         print("Stopped by user.")
#     finally:
#         if 'visualizer' in locals():
#             visualizer.close()