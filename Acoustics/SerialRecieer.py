import serial

ser = serial.Serial('COM5', 115200, timeout=1)

while True:
    byte = ser.read(1)
    if byte == b'\xAA':  # Detect start marker
        data = ser.read(256)  # Read the full array
        print("Received:", data)
