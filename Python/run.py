'''
Author: Thyssen Wen
Date: 2021-05-27 21:42:29
LastEditors: Thyssen Wen
LastEditTime: 2021-05-28 20:47:10
Description: run script
FilePath: \DLLG-2021-BUG-CV\Python\run.py
'''

import cv2
import numpy as np
import logging
import armor.proposal as proposal
import armor.classify as classify
import logger.logger as logger
import config.config as config

class color():
    """
    enermy color define enum
    """
    BLUE = 0
    RED = 1

def armorDeteting(img,enermy_color):
    classifier = classify.Classifier()
    proposal_ROIs = proposal.proposal_ROIs(enermy_color)

    armorDetetorProcessd


def armorDetetorProcessd(img,Classifier,proposal_ROIs):
    # if enermy_color != color.BLUE and enermy_color != color.RED:
        # logging.error("error enemy color!Use White default")
    ROIs = proposal_ROIs.proposal(img)
    if len(ROIs) > 1:
        for bbox in ROIs:#遍历所有的轮廓
            [x , y, w, h] = bbox.rectangle
            #在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,),3)
            ROI_img = img[y:y+h, x:x+w]
            ROI_img = cv2.cvtColor(ROI_img,cv2.COLOR_BGR2GRAY)


    cv2.imshow("img",img)
    cv2.waitKey(10)
    
    return img