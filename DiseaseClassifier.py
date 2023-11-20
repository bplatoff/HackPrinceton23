import os
import torch
import torch.nn as nn
import torch.nn.init as init
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms

from PIL import Image
from tqdm import tqdm

import torch.nn.functional as F
from torchvision.models import resnet50, ResNet50_Weights

class ResNetClassifer(nn.Module):
    def __init__(self, num_classes):
        super(ResNetClassifer, self).__init__()
        self.num_classes = num_classes

        self.idx_to_class = {0: ('Apple', 'Apple Scab'),
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

        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),  # Assuming your model expects images of size (224, 224)
            transforms.ToTensor(),
        ])

        # Use a pre-trained ResNet model from Hugging Face
        self.resnet_model = resnet50(weights=ResNet50_Weights.DEFAULT)

        for param in self.resnet_model.parameters():
            param.requires_grad = False

        # Add a global average pooling layer
        self.global_avg_pooling = nn.AdaptiveAvgPool2d(1)

        # Fully connected layers for embedding
        fc_inputs = self.resnet_model.fc.in_features
        self.resnet_model.fc = nn.Sequential(
            nn.Linear(fc_inputs, 256),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(256, num_classes), 
            nn.LogSoftmax(dim=1)
        )

    def forward(self, x):
        return self.resnet_model(x)
    
    def loadModel(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if not torch.cuda.is_available(): print("WARNING: Model will run extremely slow on cpu")
        print(os.getcwd())
        if torch.cuda.is_available():
            self.load_state_dict(torch.load("DiseasedCropClassifier_5epochs_secondIteration.pth"))
        else:
            print("WARNING: Model will run extremely slow on cpu. If on colab, go to Runtime->Change Runtime Type->Hardware Accelerator->GPU.")
            self.load_state_dict(torch.load("DiseasedCropClassifier_5epochs_secondIteration.pth", map_location=torch.device('cpu')))

        self.to(self.device)
        self.eval()
    
    def apply(self, x):
        # Utility function for returning all data reprsented by one pass of the model
        # input: RGB frame from a camera

        input_tensor = self.transform(x)
        input_tensor = input_tensor.unsqueeze(0)  # Add batch dimension

        # Move the input tensor to the same device as the model
        input_tensor = input_tensor.to(self.device)

        # Forward pass through the model
        with torch.no_grad():
            prediction = self.forward(input_tensor)
        
        probabilities = F.softmax(prediction, dim=1)
        predicted_probability, predicted_classes = probabilities.max(1)
        predicted_classes = predicted_classes.item()
        plant_type, disease_status = self.idx_to_class[predicted_classes]
        predicted_probability = predicted_probability.item() * 100

        return plant_type, disease_status, predicted_probability