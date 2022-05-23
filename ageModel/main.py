import torch
import matplotlib.pyplot as plt
import torchvision
import cv2
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image


class ConvolutionalNetwork_age(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1,  25, 3, 1)
        self.conv2 = nn.Conv2d(25, 50, 3, 1)
        self.conv3 = nn.Conv2d(50, 75, 3, 1)
        self.conv4 = nn.Conv2d(75, 100, 3, 1)
        self.fc1 = nn.Linear(10*10*100, 2000) #(((((200-2)/2)-2))/2)-2))/2) = 23,.. (4->10)
        self.fc2 = nn.Linear(2000, 200)
        self.fc3 = nn.Linear(200,7) #7-liczba klas wieków

    def forward(self, X):
        X = F.relu(self.conv1(X))
        X = F.max_pool2d(X, 2, 2)
        X = F.relu(self.conv2(X))
        X = F.max_pool2d(X, 2, 2)
        X = F.relu(self.conv3(X))
        X = F.max_pool2d(X, 2, 2)
        X = F.relu(self.conv4(X))
        X = F.max_pool2d(X, 2, 2)
        X = X.view(-1, 10*10*100)
        X = F.relu(self.fc1(X))
        X = F.relu(self.fc2(X))
        X = self.fc3(X)
        return F.softmax(X, dim=1)


def load_image(path):
    img = torchvision.io.read_image(path, torchvision.io.ImageReadMode.GRAY)
    img = img.reshape((200, 200), 1)
    img = img.numpy()
    img = img/255
    img = torch.Tensor(img).view(-1, 200, 200)
    return img


def predict_gender(model, image):
    with torch.no_grad():
        net_out = model(image.to(DEVICE_AGE).view(-1, 1, 200, 200))[0]  # returns a list,
        predicted_class = torch.argmax(net_out)
    return predicted_class.item()


MODELPATH_AGE = "model_age.pth"
IMGPATH_AGE = "testimg2.jpg"
DEVICE_AGE = "cuda" if torch.cuda.is_available() else "cpu"

model_age_ = ConvolutionalNetwork_age()
# model_age_.load_state_dict(torch.load(MODELPATH_AGE, map_location=DEVICE_AGE))
# model_age_.to(DEVICE_AGE)
# testimg = load_image(IMGPATH_AGE)
# output = predict_gender(model_age_, testimg)
# print(output)
# 0 = 8-15
# 1 = 15-20
# 2 = 20-30
# 3 = 30-45
# 4 = 45-55
# 5 = 55-70
# 6 = 70-..
