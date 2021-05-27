'''
Author: Thyssen Wen
Date: 2021-05-27 16:12:35
LastEditors: Thyssen Wen
LastEditTime: 2021-05-27 16:45:34
Description: proposal ROI python implement
FilePath: \DLLG-2021-BUG-CV\Python\armor\proposal.py
'''
import cv2
import numpy as np

class enermy_color():
    """
    enermy color define enum
    """
    BLUE = 0
    RED = 1

class proposal:
    """
    summary
    """

def proposal_hsv(img,enermy_color):
    """
    proposal use hsv model

    Args:
        img (cv::mat): src image
        enermy_color (enum): detetor enermy color

    Returns:
        contours var: rect poposal
    """
    # 初始化
    kernel = np.ones((3,5),np.uint8)
    # 图片预处理
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # 分离颜色
    Lower = np.array([100, 50, 150])#要识别颜色的下限
    Upper = np.array([124, 255, 255])#要识别的颜色的上限
    mask = cv2.inRange(hsv, Lower, Upper)
    # 二值化
    ret,binary = cv2.threshold(mask,0,255,cv2.THRESH_BINARY)
    # 开闭操作
    erosion = cv2.erode(binary,kernel)
    dilation = cv2.dilate(erosion,kernel)
    dilation = cv2.dilate(dilation,kernel)
    erosion = cv2.erode(dilation,kernel)
    # 找轮廓
    contours, hierarchy = cv2.findContours(erosion,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return contours

def proposal_hsv(img,enermy_color):
    # 初始化
    kernel = np.ones((3,5),np.uint8)
    # 图片预处理
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # 分离颜色
    Lower = np.array([100, 50, 150])#要识别颜色的下限
    Upper = np.array([124, 255, 255])#要识别的颜色的上限
    mask = cv2.inRange(hsv, Lower, Upper)
    # 二值化
    ret,binary = cv2.threshold(mask,0,255,cv2.THRESH_BINARY)
    # 开闭操作
    erosion = cv2.erode(binary,kernel)
    dilation = cv2.dilate(erosion,kernel)
    dilation = cv2.dilate(dilation,kernel)
    erosion = cv2.erode(dilation,kernel)
    
    return erosion