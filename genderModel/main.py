import torch
import matplotlib.pyplot as plt
import torchvision
import cv2
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image


class ConvolutionalNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # self.model_path = model_path
        # self.img_path = img_path
        # self.output = 0
        self.conv1 = nn.Conv2d(1, 30, 3, 1)
        self.conv2 = nn.Conv2d(30, 60, 3, 1)
        self.conv3 = nn.Conv2d(60, 100, 3, 1)
        self.conv4 = nn.Conv2d(100,150, 3, 1)
        self.fc1 = nn.Linear(10*10*150, 2000) #(((((200-2)/2)-2))/2)-2))/2) = 23,.. (4->10)
        self.fc2 = nn.Linear(2000, 300)
        self.fc3 = nn.Linear(300,2) #8-liczba klas wieków

    def forward(self, X):
        X = F.relu(self.conv1(X))
        X = F.max_pool2d(X, 2, 2)
        X = F.relu(self.conv2(X))
        X = F.max_pool2d(X, 2, 2)
        X = F.relu(self.conv3(X))
        X = F.max_pool2d(X, 2, 2)
        X = F.relu(self.conv4(X))
        X = F.max_pool2d(X, 2, 2)
        X = X.view(-1, 10*10*150)
        X = F.relu(self.fc1(X))
        X = F.relu(self.fc2(X))
        X = self.fc3(X)
        return torch.sigmoid(X)


def load_image(path):
    img = torchvision.io.read_image(path, torchvision.io.ImageReadMode.GRAY)
    img = img.reshape((200, 200), 1)
    img = img.numpy()
    img = img/255
    img = torch.Tensor(img).view(-1, 200, 200)
    return img


def predict_gender(model, image):
    with torch.no_grad():
        net_out = model(image.to(DEVICE).view(-1, 1, 200, 200))[0]  # returns a list,
        predicted_class = torch.argmax(net_out)
        print('net_out: ', net_out)
    return predicted_class.item()


MODELPATH = "model.pth"
IMGPATH = "images.jpg"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model_ = ConvolutionalNetwork()
# model_.load_state_dict(torch.load(MODELPATH, map_location=DEVICE))
# model_.to(DEVICE)
# testimg = load_image(IMGPATH)
# output = predict_gender(model_, testimg)
# print(output)   # 0 = 'male'; 1 = 'female'
