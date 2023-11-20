import socket
import sys
import signal
import json
import base64
import time
import pickle
import struct
import numpy as np
import cv2
import torch
import torch.nn.functional as F
from torchvision import transforms
from DiseaseClassifier import ResNetClassifer

class ReceiveServer():
    def __init__(self, IP, PORT):
        
        # Load the Model
        self.DiseasePredictor = ResNetClassifer(38)
        self.DiseasePredictor.loadModel()

        self.is_camera_change = False

        # Set default values in case of failed receiving
        self.start_time = time.time()
        self.plant_type = "Corn"
        self.disease_status = "Healthy"
        self.predicted_probability = 67.345
        self.data = []

        # Set up socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((IP, PORT))

    def sendMessage(self):
        # Sends a True/False message depending on if we want to rotate the camera

        try:
            with open('Test Images/switch_camera.txt', 'rb') as file:
                self.is_camera_change = pickle.load(file)[0]
        except Exception as e:
            with open('Test Images/switch_camera.txt', 'wb') as file:
                pickle.dump(self.is_camera_change, file)

        print(self.is_camera_change)

        if self.is_camera_change:
            # Send a message back to the server indicating the camera angle change
            message = "camera_angle_changed"
            print("Sending Camera Change message")
        else:
            message = "continue"

        self.socket.sendall(message.encode("utf-8"))

    def receiveMessage(self):

        # Receive the data length
        data_len_bytes = self.socket.recv(struct.calcsize("Q"))
        if len(data_len_bytes) < struct.calcsize("Q"):
            print("Incomplete data length received")
        else:
            data_len = struct.unpack("Q", data_len_bytes)[0]
            print("Received Data of Length: ", data_len)

            # Receive the data
            data = b""
            while len(data) < data_len:
                packet = self.socket.recv(data_len - len(data))
                if not packet:
                    print("Connection closed or packet is empty")
                    break
                data += packet

            if len(data) == data_len:
                try:
                    # Deserialize the received data from JSON
                    received_data = json.loads(data.decode())

                    # Extract the frame and additional parameters
                    jpg_as_text = received_data["image"]
                    additional_parameters = received_data["params"]

                    # Convert the base64 string back to numpy array
                    if jpg_as_text != 0:
                        jpg_original = base64.b64decode(jpg_as_text)
                        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
                        frame = cv2.imdecode(jpg_as_np, flags=1)
                    else:
                        frame = None

                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
            else:
                print("Incomplete data received")

        if frame is not None:
            print("Applying Deep Learning Model")
            cv2.imwrite('Test Images/CurrentImage.jpg', frame)

            plant_type, disease_status, predicted_probability = self.DiseasePredictor.apply(frame)

        print("Received Parameters: ", additional_parameters)
        self.data = [plant_type, disease_status, predicted_probability, additional_parameters['Temperature'], additional_parameters['Humidity'], additional_parameters['Light Value'], additional_parameters['Moisture Value']]

        # Dump the new data into the text file
        with open('Test Images/newdata.txt', 'wb') as file:
            pickle.dump(data, file)

    def runServer(self):
        while True:
            self.sendMessage()
            self.receiveMessage()
            time.sleep(.1)

IP, PORT = "192.168.1.158", 5010
clientServer = ReceiveServer(IP, PORT)
clientServer.runServer()