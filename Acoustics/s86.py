import sys
import serial
import numpy as np
import pyqtgraph as pg
import scipy.ndimage
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QSlider, QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal, Qt

def twos_complement_24bit(msb, mid, lsb):
    """Convert 3 bytes (MSB, MID, LSB) to a signed 24-bit integer."""
    value = (msb << 16) | (mid << 8) | lsb
    return value - 0x1000000 if value & 0x800000 else value

class SerialReader(QThread):
    """Handles reading serial data in a separate thread."""
    data_received = pyqtSignal(np.ndarray)

    def __init__(self, port, baudrate=3000000, grid_size=16):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.grid_size = grid_size
        self.running = True
        self.ser = None

    def run(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.ser.read(1)  # Clear initial data
            buffer = bytearray()
            
            while self.running:
                buffer.extend(self.ser.read(1024 - len(buffer)))
                
                while len(buffer) >= 1024:
                    frame_data = np.zeros((self.grid_size, self.grid_size))
                    for i in range(0, 1024, 4):
                        seq_num = buffer[i]
                        value = twos_complement_24bit(buffer[i+1], buffer[i+2], buffer[i+3])
                        row, col = 15 - (seq_num // self.grid_size), 15 - (seq_num % self.grid_size)
                        frame_data[row, col] = frame_data[row, col] * 0.6 + 0.4 * (value + 1)

                    buffer = buffer[1024:]  # Remove processed bytes
                    self.data_received.emit(frame_data)  # Send updated data to main thread

        except Exception as e:
            print(f"Serial error: {e}")
        finally:
            if self.ser:
                self.ser.close()

    def stop(self):
        self.running = False
        self.wait()

class HeatmapVisualizer(QMainWindow):
    """Main PyQt GUI with PyQtGraph for real-time heatmap visualization."""
    def __init__(self, port):
        super().__init__()
        self.setWindowTitle("Real-time Sensor Heatmap")
        self.setGeometry(100, 100, 600, 700)
        
        self.grid_size = 16
        self.smoothing_sigma = 1.0  # Default smoothing factor

        # Set up PyQtGraph heatmap
        self.plot_widget = pg.PlotWidget()
        self.img_item = pg.ImageItem()
        self.plot_widget.addItem(self.img_item)
        self.plot_widget.setAspectLocked(True)
        self.plot_widget.invertY(True)  # Align with matrix indexing

        # Color map settings
        colormap = pg.colormap.getFromMatplotlib('jet')
        self.img_item.setLookupTable(colormap.getLookupTable())

        # Status label
        self.status_label = QLabel("Waiting for data...")

        # Smoothing slider
        self.smoothing_slider = QSlider(Qt.Orientation.Horizontal)
        self.smoothing_slider.setMinimum(0)
        self.smoothing_slider.setMaximum(10)
        self.smoothing_slider.setValue(int(self.smoothing_sigma * 2))
        self.smoothing_slider.setTickInterval(1)
        self.smoothing_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.smoothing_slider.valueChanged.connect(self.update_smoothing)
        
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Less Smooth"))
        slider_layout.addWidget(self.smoothing_slider)
        slider_layout.addWidget(QLabel("More Smooth"))
        
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.status_label)
        layout.addLayout(slider_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Start serial reader thread
        self.serial_thread = SerialReader(port)
        self.serial_thread.data_received.connect(self.update_heatmap)
        self.serial_thread.start()
    
    def update_smoothing(self, value):
        """Updates smoothing factor based on slider input."""
        self.smoothing_sigma = value / 2.0

    def update_heatmap(self, data):
        """Updates heatmap display with optional smoothing."""
        if self.smoothing_sigma > 0:
            data = scipy.ndimage.gaussian_filter(data, sigma=self.smoothing_sigma)
        
        vmin, vmax = np.min(data), np.max(data)
        self.img_item.setImage(data.T, levels=(vmin, vmax))
        self.status_label.setText(f"Frame Updated - Max: {vmax:.2f}")
    
    def closeEvent(self, event):
        """Cleanup on window close."""
        self.serial_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    port = "COM9"  # Update to your correct port
    window = HeatmapVisualizer(port)
    window.show()
    sys.exit(app.exec())
