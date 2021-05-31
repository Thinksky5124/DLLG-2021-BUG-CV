'''
Author: Thyssen Wen
Date: 2021-05-28 19:18:51
LastEditors: Thyssen Wen
LastEditTime: 2021-05-31 18:12:34
Description: train classifier script
FilePath: \DLLG-2021-BUG-CV\Python\train_classifier.py
'''
import cv2
import numpy as np
from torchvision.datasets.folder import ImageFolder
import config.config as config
import logger.logger as logger
import logging
import time
import armor.classify as classify
import armor.proposal as proposal
import torch

class color():
    """
    enermy color define enum
    """
    BLUE = 0
    RED = 1

class train_model():
    train_network = 0
    collect_Dataset = 1

class getImageModel():
    fromCamera = 0
    fromVideo = 1
    fromImage = 2
    
def train():
    classes = ('1', '2', '3','4', '5', '6')
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

def read_video(enermy_color,classifier):
    # 导入数据集
    video_path = './DataSet/video/smallDataset.mp4'
    capture = cv2.VideoCapture(video_path)
    # 回显视频
    fps = capture.get(cv2.CAP_PROP_FPS)
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter('./Debug/outputVideo.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    # 统计帧数
    frameCnt = 1

    #run
    while capture.isOpened():
        success,img=capture.read() # img 就是一帧图片
        if not success:break # 当获取完最后一帧就结束
        
        # Start time
        start = time.time()
        logging.info("Process "+str(frameCnt)+" frame")
        
        # run program
        # proposal ROI
        proposal_ROIs = proposal.proposal_ROIs(enermy_color)
        ROIs = proposal_ROIs.proposal(img)
        # use classifier to detect
        if len(ROIs) > 1:
            ROI_imgs = []
            for bbox in ROIs:
                [x , y, w, h] = bbox.rectangle
                # draw rectangle in show image
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,),1)
                # crop ROI from image
                ROI_img = img[y:y+h, x:x+w]
                ROI_img = cv2.cvtColor(ROI_img,cv2.COLOR_BGR2GRAY)
                ROI_imgs.append(ROI_img)
            classifier.collectingDataset(ROI_imgs)
        logging.info("Finish Process "+str(frameCnt)+" frame")
        # End time
        end = time.time()
        # Time elapsed
        seconds = end - start
        if seconds > 0:
            fps = int(1 / seconds)
        else:
            fps = 100
        cv2.putText(img,'fps:'+str(fps),(550,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

        cv2.imshow("show_img",img)
        cv2.waitKey(10)
        frameCnt = frameCnt + 1
        video_writer.write(img)
    # 释放空间
    video_writer.release()
    capture.release()

def read_camera(enermy_color,classifier):
    # 导入数据集
    video_path = './DataSet/video/smallDataset.mp4'
    capture = cv2.VideoCapture(video_path)
    # 回显视频
    fps = capture.get(cv2.CAP_PROP_FPS)
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter('./Debug/outputVideo.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    # 统计帧数
    frameCnt = 1

    #run
    while capture.isOpened():
        success,img=capture.read() # img 就是一帧图片
        if not success:break # 当获取完最后一帧就结束
        
        # Start time
        start = time.time()
        logging.info("Process "+str(frameCnt)+" frame")
        
        # run program
        # proposal ROI
        proposal_ROIs = proposal.proposal_ROIs(enermy_color)
        ROIs = proposal_ROIs.proposal(img)
        # use classifier to detect
        if len(ROIs) > 1:
            ROI_imgs = []
            for bbox in ROIs:
                [x , y, w, h] = bbox.rectangle
                # draw rectangle in show image
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,),1)
                # crop ROI from image
                ROI_img = img[y:y+h, x:x+w]
                ROI_img = cv2.cvtColor(ROI_img,cv2.COLOR_BGR2GRAY)
                ROI_imgs.append(ROI_img)
            classifier.collectingDataset(ROI_imgs)
        logging.info("Finish Process "+str(frameCnt)+" frame")
        # End time
        end = time.time()
        # Time elapsed
        seconds = end - start
        if seconds > 0:
            fps = int(1 / seconds)
        else:
            fps = 100
        cv2.putText(img,'fps:'+str(fps),(550,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

        cv2.imshow("show_img",img)
        cv2.waitKey(10)
        frameCnt = frameCnt + 1
        video_writer.write(img)
    # 释放空间
    video_writer.release()
    capture.release()

def collectDataset(enermy_color,getImageModel_args):
    logger.init_logging()
    logging.info('collecting dataset Start!')
    classifier = classify.Classifier()

    if getImageModel_args == getImageModel.fromVideo:
        read_video(enermy_color,classifier)
    elif getImageModel_args == getImageModel.fromCamera:
        read_camera(enermy_color,classifier)
    else:
        logging.error('set getImageModel error!')
    
    logging.info('collecting dataset Finish!')



if  __name__ == '__main__':
    # ! set model
    model_args = train_model.collect_Dataset
    enermy_color = color.BLUE
    getImageModel_args = getImageModel.fromVideo

    # run
    if model_args == train_model.train_network:
        train()
    elif model_args == train_model.collect_Dataset:
        collectDataset(enermy_color,getImageModel_args)
    else:
        logging.error('set model error !')
