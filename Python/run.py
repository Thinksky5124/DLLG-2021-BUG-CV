'''
Author: Thyssen Wen
Date: 2021-05-27 21:42:29
LastEditors: Thyssen Wen
LastEditTime: 2021-05-27 22:06:02
Description: run script
FilePath: /DLLG-2021-BUG-CV/Python/run.py
'''

import cv2
import numpy as np
import logging
import armor.proposal as proposal
import logger.logger as logger
import config.config as config

def armorDetetorThread(img,enermy_color):
    proposal_ROIs = proposal.proposal_ROIs(img,enermy_color)
    for bbox in proposal_ROIs.ROIs:#遍历所有的轮廓
        [x , y, w, h] = bbox
        #在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,),3)
    
    return img