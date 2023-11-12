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

# Open a connection to the camera (0 represents the default camera)
cap = cv2.VideoCapture(0)

# Define a transformation to preprocess the image before feeding it into the model
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),  # Assuming your model expects images of size (224, 224)
    transforms.ToTensor(),
])

# List to accumulate predictions
predictions = []

# Time duration for capturing photos (in seconds)
capture_duration = 20

# Record the start time
start_time = time.time()

try:
    while time.time() - start_time < capture_duration:

        print("Beginning Capture")

        # Capture a frame
        ret, frame = cap.read()

        # Convert the OpenCV BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Apply the defined transformations
        input_tensor = transform(rgb_frame)
        input_tensor = input_tensor.unsqueeze(0)  # Add batch dimension

        # Move the input tensor to the same device as the model
        input_tensor = input_tensor.to(device)

        # Forward pass through the model
        with torch.no_grad():
            prediction = DiseasePredictor(input_tensor)
        
        probabilities = F.softmax(prediction[:, 7:11], dim=1)
        predicted_probability, predicted_classes = probabilities.max(1)
        predicted_classes = predicted_classes.item()
        plant_type, disease_status = idx_to_class[predicted_classes]
        predicted_probability = predicted_probability.item() * 100

        # Store the prediction in the list
        predictions.append((plant_type, disease_status, predicted_probability))

        # Sleep for a short duration before capturing the next frame
        time.sleep(1)

except KeyboardInterrupt:
    # Handle KeyboardInterrupt (e.g., when the user interrupts the cell execution)
    pass

finally:
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

# Analyze accumulated predictions
if predictions:
    # Calculate the average confidence and make a final decision
    avg_confidence = sum(p[2] for p in predictions) / len(predictions)
    final_decision = max(predictions, key=lambda x: x[2])  # Choose the prediction with the highest confidence

    print("Final Decision:")
    print("Plant Type: ", final_decision[0])
    print("Disease Status: ", final_decision[1])
    print(f'Average Confidence in Disease Assessment: {avg_confidence:.6f}%')
else:
    print("No predictions were made.")
