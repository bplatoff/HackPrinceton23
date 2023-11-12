# HackPrinceton23 - Harvest Hero: Cultivating Innovation
*A code repository for Hack Princeton 2023. Team: Benjmain Platoff, Aaron Lozhkin, Simon Grishin*

Harvest Hero is a scalable IoT device that monitors crop health over time and throughout the season. We leverage advanced sensor data in tandem with deep learning techniques to provide the most accurate crop health reports. Harvest Hero aims to mitigate crop losses, boost yields, and contribute to sustainable agriculture by addressing key pain points in farming. 

## Hardware

### RaspberryPI
- Interfaces with the primary client to send real time video and sensor data to the machine learning model
- Capable of sending data to an Azure IOT Hub for scalability and processing
- Aggregates data from the Arduino board and cleans it for exporting

### Arduino Uno
- Aggregates humidity, temperature, light levels, and soil moisture from the arduino sensors

## Disease Detection with Deep Learning

![image](https://github.com/bplatoff/HackPrinceton23/assets/23532191/368d9d18-6fd3-4569-ac34-a8aa769c0cda)

Crop Type: Tomato
Disease Status: Bacterial Spot

Model Prediction: Tomato with Bacterial Spot

![image](https://github.com/bplatoff/HackPrinceton23/assets/23532191/60be15aa-11d0-46ea-9101-2526b634ba5a)

Crop Type: Apple
Disease Status: Cedar Apple Rust

Model Prediction: Apple with Cedar Rust

![image](https://github.com/bplatoff/HackPrinceton23/assets/23532191/dce702ee-9def-4e32-94c0-56ef9a4a6277)
Crop Type: Bell Pepper
Disease Status: Healthy

Model Prediction: Healthy Bell Pepper

### Model Architecture

We leveraged Microsoft's [ResNet50](https://huggingface.co/microsoft/resnet-50) and implemented a transfer learning scheme that applied ResNet's incredible classification abilities to learn on the [New Plant Diseases Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)

ResNet utilizes a sequence of convolutional layers, skip layers, and pooling layers to learn patterns within images. Trained on ImageNet with 1000 object classes and 1,281,167 training images, this model has become incredible efficient in noticing the correct features of an image to classify it. Thus, with **transfer learning** we can easily adapt ResNet's architecture and model parameters to learn various plant diseases.

![image](https://github.com/bplatoff/HackPrinceton23/assets/23532191/368efdd6-b796-443b-be79-32724842d0e0)

After just 3 epochs, we achieved the [first iteration](DiseasedCropClassifier_3epochs_firstIteration_92ValAcc.pth) of our model which achieved a 92% accuracy on the validation dataset and took roughly 20 minutes to train. However, later in the project we decided to run the model for 5 epoch and obtain the [second iteration](DiseasedCropClassifier_5epochs_secondIteration.pth) which achieved a 96% accuracy on teh validation dataset. This second iteration took roughly 35 minutes to train.

![image](https://github.com/bplatoff/HackPrinceton23/assets/23532191/9e627dd0-874a-43e4-977e-c657984b48da)

Crop Monitoring Dashboard: 

![image](https://github.com/bplatoff/HackPrinceton23/assets/124309228/6d68cd86-a0a5-466a-ab1b-b49f6e71b935)

