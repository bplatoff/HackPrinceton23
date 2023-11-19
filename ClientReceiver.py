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


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if not torch.cuda.is_available(): print("WARNING: Model will run extremely slow on cpu")

# Load the model
DiseasePredictor = ResNetClassifer(38).to(device)

if torch.cuda.is_available():
    DiseasePredictor.load_state_dict(torch.load("DiseasedCropClassifier_5epochs_secondIteration.pth"))
else:
    print("WARNING: Model will run extremely slow on cpu. If on colab, go to Runtime->Change Runtime Type->Hardware Accelerator->GPU.")
    DiseasePredictor.load_state_dict(torch.load("/content/siamese_triplet_model_cache.pth", map_location=torch.device('cpu')))
DiseasePredictor.eval()

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),  # Assuming your model expects images of size (224, 224)
    transforms.ToTensor(),
])

predictions = []
start_time = time.time()
change_camera_angle_condition = False


# Set up socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.168", 5010))
while True:

    if time.time()-start_time >= 120:
        start_time = time.time()
        # Add your code to change the camera angle here

        # Send a message back to the server indicating the camera angle change
        message = "camera_angle_changed"
        print("Sending Camera Change message")
    else:
        message = "continue"
    s.sendall(message.encode("utf-8"))

    # Receive the data length
    data_len_bytes = s.recv(struct.calcsize("Q"))
    if len(data_len_bytes) < struct.calcsize("Q"):
        print("Incomplete data length received")
    else:
        data_len = struct.unpack("Q", data_len_bytes)[0]
        print("Received Data of Length: ", data_len)

        # Receive the data
        data = b""
        while len(data) < data_len:
            packet = s.recv(data_len - len(data))
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

                    # Further processing with frame...
                else:
                    frame = None
                    # Further processing without frame...

            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
        else:
            print("Incomplete data received")
            
    disease_status = "Healthy"
    predicted_probability = 67.345

    if frame is not None:
        print("Applying Deep Learning Model")
        # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite('Test Images/CurrentImage.jpg',frame)
        input_tensor = transform(frame)
        input_tensor = input_tensor.unsqueeze(0)  # Add batch dimension

        # Move the input tensor to the same device as the model
        input_tensor = input_tensor.to(device)

        # Forward pass through the model
        with torch.no_grad():
            prediction = DiseasePredictor(input_tensor)
        
        probabilities = F.softmax(prediction, dim=1)
        predicted_probability, predicted_classes = probabilities.max(1)
        predicted_classes = predicted_classes.item()
        plant_type, disease_status = DiseasePredictor.idx_to_class[predicted_classes]
        predicted_probability = predicted_probability.item() * 100


        # Store the prediction in the list
        predictions.append((plant_type, disease_status, predicted_probability))

    print("Received Parameters: ", additional_parameters)
    data = [disease_status, predicted_probability, additional_parameters['Temperature'], additional_parameters['Humidity'], additional_parameters['Light Value'], additional_parameters['Moisture Value']]
    file = open('Test Images/newdata.txt', 'wb')

    # dump information to that file
    pickle.dump(data, file)

    # close the file
    file.close()

# except Exception as error:
#     print(error)
#     print("Something is going wrong :(")
