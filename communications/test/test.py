import serial
import time

# Change this to match your serial port name:
# Windows: COM3, COM4, etc.
# macOS/Linux: /dev/ttyUSB0, /dev/ttyACM0, /dev/cu.usbserial, etc.
PORT = 'COM25'  # Replace with your actual port (e.g., '/dev/ttyUSB0')
BAUD_RATE = 9600

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {PORT} at {BAUD_RATE} baud.")

    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Received: {line}")
        time.sleep(0.1)

except serial.SerialException as e:
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    print("\nInterrupted by user.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
