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
        self.energy_armor_area_max = int(config.getConfig("energy", "energy_armor_area_max_threshold"))
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
            red_hmin_1 = int(config.getConfig("energy", "hsv_red_hmin_1"))
            red_hmax = int(config.getConfig("energy", "hsv_red_hmax"))
            red_hmax_1 = int(config.getConfig("energy", "hsv_red_hmax_1"))
            red_smin = int(config.getConfig("energy", "hsv_red_smin"))
            red_smax = int(config.getConfig("energy", "hsv_red_smax"))
            red_vmin = int(config.getConfig("energy", "hsv_red_vmin"))
            red_vmax = int(config.getConfig("energy", "hsv_red_vmax"))
            self.Lower = np.array([red_hmin, red_smin, red_vmin])#要识别颜色的下限
            self.Upper = np.array([red_hmax, red_smax, red_vmax])#要识别的颜色的上限
            self.Lower2 = np.array([red_hmin_1, red_smin, red_vmin])
            self.Upper2 = np.array([red_hmax_1, red_smax, red_vmax])
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
        imgdraw = img.copy()
        imgdraw = cv2.cvtColor(imgdraw, cv2.COLOR_GRAY2BGR)
        # initial
        filterContours=[]
        # 找轮廓
        contours, hierarchy = cv2.findContours(img, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            for i in range(0, len(contours)):
                # 算法参考 link: https://blog.csdn.net/u010750137/article/details/100825793
                # 找最小外接矩形
                box_i = cv2.minAreaRect(contours[i])
                # 获得矩形四个顶点
                box_points = cv2.boxPoints(box_i)
                for j in range(0,4):
                    # 绘制矩形
                    # 不能使用rectangle函数
                    cv2.line(imgdraw, (int(box_pts[j][0]), int(box_pts[j][1])),
                             (int(box_pts[(j+1)%4][0]), int(box_pts[(j+1)%4][1])), (0,255,0), 2)
                # 计算宽度和长度
                width = np.linalg.norm(box_pts[0] - box_pts[1])
                height = np.linalg.norm(box_pts[1] - box_pts[2])

                # 若宽度大于长度，变换顶点坐标
                if(width > height):
                    box_pts = np.roll(box_pts, -1, axis=0)
                    width, height = height, width

                # 检测到合适的矩形区域
                if(height*width > 3500 and height*width < 5000):
                    # 使用透视变换，矫正为规则矩形
                    # 源矩形坐标
                    rect_src = np.array([[box_pts[0][0], box_pts[0][1]],
                                         [box_pts[1][0], box_pts[1][1]],
                                         [box_pts[2][0], box_pts[2][1]],
                                         [box_pts[3][0], box_pts[3][1]]
                                         ], dtype='float32')
                    # 目标矩形坐标
                    rect_dst = np.array([[0, 0],
                                         [width, 0],
                                         [width, height],
                                         [0, height]
                                        ], dtype='float32')
                    # 计算透视变换矩阵
                    perspective_mat = cv2.getPerspectiveTransform(rect_src, rect_dst)
                    warped_img = cv2.warpPerspective(img, perspective_mat, (int(width), int(height)))
                    cv2.imshow("roi", warped_img)

        # for i in contours:#遍历所有的轮廓
        #     x,y,w,h = cv2.boundingRect(i)#将轮廓分解为识别对象的左上角坐标和宽、高
        #     if w*h > self.energy_armor_area_min and w*h < self.energy_armor_area_max:
        #         filterContours.append(Rectangle(x,y,w,h))
        # return filterContours

    
    def preImageProcess_hsv(self,img):
        """
        Pre-process the image input

        Transform the input image into hsv model.
        Use filters to remove the irrelative color pixels

        Args:
            img (cv::mat): src image

        Returns:
            image (cv::mat): pre process image
        """
        # 初始化
        kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))

        # 图片预处理
        # 过滤方法和HSV阈值参考2018东林方案
        # link: https://github.com/moxiaochong/NEFU-ARES-Vison-Robomaster2018/blob/eb9daf94110312598a64c469f194eb9366d340c9/ARES/Template/Armor_Detector.cpp#L219
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        # 取v通道，仅在该通道上进行阈值操作
        img_binary = img_hsv[:,:,2]
        ret, thr = cv2.threshold(img_binary, int(255*self.binaryThreshold), 255, cv2.THRESH_BINARY)
        img_dilate = cv2.dilate(thr, kernel1)
        if self.enermy_color == color.BLUE:
            mask = cv2.inRange(img_hsv, self.Lower, self.Upper)

        else:
            # 红色需要根据两个阈值进行判断，使用或运算将两个区域相加
            mask1 = cv2.inRange(img_hsv, self.Lower, self.Upper)
            mask2 = cv2.inRange(img_hsv, self.Lower2, self.Upper2)
            mask = cv2.bitwise_or(mask1, mask2)
        # 掩膜操作
        img_masked = cv2.bitwise_not(mask, thr)
        # 反色操作 背景色为黑色
        img_masked = cv2.bitwise_not(img_masked, img_masked)
        img_result = cv2.cv2.morphologyEx(img_masked, cv2.MORPH_CLOSE, kernel2)
        
        return img_result










