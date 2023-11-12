import socket
import socket
import pickle
import struct
import cv2

from DiseaseClassifier import ResNetClassifer

import cv2
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import time

idx_to_class = {0: ('Apple', 'Apple Scab'),
                1: ('Apple', 'Black Rot'),
                2: ('Apple', 'Cedar Apple Rust'),
                3: ('Apple', 'Healthy'),
                4: ('Blueberry', 'Healthy'),
                5: ('Cherry', 'Healthy'),
                6: ('Cherry', 'Powdery Mildew'),
                7: ('Corn', 'Cercospora Leaf Spot / Gray Leaf Spot'),
                8: ('Corn', 'Common Rust'),
                9: ('Corn', 'Healthy'),
                10: ('Corn', 'Northern Leaf Blight'),
                11: ('Grape', 'Black Rot'),
                12: ('Grape', 'Esca (Black Measles)'),
                13: ('Grape', 'Healthy'),
                14: ('Grape', 'Leaf Blight (Isariopsis Leaf Spot)'),
                15: ('Orange', 'Haunglongbing (Citrus Greening)'),
                16: ('Peach', 'Bacterial Spot'),
                17: ('Peach', 'Healthy'),
                18: ('Bell Pepper', 'Bacterial Spot'),
                19: ('Bell Pepper', 'Healthy'),
                20: ('Potato', 'Early Blight'),
                21: ('Potato', 'Healthy'),
                22: ('Potato', 'Late Blight'),
                23: ('Raspberry', 'Healthy'),
                24: ('Soybean', 'Healthy'),
                25: ('Squash', 'Powdery Mildew'),
                26: ('Strawberry', 'Healthy'),
                27: ('Strawberry', 'Leaf Scorch'),
                28: ('Tomato', 'Bacterial Spot'),
                29: ('Tomato', 'Early Blight'),
                30: ('Tomato', 'Healthy'),
                31: ('Tomato', 'Late Blight'),
                32: ('Tomato', 'Leaf Mold'),
                33: ('Tomato', 'Septoria Leaf Spot'),
                34: ('Tomato', 'Spider Mites / Two-Spotted Spider Mite'),
                35: ('Tomato', 'Target Spot'),
                36: ('Tomato', 'Tomato Mosaic Virus'),
                37: ('Tomato', 'Tomato Yellow Leaf Curl Virus')}


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

change_camera_angle_condition = False

# Set up socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.50", 5002))
while True:

    if change_camera_angle_condition:
            # Add your code to change the camera angle here

            # Send a message back to the server indicating the camera angle change
            message = "camera_angle_changed"
            s.sendall(message.encode("utf-8"))

    # Receive the length of the data
    data_len = struct.unpack("L", s.recv(struct.calcsize("L")))[0]

    # Receive the data
    data = b""
    while len(data) < data_len:
        packet = s.recv(data_len - len(data))
        if not packet:
            break
        data += packet

    # Deserialize the received data
    frame, additional_parameters = pickle.loads(data)

    if frame is not None:
        print("Applying Deep Learning Model")
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
        plant_type, disease_status = idx_to_class[predicted_classes]
        predicted_probability = predicted_probability.item() * 100

        # Store the prediction in the list
        predictions.append((plant_type, disease_status, predicted_probability))


    # Print additional parameters
    print("Additional Parameters: ", additional_parameters)
    print("Deep Learning Output: ", predictions[-1])

# except Exception as error:
#     print(error)
#     print("Something is going wrong :(")
