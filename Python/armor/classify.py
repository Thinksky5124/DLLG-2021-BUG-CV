'''
Author: Thyssen Wen
Date: 2021-05-28 17:17:36
LastEditors: Thyssen Wen
LastEditTime: 2021-05-31 18:27:05
Description: python implement small classification model
FilePath: \DLLG-2021-BUG-CV\Python\armor\classify.py
'''
import cv2
import numpy as np
import logging
import config.config as config
import math
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import transforms
from torchvision import datasets

class Classifier():
    def __init__(self):
        self.weight_save_path = config.getConfig("classify", "weight_save_path")
        self.image_size = int(config.getConfig("classify", "image_size"))
        self.Network = Net()
        logging.info("Initialize classifier success!")

        if os.path.exists(self.weight_save_path):
            logging.info("load networ weight success!")
            self.Network = Net()
            self.Network.load_state_dict(torch.load(self.weight_save_path))
        else:
            logging.warning('no load networ weight! Please check train classifier!')
            self.learning_rate = float(config.getConfig("classify", "learning_rate"))
            self.momentum = float(config.getConfig("classify", "momentum"))
            self.criterion = nn.CrossEntropyLoss()
            self.optimizer = optim.SGD(self.Network.parameters(), lr=self.learning_rate, momentum=self.momentum)

    def train(self):
        epoches = int(config.getConfig("classify", "epoches"))
        batch_size = int(config.getConfig("classify", "batch_size"))
        train_set_root = config.getConfig("classify", "train_set_root")
        weight_save_path = config.getConfig("classify", "weight_save_path")
        
        train_data = datasets.ImageFolder(train_set_root,transform=transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize(32),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor()
        ]))
        
        trainloader = torch.utils.data.DataLoader(train_data, batch_size=batch_size,shuffle=True, num_workers=2)
        for epoch in range(epoches):  # loop over the dataset multiple times

            running_loss = 0.0
            for i, data in enumerate(trainloader, 0):
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data

                # zero the parameter gradients
                self.optimizer.zero_grad()

                # forward + backward + optimize
                outputs = self.Network(inputs)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

                # print statistics
                running_loss += loss.item()
                if i % 2000 == 1999:    # print every 2000 mini-batches
                    print('[%d, %5d] loss: %.3f' %
                        (epoch + 1, i + 1, running_loss / 2000))
                    running_loss = 0.0

        print('Finished Training')

        torch.save(self.Network.state_dict(), weight_save_path)

    def collectingDataset(self,imgs):
        save_number = 1
        train_set_root = config.getConfig("classify", "train_set_root")
        for img in imgs:
            img = cv2.resize(img, (self.image_size,self.image_size), interpolation = cv2.INTER_AREA)
            while os.path.exists(train_set_root+'/unclassify/'+str(save_number)+'.jpg'):
                save_number = save_number + 1
            cv2.imwrite(train_set_root+'/unclassify/'+str(save_number)+'.jpg',img)
            save_number = save_number + 1

    def predictProb(self,img):
        img = cv2.resize(img, (self.image_size,self.image_size), interpolation = cv2.INTER_AREA)
        testdata = torch.from_numpy(img)
        testdata = testdata.unsqueeze(0).unsqueeze(0)
        testdata = testdata.to(torch.float32)

        output = self.Network(testdata)
        return output
    
    def predict(self,img):
        """
        predict singal image and return predict class number

        Args:
            img (ndarray): image ready to predict

        Returns:
            int: predict class number
        """
        _, predicted = torch.max(self.predictProb(img), 1)
        return predicted
    
    def predicts(self,imgs):
        """
        predict multi images
        return max prob image number in list and predict class number

        Args:
            imgs (list): list of predicted images

        Returns:
            int: max prob image number in list
            int: predict class number
            float: predict prob
        """
        predicteds = []
        for img in imgs:
            predicteds.append(self.predictProb(img))
        predicteds = torch.cat(predicteds,dim=0)
        values, class_indexes = torch.max(predicteds, 1)
        value, image_index = torch.max(values.unsqueeze(0),1)
        logging.info('predict sucess and extract the best prob bbox')
        return image_index.item(),class_indexes[image_index].item(),value.item()

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 3x3 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.conv2 = nn.Conv2d(6, 16, 3)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 6 * 6, 120)  # 6*6 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.softMax = nn.Softmax(dim=1)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        x= self.softMax(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features