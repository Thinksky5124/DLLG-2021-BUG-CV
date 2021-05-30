'''
Author: Thyssen Wen
Date: 2021-05-28 19:18:51
LastEditors: Thyssen Wen
LastEditTime: 2021-05-30 12:14:53
Description: train classifier script
FilePath: /DLLG-2021-BUG-CV/Python/train_classifier.py
'''
import cv2
import numpy as np
from torchvision.datasets.folder import ImageFolder
import config.config as config
import logger.logger as logger
import logging
import armor.classify as classify
import torch


if  __name__ == '__main__':
    classes = ('0', '1', '2', '3','4', '5', '6', '7', '8', '9')
    logger.init_logging()
    logging.info('Networ Train Start!')
    classifier = classify.Classifier()
    classifier.train()

    img = cv2.imread("./DataSet/Classifier_testset/test1.png")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    classifier_trained = classify.Classifier()
    predicted = classifier_trained.predict(img)
    print('Predicted: ', ' '.join('%5s' % classes[predicted]))
    
    logging.info('Networ Train Finish!')