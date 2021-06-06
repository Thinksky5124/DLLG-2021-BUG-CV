'''
Author: Thyssen Wen
Date: 2021-06-04 20:34:30
LastEditors: Tongbh111
LastEditTime: 2021-06-05 23:51:42
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
        self.svm_model_path = config.getConfig("energy", "svm_model_path")
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
        # TODO: add predict functions to match the speed of rotation(Kalman Filter)
        # main process of energy detection
        processImage = self.preImageProcess_hsv(img)
        logging.info("pre Process Image using hsv color space success!")
        target_x, target_y = self.findAndfilterContours(processImage)
        logging.info("target is x: " + str(target_x) + " y: " + str(target_y))


    def findAndfilterContours(self,img):
        """
        Function for detect the windmills in the image

        Find all the contours in the image
        Transform the ROI with a proper area into regular rectangle
        Judge the type of the ROI with SVM
        Find sub contours of the ROI, get the center point we need to strike
        The output is a tuple(int, int), the center point of armor

        Args:
            img (cv::mat): src image

        Returns:
            target_x, target_y (tuple(int, int)): center point of armor
        """
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
                    # 将所得能量机关扇叶图像送入SVM识别器中
                    type = self.judgeEnergyType(warped_img)
                    if type == 1 and hierarchy[0][i][2] > 0:
                        strike_area = cv2.minAreaRect(contours[hierarchy[0][i][2]])
                        target_x, target_y = strike_area[0]
                        cv2.circle(imgdraw, (int(target_x), int(target_y)), 10, (0,0,255), -1)
                    cv2.imshow("imgdraw", imgdraw)

        return target_x, target_y
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
        The output is a binary mat with one color

        Args:
            img (cv::mat): src image

        Returns:
            image_result (cv::mat): pre process image
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

    def judgeEnergyType(self, img):
        """
        Judge the type of the energy windmill

        Use Hog descriptor to get the feature of image input
        Load trained SVM model to predict type
        Output the predict type(1 for windmill need to strike, 2 for already striken)

        Args:
            img (cv::mat): src image

        Returns:
            predict (int): predict result of the SVM
        """
        # 计算输入图像的HOG特征
        winSize = (48, 48)
        blockSize = (16, 16)
        blockStride = (8, 8)
        cellSize = (8, 8)
        nbins = 9
        img = cv2.resize(img, (48, 48))
        hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins, 1, -1,
                                cv2.HOGDescriptor_L2Hys, 0.2, False, cv2.HOGDescriptor_DEFAULT_NLEVELS)
        hog_data = hog.compute(img)
        # int转换为float类型， 防止报错，并作转置，输入SVM的数据大小为(1,900)
        hog_data = hog_data.astype(np.float32)
        hog_data = np.transpose(hog_data)
        # 创建SVM 当前执行一次识别需要重新读取一次，考虑将其放入init函数中
        svm = cv2.ml.SVM_load(self.svm_model_path)
        # predict为SVM识别结果 1为待击打 2为已击打
        _, predict = cv2.ml_StatModel.predict(svm, hog_data)
        return predict

