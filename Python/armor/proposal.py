'''
Author: Thyssen Wen
Date: 2021-05-27 16:12:35
LastEditors: Thyssen Wen
LastEditTime: 2021-05-30 13:57:20
Description: proposal ROI python implement
FilePath: /DLLG-2021-BUG-CV/Python/armor/proposal.py
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

class Armor_bbox:
    def __init__(self,Rectangle_a,Rectangle_b,armorType):
        armor_bbox_size_param = float(config.getConfig("proposal", "armor_bbox_size_param"))
        image_height = int(config.getConfig("image_size", "image_height"))
        additional_length = int(armor_bbox_size_param*max(Rectangle_a.height,Rectangle_b.height))

        self.armorType = armorType
        self.centerPoint_x = (Rectangle_a.centerPoint_x + Rectangle_b.centerPoint_x)//2
        self.centerPoint_y = (Rectangle_a.centerPoint_y + Rectangle_b.centerPoint_y)//2
        self.x = min(Rectangle_a.centerPoint_x,Rectangle_b.centerPoint_x)
        self.y = max(min(Rectangle_a.y,Rectangle_b.y) - additional_length,0)
        self.width = abs(Rectangle_a.centerPoint_x - Rectangle_b.centerPoint_x)
        if self.y + max(Rectangle_a.height,Rectangle_b.height) + additional_length*2 > image_height:
            self.height = image_height - self.y
        else:
            self.height = max(Rectangle_a.height,Rectangle_b.height) + additional_length*2
        self.rectangle = [self.x,self.y,self.width,self.height]
    
    def getArea(self):
        return self.width*self.height


class proposal_ROIs:
    """
    proposal ROI class return ROI in every frame
    """
    def __init__(self,enermy_color):
        self.enermy_color = enermy_color
        self.nms_threshold = float(config.getConfig("proposal", "nms_threshold"))
        self.lightBars_min_area = int(config.getConfig("proposal", "lightBars_area_min_threshold"))
        self.lightBars_max_area = int(config.getConfig("proposal", "lightBars_area_max_threshold"))
        self.hightDistance_threshold = float(config.getConfig("proposal", "lightBars_hightDistance"))
        self.centerDistance_min_threshold = float(config.getConfig("proposal", "lightBars_centerDistance_min"))
        self.centerDistance_max_threhold = float(config.getConfig("proposal", "lightBars_centerDistance_max"))
        self.lengthRate_min_threhold = float(config.getConfig("proposal", "lightBars_lengthRate_min"))
        self.lengthRate_max_threhold = float(config.getConfig("proposal", "lightBars_lengthRate_max"))
        if self.enermy_color == color.BLUE:
            blue_hmin = int(config.getConfig("proposal", "hsv_blue_hmin"))
            blue_hmax = int(config.getConfig("proposal", "hsv_blue_hmax"))
            blue_smin = int(config.getConfig("proposal", "hsv_blue_smin"))
            blue_smax = int(config.getConfig("proposal", "hsv_blue_smax"))
            blue_vmin = int(config.getConfig("proposal", "hsv_blue_vmin"))
            blue_vmax = int(config.getConfig("proposal", "hsv_blue_vmax"))
            self.Lower = np.array([blue_hmin, blue_smin, blue_vmin])#要识别颜色的下限
            self.Upper = np.array([blue_hmax, blue_smax, blue_vmax])#要识别的颜色的上限
            self.binary_threshold = config.getConfig("proposal", "blue_binary_threshold")
        elif self.enermy_color == color.RED:
            red_hmin = int(config.getConfig("proposal", "hsv_red_hmin"))
            red_hmax = int(config.getConfig("proposal", "hsv_red_hmax"))
            red_smin = int(config.getConfig("proposal", "hsv_red_smin"))
            red_smax = int(config.getConfig("proposal", "hsv_red_smax"))
            red_vmin = int(config.getConfig("proposal", "hsv_red_vmin"))
            red_vmax = int(config.getConfig("proposal", "hsv_red_vmax"))
            self.Lower = np.array([red_hmin, red_smin, red_vmin])#要识别颜色的下限
            self.Upper = np.array([red_hmax, red_smax, red_vmax])#要识别的颜色的上限
            self.binary_threshold = config.getConfig("proposal", "red_binary_threshold")
        else:
            self.Lower = np.array([0, 0, 221])#要识别颜色的下限
            self.Upper = np.array([180, 30, 255])#要识别的颜色的上限
    
    def proposal(self,img):
        # initialize param
        ROIs_nms = []
        
        # process
        processImage = self.preImageProcess_hsv(img)
        logging.info("pre Process Image using hsv color space success!")
        lightBars = self.findAndfilterContours(processImage)
        logging.info("find "+str(len(lightBars))+" lightBars in current frame")
        if len(lightBars) >= 2:
            ROIs_nms = self.proposal_bbox(lightBars)
            logging.info("find "+str(len(ROIs_nms))+" ROIs in current frame")
            # nms process
            if len(ROIs_nms) >= 2:
                logging.info("Start nms to reduce armor bbox")
                ROIs_nms = self.non_max_suppress(ROIs_nms,self.nms_threshold)
                logging.info("remain "+str(len(ROIs_nms))+" ROIs after nms")
        
        return ROIs_nms

    def findAndfilterContours(self,img):
        # initial
        filterContours=[]

        # 找轮廓
        contours, _ = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours:#遍历所有的轮廓
            x,y,w,h = cv2.boundingRect(i)#将轮廓分解为识别对象的左上角坐标和宽、高
            if h>=w and w*h > self.lightBars_min_area and w*h < self.lightBars_max_area:
                filterContours.append(Rectangle(x,y,w,h))
        return filterContours

    def proposal_bbox(self,lightBars):
        #initilazie param
        proposal_bbox = []

        #filter proposal
        for i in range(len(lightBars) - 1):
            for j in range(i+1,len(lightBars)):
                lightBars_hightDistance = abs(lightBars[i].centerPoint_y - lightBars[j].centerPoint_y)
                lightBars_centerDistance = abs(lightBars[i].centerPoint_x - lightBars[j].centerPoint_x)
                lightBars_lengthRate = abs(lightBars[i].centerPoint_y / lightBars[j].centerPoint_y)
                if lightBars_hightDistance < self.hightDistance_threshold and \
                    lightBars_centerDistance > self.centerDistance_min_threshold and \
                    lightBars_centerDistance < self.centerDistance_max_threhold and \
                    lightBars_lengthRate > self.lengthRate_min_threhold and \
                    lightBars_lengthRate < self.lengthRate_max_threhold :
                    proposal_bbox.append(Armor_bbox(lightBars[i],lightBars[j],0))
        return proposal_bbox


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
        ret,binary = cv2.threshold(mask,0,255,cv2.THRESH_BINARY)

        # 开闭操作
        erosion = cv2.erode(binary,kernel)
        dilation = cv2.dilate(erosion,kernel)
        dilation = cv2.dilate(dilation,kernel)
        erosion = cv2.erode(dilation,kernel)
        
        return erosion

    def preImageProcess_rgb(self,img):
        # 初始化
        kernel = np.ones((3,5),np.uint8)
        # 分离颜色
        if self.enermy_color == color.BLUE:
            color_channel = img[...,0]
        elif self.enermy_color == color.RED:
            color_channel = img[...,1]
        else:
            color_channel = img[...,0]
            logging.error("error enemy color!Use BLUE default")
        
        # 二值化
        ret,binary = cv2.threshold(color_channel,int(self.binary_threshold),255,cv2.THRESH_BINARY)

        # 开闭操作
        erosion = cv2.erode(binary,kernel)
        dilation = cv2.dilate(erosion,kernel)
        dilation = cv2.dilate(dilation,kernel)
        erosion = cv2.erode(dilation,kernel)
        
        return erosion

    def non_max_suppress(self, ROIs, thresh):
        """
        non max suppress to remain one bounding box

        Args:
            ROIs (list): list of Armor_bbox
            thresh (float): non max suppress threshold

        Returns:
            list: list of bounding box after non max supress
        
        from:https://zhuanlan.zhihu.com/p/40976906
        """
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        ROIs_nms = []
        
        for armor_bbox in ROIs:#遍历所有的轮廓
            [x , y, w, h] = armor_bbox.rectangle
            x1.append(x)
            y1.append(y)
            x2.append(x+w)
            y2.append(y+h)
        x1 = np.array(x1)
        y1 = np.array(y1)
        x2 = np.array(x2)
        y2 = np.array(y2)
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = areas.argsort()[::-1]
        keep = []

        while order.size > 0:
            i = order[0]
            keep.append(i)#保留当前最大area对应的bbx索引
			#获取所有与当前bbx的交集对应的左上角和右下角坐标，并计算IoU（注意这里是同时计算一个bbx与其他所有bbx的IoU）
            xx1 = np.maximum(x1[i], x1[order[1:]])#最大置信度的左上角坐标分别与剩余所有的框的左上角坐标进行比较，分别保存较大值；因此这里的xx1的维数应该是当前类的框的个数减1
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            inter = np.maximum(0.0, xx2-xx1+1) * np.maximum(0.0, yy2-yy1+1)
            iou = inter / (areas[i] + areas[order[1:]] - inter)#注意这里都是采用广播机制，同时计算了置信度最高的框与其余框的IoU
            inds = np.where(iou <= thresh)[0]#保留iou小于等于阙值的框的索引值
            order = order[inds + 1]#将order中的第inds+1处的值重新赋值给order；即更新保留下来的索引，加1是因为因为没有计算与自身的IOU，所以索引相差１，需要加上
        for keep_id in keep:
            ROIs_nms.append(ROIs[keep_id])
            
        return ROIs_nms