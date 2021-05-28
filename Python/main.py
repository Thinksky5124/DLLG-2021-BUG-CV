'''
Author: Thyssen Wen
Date: 2021-05-26 17:17:36
LastEditors: Thyssen Wen
LastEditTime: 2021-05-28 20:46:35
Description: python implement main script
FilePath: \DLLG-2021-BUG-CV\Python\main.py
'''
import cv2
import numpy as np
import logging
import threading
import run
import logger.logger as logger

class color():
    """
    enermy color define enum
    """
    BLUE = 0
    RED = 1
    WHITE = 2

class VisionDetetorThread(threading.Thread):
    def run(self):
        self.armorDeteting()

    def armorDeteting(self):
        while(thread_run_flag):
            lock=threading.Lock()
            lock.acquire()
            image = img
            lock.release()
            armorDetetorProcessd()

class ImageGetThread(threading.Thread):
    def run(self):
        self.armorDeteting()

    def armorDeteting(self):
        while(thread_run_flag):
            lock=threading.Lock()
            lock.acquire()
            image = img
            lock.release()
            armorDetetorProcessd()

class ShotCommandThread(threading.Thread):
    def run(self):
        self.armorDeteting()

    def armorDeteting(self):
        while(thread_run_flag):
            lock=threading.Lock()
            lock.acquire()
            image = img
            lock.release()
            armorDetetorProcessd()

def runThread(enermy_color):
    detetor_thread = VisionDetetorThread()
    detetor_thread.start()
    img = armorDetetorProcessd(image,enermy_color)
    return img

def mian_read_video():
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

def mian_read_picture():
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

if  __name__ == '__main__':
    logger.init_logging()
    logging.info('Application Start!')
    runThread()
    logging.info('Application Finish!')