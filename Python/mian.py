'''
Author: Thyssen Wen
Date: 2021-05-26 17:17:36
LastEditors: Thyssen Wen
LastEditTime: 2021-05-27 16:39:44
Description: python implement main script
FilePath: \DLLG-2021-BUG-CV\Python\mian.py
'''
import cv2
import numpy as np
import Python.armor.proposal

if  __name__ == '__main__':
    # 导入数据集
    video_path = './DataSet/smallDataset.mp4'
    capture = cv2.VideoCapture(video_path)
    # 回显视频
    fps = capture.get(cv2.CAP_PROP_FPS)
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter('./CVVerifyPython/outputVideo.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    while capture.isOpened():
        success,img=capture.read() # img 就是一帧图片
        if not success:break # 当获取完最后一帧就结束
        # HSV
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        Lower = np.array([100, 50, 150])#要识别颜色的下限
        Upper = np.array([124, 255, 255])#要识别的颜色的上限
        mask = cv2.inRange(hsv, Lower, Upper)
        ret,binary = cv2.threshold(mask,0,255,cv2.THRESH_BINARY)
        erosion = cv2.erode(binary,kernel)
        dilation = cv2.dilate(erosion,kernel)
        dilation = cv2.dilate(dilation,kernel)
        erosion = cv2.erode(dilation,kernel)
        #RGB
        
        
        
        contours, hierarchy = cv2.findContours(erosion,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours:#遍历所有的轮廓
            x,y,w,h = cv2.boundingRect(i)#将轮廓分解为识别对象的左上角坐标和宽、高
            #在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,),3)
        video_writer.write(img)
    # 释放空间
    video_writer.release()
    capture.release()