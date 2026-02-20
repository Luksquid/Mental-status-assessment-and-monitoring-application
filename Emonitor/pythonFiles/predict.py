import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.nn.functional import relu, softmax
from PIL import Image
import pandas as pd
import cv2
import numpy as np
import sys
import json
import datetime
import os

DEVICE = torch.device("cpu")

class EmotionLeNet(nn.Module):
    def __init__(self):
        super(EmotionLeNet, self).__init__()

        self.convolutional_1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.batch_narm_1 = nn.BatchNorm2d(32)
        self.convolutional_2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.batch_narm_2 = nn.BatchNorm2d(64)
        self.convolutional_3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.batch_narm_3 = nn.BatchNorm2d(128)

        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.dropout = nn.Dropout(0.5)

        self.linear_1 = nn.Linear(128*8*8, 256)
        self.linear_2 = nn.Linear(256, 128)
        self.linear_3 = nn.Linear(128, 7)

    def forward(self, x):
        x = self.pool(relu(self.batch_narm_1(self.convolutional_1(x))))
        x = self.pool(relu(self.batch_narm_2(self.convolutional_2(x))))
        x = self.pool(relu(self.batch_narm_3(self.convolutional_3(x))))

        x = x.view(-1, 128*8*8)
        x = relu(self.linear_1(x))
        x = self.dropout(x)
        x = relu(self.linear_2(x))
        x = self.dropout(x)
        x = self.linear_3(x)

        return x


transformation = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
])

current_time = datetime.datetime.now()


def predict(image, model):
    model.eval()

    gray_image = cv2.cvtColor(image.astype("uint8"), cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    try:
        x, y, w, h = face_cascade.detectMultiScale(gray_image, 1.1, 5)[0]
    except:
        print(json.dumps({"message": 'No face detected', 'time': current_time.strftime("%H:%M:%S")}))
        sys.exit()

    image = image[y:y+h, x:x+w].astype("uint8")

    image = Image.fromarray(image)

    input_tensor = transformation(image).unsqueeze(0) 

    with torch.no_grad():
        logits = model(input_tensor) 

    probs = softmax(logits, dim=1) * 100
    _, predicted_class = torch.max(probs, 1)

    predicted_class = int(predicted_class)

    labels = {'angry': 0, 'disgust': 1, 'fear': 2, 'happy': 3, 'neutral': 4, 'sad': 5, 'surprise': 6}
    labels = dict(zip(labels.values(), labels.keys()))

    probs = probs.tolist()[0]
    probs = {labels[i]: round(probs[i], 4) for i in range(7)}
    probs = dict(sorted(probs.items(), key=lambda item: item[1], reverse=True))

    return probs, labels[predicted_class]

input_data = sys.stdin.read()
data = json.loads(input_data)

model = torch.load(os.path.join(os.path.dirname(__file__), '.', '', 'model.pth'), map_location=torch.device("cpu"), weights_only=False)

probs, predicted = predict(np.array(data['image']), model)

probs_keys = list(probs.keys())
probs_values = list(probs.values())

now_time = current_time.strftime("%H:%M:%S")

if probs_values[0] - probs_values [1] > 10:
    print(json.dumps({"message": f'Detection emotion: {probs_keys[0]}', 'time': now_time}))

    emotions_df = pd.DataFrame([{'emotion': predicted, 'time': now_time, 'probability': probs_values[0]}])
    emotions_df.to_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'session_statistics.csv'), 
                       mode='a', header=False, index=False)

else:
    print(json.dumps({"message": 'No emotion detected', 'time': now_time}))

