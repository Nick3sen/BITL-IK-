# pi_echo.py
import serial

# Use the UART port (serial0 is usually a symlink to the correct one)
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

print("Raspberry Pi echo server started. Waiting for messages...")

try:
    while True:
        if ser.in_waiting > 0:
            # Read and decode incoming message
            message = ser.readline().decode('utf-8', errors='ignore').strip()
            if message:
                print(f"Received from laptop: {message}")
                # Send it back (echo)
                ser.write((message + '\n').encode())
                print("sending")
except KeyboardInterrupt:
    print("Exiting.")
    ser.close()
