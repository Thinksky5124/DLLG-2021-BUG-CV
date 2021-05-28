'''
Author: Thyssen Wen
Date: 2021-05-26 17:17:36
LastEditors: Thyssen Wen
LastEditTime: 2021-05-28 10:37:41
Description: python implement main script
FilePath: /DLLG-2021-BUG-CV/Python/main.py
'''
import cv2
import numpy as np
import logging
import run
import logger.logger as logger

class color():
    """
    enermy color define enum
    """
    BLUE = 0
    RED = 1

def mian_read_video():
    # 导入数据集
    video_path = './DataSet/video/smallDataset.mp4'
    capture = cv2.VideoCapture(video_path)
    # 回显视频
    fps = capture.get(cv2.CAP_PROP_FPS)
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter('./Debug/outputVideo.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    while capture.isOpened():
        success,img=capture.read() # img 就是一帧图片
        if not success:break # 当获取完最后一帧就结束
        # run program
        img = run.armorDetetorThread(img,3)
        video_writer.write(img)
    # 释放空间
    video_writer.release()
    capture.release()

def mian_read_picture():
    for picture_number in range(1,6):
        image_path = './DataSet/picture/picture'+str(picture_number)+'.jpg'
        img = cv2.imread(image_path)
        # run program
        img = run.armorDetetorThread(img,0)
        
        image_write_path = './Debug/picture'+str(picture_number)+'.jpg'
        cv2.imwrite(image_write_path,img)

if  __name__ == '__main__':
    logger.init_logging()
    logging.info('Application Start!')
    mian_read_video()
    logging.info('Application Finish!')