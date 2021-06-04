'''
Author: Thyssen Wen
Date: 2021-06-04 20:34:30
LastEditors: Thyssen Wen
LastEditTime: 2021-06-04 21:09:54
Description: energy hit module
FilePath: \DLLG-2021-BUG-CV\Python\energy\energy.py
'''
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
        self.x = x
        self.y = y
        self.centerPoint_x,self.centerPoint_y = self.centerPoint(x,y,w,h)
        self.rectangle = [self.x,self.y,self.width,self.height]
    
    def centerPoint(self,x,y,w,h):
        return x+w//2,y+h//2
    
    def getArea(self):
        return self.width*self.height
        
class Energy():
    def __init__(self,enermy_color):
        self.enermy_color = enermy_color
        self.energy_armor_area_min = int(config.getConfig("energy", "energy_armor_area_min_threshold"))
        self.energy_armor_area_max= int(config.getConfig("energy", "energy_armor_area_max_threshold"))
        if self.enermy_color == color.BLUE:
            blue_hmin = int(config.getConfig("energy", "hsv_blue_hmin"))
            blue_hmax = int(config.getConfig("energy", "hsv_blue_hmax"))
            blue_smin = int(config.getConfig("energy", "hsv_blue_smin"))
            blue_smax = int(config.getConfig("energy", "hsv_blue_smax"))
            blue_vmin = int(config.getConfig("energy", "hsv_blue_vmin"))
            blue_vmax = int(config.getConfig("energy", "hsv_blue_vmax"))
            self.Lower = np.array([blue_hmin, blue_smin, blue_vmin])#要识别颜色的下限
            self.Upper = np.array([blue_hmax, blue_smax, blue_vmax])#要识别的颜色的上限
            self.binaryThreshold = config.getConfig("energy", "blue_binaryThreshold")
        elif self.enermy_color == color.RED:
            red_hmin = int(config.getConfig("energy", "hsv_red_hmin"))
            red_hmax = int(config.getConfig("energy", "hsv_red_hmax"))
            red_smin = int(config.getConfig("energy", "hsv_red_smin"))
            red_smax = int(config.getConfig("energy", "hsv_red_smax"))
            red_vmin = int(config.getConfig("energy", "hsv_red_vmin"))
            red_vmax = int(config.getConfig("energy", "hsv_red_vmax"))
            self.Lower = np.array([red_hmin, red_smin, red_vmin])#要识别颜色的下限
            self.Upper = np.array([red_hmax, red_smax, red_vmax])#要识别的颜色的上限
            self.binaryThreshold = config.getConfig("energy", "red_binaryThreshold")
        else:
            self.Lower = np.array([0, 0, 221])#要识别颜色的下限
            self.Upper = np.array([180, 30, 255])#要识别的颜色的上限
        
    def foundHitleave(self,img):
        # process
        processImage = self.preImageProcess_hsv(img)
        logging.info("pre Process Image using hsv color space success!")
        hitLeaves = self.findAndfilterContours(processImage)
        logging.info("find "+str(len(hitLeaves))+" lightBars in current frame")
        
        return hitLeaves

    def findAndfilterContours(self,img):
        # initial
        filterContours=[]

        # 找轮廓
        contours, _ = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours:#遍历所有的轮廓
            x,y,w,h = cv2.boundingRect(i)#将轮廓分解为识别对象的左上角坐标和宽、高
            if w*h > self.energy_armor_area_min and w*h < self.energy_armor_area_max:
                filterContours.append(Rectangle(x,y,w,h))
        return filterContours
    
    def preImageProcess_hsv(self,img):
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
        mask = cv2.inRange(hsv, self.Lower, self.Upper)
        
        # 二值化
        ret,binary = cv2.threshold(mask,int(255*self.binaryThreshold),255,cv2.THRESH_BINARY)

        # 开闭操作
        erosion = cv2.erode(binary,kernel)
        dilation = cv2.dilate(erosion,kernel)
        dilation = cv2.dilate(dilation,kernel)
        erosion = cv2.erode(dilation,kernel)
        
        return erosion