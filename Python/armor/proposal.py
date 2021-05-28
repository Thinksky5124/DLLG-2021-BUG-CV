'''
Author: Thyssen Wen
Date: 2021-05-27 16:12:35
LastEditors: Thyssen Wen
LastEditTime: 2021-05-28 11:05:37
Description: proposal ROI python implement
FilePath: /DLLG-2021-BUG-CV/Python/armor/proposal.py
'''
from typing import Counter
import cv2
import numpy as np
import logging
import config.config as config

class color():
    """
    enermy color define enum
    """
    BLUE = 0
    RED = 1

class Rectangle:
    def __init__(self,x,y,w,h):
        self.width=w
        self.height=h
        self.centerPont_x,self.centerPont_y = self.centerPoint(x,y,w,h)
    
    def centerPoint(self,x,y,w,h):
        return (x+w)/2,(y+h)/2
    
    def getLength(self):
        return (self.width+self.height)*2
    
    def getArea(self):
        return self.width*self.height


class proposal_ROIs:
    """
    summary
    """
    def __init__(self,img,enermy_color):
        self.ROIs = self.proposal(img,enermy_color)
    
    def proposal(self,img,enermy_color):
        processImage = self.preImageProcess_hsv(img,enermy_color)
        lightBars = self.findAndfilterContours(processImage)
        
        return lightBars

    def findAndfilterContours(self,img):
        # initial
        filterContours=[]
        lightBars_min_area = int(config.getConfig("proposal", "lightBars_area_min_threshold"))
        lightBars_max_area = int(config.getConfig("proposal", "lightBars_area_max_threshold"))
        # 找轮廓
        contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours:#遍历所有的轮廓
            x,y,w,h = cv2.boundingRect(i)#将轮廓分解为识别对象的左上角坐标和宽、高
            if h>=w and w*h > lightBars_min_area and w*h < lightBars_max_area:
                filterContours.append(Rectangle(x,y,w,h))
        return filterContours

    def proposal_bbox(self,lightBars):
        #initilazie param
        hightDistance_threshold = config.getConfig("proposal", "lightBars_hightDistance")
        centerDistance_min_threshold = config.getConfig("proposal", "lightBars_centerDistance_min")
        centerDistance_max_threhold = config.getConfig("proposal", "lightBars_centerDistance_max")
        lengthRate_min_threhold = config.getConfig("proposal", "lightBars_lengthRate_min")
        lengthRate_max_threhold = config.getConfig("proposal", "lightBars_lengthRate_max")
        #filter proposal
        for i in range(len(lightBars) - 1):
            for j in range(i+1,len(lightBars)):
                lightBars_hightDistance = abs(lightBars[i].centerPont_y - lightBars[j].centerPont_y)
                lightBars_centerDistance = abs(lightBars[i].centerPont_x - lightBars[j].centerPont_x)
                lightBars_lengthRate = abs(lightBars[i].centerPont_y / lightBars[j].centerPont_y)
                if lightBars_hightDistance < hightDistance_threshold and \
                    lightBars_centerDistance > centerDistance_min_threshold and \
                    lightBars_centerDistance < centerDistance_max_threhold and \
                    lightBars_lengthRate > lengthRate_min_threhold and \
                    lightBars_lengthRate < lengthRate_max_threhold :
                    


    def preImageProcess_hsv(self,img,enermy_color):
        """
        pre process image ready to extract light bars

        Args:
            img (cv::mat): src image
            enermy_color (enum): detetor enermy color

        Returns:
            image (cv::mat): pre process image
        """
        # 初始化
        kernel = np.ones((3,5),np.uint8)
        # 图片预处理
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        # 分离颜色
        if enermy_color == color.BLUE:
            blue_hmin = int(config.getConfig("proposal", "hsv_blue_hmin"))
            blue_hmax = int(config.getConfig("proposal", "hsv_blue_hmax"))
            blue_smin = int(config.getConfig("proposal", "hsv_blue_smin"))
            blue_smax = int(config.getConfig("proposal", "hsv_blue_smax"))
            blue_vmin = int(config.getConfig("proposal", "hsv_blue_vmin"))
            blue_vmax = int(config.getConfig("proposal", "hsv_blue_vmax"))
            Lower = np.array([blue_hmin, blue_smin, blue_vmin])#要识别颜色的下限
            Upper = np.array([blue_hmax, blue_smax, blue_vmax])#要识别的颜色的上限
        elif enermy_color == color.RED:
            red_hmin = int(config.getConfig("proposal", "hsv_red_hmin"))
            red_hmax = int(config.getConfig("proposal", "hsv_red_hmax"))
            red_smin = int(config.getConfig("proposal", "hsv_red_smin"))
            red_smax = int(config.getConfig("proposal", "hsv_red_smax"))
            red_vmin = int(config.getConfig("proposal", "hsv_red_vmin"))
            red_vmax = int(config.getConfig("proposal", "hsv_red_vmax"))
            Lower = np.array([red_hmin, red_smin, red_vmin])#要识别颜色的下限
            Upper = np.array([red_hmax, red_smax, red_vmax])#要识别的颜色的上限
        else:
            Lower = np.array([0, 0, 221])#要识别颜色的下限
            Upper = np.array([180, 30, 255])#要识别的颜色的上限
        mask = cv2.inRange(hsv, Lower, Upper)
        
        # 二值化
        ret,binary = cv2.threshold(mask,0,255,cv2.THRESH_BINARY)

        # 开闭操作
        erosion = cv2.erode(binary,kernel)
        dilation = cv2.dilate(erosion,kernel)
        dilation = cv2.dilate(dilation,kernel)
        erosion = cv2.erode(dilation,kernel)
        
        return erosion

    def preImageProcess_rgb(self,img,enermy_color):
        # 初始化
        kernel = np.ones((3,5),np.uint8)
        # 分离颜色
        if enermy_color == color.BLUE:
            color_channel = img[...,0]
            binary_threshold = config.getConfig("proposal", "blue_binary_threshold")
        elif enermy_color == color.RED:
            color_channel = img[...,1]
            binary_threshold = config.getConfig("proposal", "red_binary_threshold")
        else:
            color_channel = img[...,0]
            logging.error("error enemy color!Use BLUE default")
        
        # 二值化
        ret,binary = cv2.threshold(color_channel,int(binary_threshold),255,cv2.THRESH_BINARY)

        # 开闭操作
        erosion = cv2.erode(binary,kernel)
        dilation = cv2.dilate(erosion,kernel)
        dilation = cv2.dilate(dilation,kernel)
        erosion = cv2.erode(dilation,kernel)
        
        return erosion