'''
Author: Thyssen Wen
Date: 2021-05-26 17:17:36
LastEditors: Thyssen Wen
LastEditTime: 2021-05-27 21:02:39
Description: python implement main script
FilePath: \DLLG-2021-BUG-CV\Python\mian.py
'''
import cv2
import numpy as np
import logging
import armor.proposal as proposal
import logger.logger as logger
import config.config as config

def mian_read_video():
    # 导入数据集
    video_path = './DataSet/video/smallDataset.mp4'
    capture = cv2.VideoCapture(video_path)
    # 回显视频
    fps = capture.get(cv2.CAP_PROP_FPS)
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter('./Debug/outputVideo.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size,False)

    while capture.isOpened():
        success,img=capture.read() # img 就是一帧图片
        if not success:break # 当获取完最后一帧就结束
        # 寻找装甲板
        proposal_ROIs = proposal.proposal_ROIs(img,3)
        for i in proposal_ROIs.ROIs:#遍历所有的轮廓
            x,y,w,h = cv2.boundingRect(i)#将轮廓分解为识别对象的左上角坐标和宽、高
            #在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,),3)
        
        cv2.imshow('img', img)
        cv2.waitKey(5)
        video_writer.write(img)
    # 释放空间
    video_writer.release()
    capture.release()

def mian_read_picture():
    for picture_number in range(1,6):
        image_path = './DataSet/picture/picture'+str(picture_number)+'.jpg'
        img = cv2.imread(image_path)
        contours = proposal.proposal_hsv(img,0)
        for i in contours:#遍历所有的轮廓
            x,y,w,h = cv2.boundingRect(i)#将轮廓分解为识别对象的左上角坐标和宽、高
            #在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,),3)
        
        image_write_path = './Debug/picture'+str(picture_number)+'.jpg'
        cv2.imwrite(image_write_path,img)

if  __name__ == '__main__':
    logger.init_logging()
    logging.info('Application Start!')
    mian_read_video()
    logging.info('Application Finish!')