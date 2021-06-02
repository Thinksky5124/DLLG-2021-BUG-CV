'''
Author: Thyssen Wen
Date: 2021-05-27 21:42:29
LastEditors: Thyssen Wen
LastEditTime: 2021-06-02 15:12:08
Description: run singal process script
FilePath: /DLLG-2021-BUG-CV/Python/multiProcess/runFunc.py
'''

import cv2
import numpy as np
import logging
import time
import camera.camera as camera
import armor.proposal as proposal
import armor.classify as classify
import config.config as config
import shot.shot as shot

def armorDetetorFunc(img,classifier,proposal_ROIs,hit_prob_thres):
    # proposal ROI
    ROIs = proposal_ROIs.proposal(img)
    # use classifier to detect
    if len(ROIs) > 1:
        ROI_imgs = []
        for bbox in ROIs:
            [x , y, w, h] = bbox.rectangle
            # draw rectangle in show image
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,),1)
            # crop ROI from image
            ROI_img = img[y:y+h, x:x+w]
            ROI_img = cv2.cvtColor(ROI_img,cv2.COLOR_BGR2GRAY)
            ROI_imgs.append(ROI_img)
        # predict and get max prob ROI
        ROI_index,armor_type,prob = classifier.predicts(ROI_imgs)
        if prob > hit_prob_thres:
            armor_hit = ROIs[ROI_index]
            armor_hit.armorType = armor_type
            [x , y, w, h] = armor_hit.rectangle
            
            # draw rectangle in show image
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,),2)
            cv2.putText(img,'armor_type:'+str(armor_hit.armorType),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

            # shot command
            # shot.angleSlove(armor_hit)
    
    return img
