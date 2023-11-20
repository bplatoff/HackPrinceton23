import signal
import sys
import json
import base64
import socket
import time
from threading import Timer
import struct
import random
import serial
import cv2

class TransmitServer():
	def __init__(self, IP, PORT, emulate_data=False):
		self.IP = IP
		self.PORT = PORT
		self.emulate = emulate_data

		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((IP, PORT))
		self.server_socket.listen(5)
		self.client_socket = None
		self.serial_conn = None
		self.setup_signal_handler()
		print("Server is now running")
		
		self.sensor_data = {"Humidity": "0", "Temperature": "0", "Moisture Value": "0", "Light Value": "0"}

		if not emulate_data:
			self.serial_conn = serial.Serial('/dev/tty.usbserial-0001', 9600, timeout=1)
			self.serial_conn.reset_input_buffer()

	def setup_signal_handler(self):
		signal.signal(signal.SIGINT, self.sigint_handler)

	def sigint_handler(self, signal, frame):
		print('Interrupted')
		if self.client_socket:
			self.client_socket.close()
		self.server_socket.close()
		sys.exit(0)

	def read_sensor_data(self):
		
		if self.emulate:
			# Generate Fake Data
			self.sensor_data = {"Humidity": str(round(random.uniform(20, 80), 2)), "Temperature": str(round(random.uniform(20, 80), 2)),
					   			"Moisture Value": str(round(random.uniform(20, 80), 2)), "Light Value": str(round(random.uniform(0, 100)))}
		else:
			while self.serial_conn.in_waiting > 0:
				line = self.serial_conn.readline().decode('utf-8').rstrip().split(':')
				line = [l.strip() for l in line]
				if line[0] in self.sensor_data.keys():
					self.sensor_data[line[0]] = line[1]
		
			
	def receive_data(self):

		take_photo = True

		try:
			message = self.client_socket.recv(1024).decode("utf-8")
			if message == "camera_angle_changed":

				if self.emulate:
					print("Received Turn Message")
				else:
					take_photo = False
					self.serial_conn.reset_input_buffer()
					self.serial_conn.write(b"turn\n")
					while self.serial_conn.in_waiting == 0:
						time.sleep(.5)
					line = self.serial_conn.readline().decode('utf-8').rstrip()
					if line == "turn_complete":
						take_photo = True
		except socket.error as e:
			pass  # No message received, ignore the error

		if take_photo:
			self.send_data()
		Timer(5, self.receive_data).start()
		
	def capture_image(self):

		camera = cv2.VideoCapture(0)
		_, frame = camera.read()
		camera.release()

		_, buffer = cv2.imencode('.jpg', frame)
		jpg_as_text = base64.b64encode(buffer).decode()

		if frame is not None: 
			return jpg_as_text 
		return 0
			

	def send_data(self):
		jpg_as_text = self.capture_image()
		self.read_sensor_data()
		
		data = {"image": jpg_as_text, "params": self.sensor_data}

		json_data = json.dumps(data)
		bytes_data = json_data.encode()

		try:
			self.client_socket.sendall(struct.pack("Q", len(bytes_data)))
			self.client_socket.sendall(bytes_data)
		except Exception as e:
			print(f"Error experienced: {e}")

	def run(self):
		while True:
			self.client_socket, address = self.server_socket.accept()
			print(f"Connection from {address} has been established.")
			self.receive_data()


# Usage
IP = '192.168.1.158'
PORT = 5010
server = TransmitServer(IP, PORT, emulate_data=True)
server.run()
