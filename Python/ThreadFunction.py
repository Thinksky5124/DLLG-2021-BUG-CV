'''
Author: Thyssen Wen
Date: 2021-05-27 21:42:29
LastEditors: Thyssen Wen
LastEditTime: 2021-05-29 21:38:16
Description: run script
FilePath: /DLLG-2021-BUG-CV/Python/ThreadFunction.py
'''

import cv2
import numpy as np
import logging
import threading
import armor.proposal as proposal
import armor.classify as classify
import logger.logger as logger
import config.config as config

class color():
    """
    enermy color define enum
    """
    BLUE = 0
    RED = 1

def armorDeteting(img,enermy_color):
    classifier = classify.Classifier()
    proposal_ROIs = proposal.proposal_ROIs(enermy_color)

    armorDetetorProcessd


def armorDetetorProcessd(img,Classifier,proposal_ROIs):
    # if enermy_color != color.BLUE and enermy_color != color.RED:
        # logging.error("error enemy color!Use White default")
    ROIs = proposal_ROIs.proposal(img)
    if len(ROIs) > 1:
        for bbox in ROIs:#遍历所有的轮廓
            [x , y, w, h] = bbox.rectangle
            #在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,),3)
            ROI_img = img[y:y+h, x:x+w]
            ROI_img = cv2.cvtColor(ROI_img,cv2.COLOR_BGR2GRAY)


    cv2.imshow("img",img)
    cv2.waitKey(10)
    
    return img

def read_video():
    # 导入数据集
    global img
    video_path = './DataSet/video/smallDataset.mp4'
    capture = cv2.VideoCapture(video_path)
    # 回显视频
    fps = capture.get(cv2.CAP_PROP_FPS)
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter('./Debug/outputVideo.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    # 统计帧数
    frameCnt = 1

    while capture.isOpened():
        success,img=capture.read() # img 就是一帧图片
        if not success:break # 当获取完最后一帧就结束
        
        logging.info("Process "+str(frameCnt)+" frame")
        # run program
        img = run.runThread(color.WHITE)
        logging.info("Finish Process "+str(frameCnt)+" frame")
        
        frameCnt = frameCnt + 1
        video_writer.write(img)
    # 释放空间
    video_writer.release()
    capture.release()

def read_picture():
    for picture_number in range(1,6):
        global img
        image_path = './DataSet/picture/picture'+str(picture_number)+'.jpg'
        img = cv2.imread(image_path)
        # 统计图片数
        frameCnt = 1

        logging.info("Process "+str(frameCnt)+" picture")
        # run program
        img = run.runThread(color.WHITE)
        logging.info("Finish Process "+str(frameCnt)+" picture")
        
        image_write_path = './Debug/picture'+str(picture_number)+'.jpg'
        cv2.imwrite(image_write_path,img)