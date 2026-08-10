import serial
import time
import requests
import os


FLASK_HOST = os.getenv("FLASK_HOST", "http://ho_app:5000")


# Update 'COM3' to match your PC's port ('/dev/ttyUSB0' on Linux)
PORT = 'COM3'
BAUD_RATE = 9600

try:
    # Open the serial port connection
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {PORT} at {BAUD_RATE} baud.")
    
    time.sleep(2)  # Give connection time to settle

    while True:
        if ser.in_waiting > 0:
            # Read line until '\n', decode ASCII/UTF-8 bytes to string
            line = ser.readline().decode('utf-8', errors='ignore').rstrip()
            print(f"Received: {line}")
            payload = {"temperature": float(line)}
            # requests.post("http://127.0.0.1:5000/add", json=payload)
            requests.post(f"{FLASK_HOST}/add", json=payload)

except serial.SerialException as e:
    print(f"Error opening port: {e}")
except KeyboardInterrupt:
    print("\nProgram closed by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")