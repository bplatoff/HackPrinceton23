#!/usr/bin/env python3
import signal
import sys
import json
import serial
import base64
import socket
import time
from threading import Timer
import cv2
import pickle
import struct

#eecutes when command+z is sent
def sigint_handler(signal, frame):
	print (' Interrupted')
	s.close()
	sys.exit(0)

signal.signal(signal.SIGTSTP, sigint_handler)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',5008))
s.listen(5)
ser = None
print("Server is now running")

def background_controller():
	
	params = {"Humidity":"0", "Temperature":"0", "Moisture Value": "0", "Light Value": "0"}
	
	while ser.in_waiting > 0:
		#print("Line recieved")
		line = ser.readline().decode('utf-8').rstrip().split(':')
		line = [l.strip() for l in line]
		print(line)
		if line[0] in params.keys():
			params[line[0]] = line[1]

	# implement check to see if we should be taking a photo
	take_photo = True

	try:
		message = clientsocket.recv(1024).decode("utf-8")
		if message == "camera_angle_changed":
			take_photo = False
			print("Change the Camera!")
			ser.reset_input_buffer()
			ser.write(b"turn\n")
			while ser.in_waiting == 0:
				time.sleep(.5)
			line = ser.readline().decode('utf-8').rstrip()
			if line == "turn_complete":
				take_photo = True
			
		
	except socket.error as e:
		pass # No message received, ignore the error

	if take_photo:
		print("Capturing Image")
		camera = cv2.VideoCapture(0)
		ret, frame = camera.read()
		camera.release()

		# Encode the frame in JPEG format
		retval, buffer = cv2.imencode('.jpg', frame)
		
		# Convert to base64 encoding and decode to string
		jpg_as_text = base64.b64encode(buffer).decode()

		# Prepare data as a dictionary
		data = {"image": jpg_as_text, "params": params}
	else:
		data = {"image": None, "params": params}

        
	# Serialize to JSON
	json_data = json.dumps(data)

	# Convert to bytes
	bytes_data = json_data.encode()

	try:
		# Send data length
		clientsocket.sendall(struct.pack("L", len(bytes_data)))
		
		# Send data
		clientsocket.sendall(bytes_data)

	except Exception as e:
		print(f"Error experienced: {e}")
		
	Timer(5, background_controller).start()

while True:
		clientsocket, address = s.accept()
		print(f"Connection from {address} has been established.")
		ser = serial.Serial('/dev/tty.usbserial-0001', 9600, timeout=1)
		ser.reset_input_buffer()
		background_controller()
