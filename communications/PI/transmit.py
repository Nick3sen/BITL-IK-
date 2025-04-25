import serial
import time
gripper = serial.Serial('/dev/ttyUSB0', 9600)  # Replace with your Arduino port
# Wait for connections to establish
time.sleep(2)

def send_to_device(device, message):
    print(f"Sending: {message}")
    device.write((message + '\n').encode('utf-8'))
    time.sleep(0.1)
  
def read_from_device(device):
    if device.in_waiting > 0:  # Check if data is available
        data = device.readline().decode('utf-8').strip()  # Read and decode the data
        parse_data(data)
        print(f"Received: {data}")

def parse_data(data):
    # Split the data into individual components
    data_parts = data.split()
    print(data_parts)

# Main loop
try:
    while True:
        # Example: Send commands
        x = int(input("do you want to send?"))
        if x == 1:
            send_to_device(gripper, "Command to Arduino 1")
        # Read responses
        read_from_device(gripper)

except KeyboardInterrupt:
    print("Exiting...")
    gripper.close()
