'''
Author: Thyssen Wen
Date: 2021-05-30 11:22:37
LastEditors: Thyssen Wen
LastEditTime: 2021-05-30 15:51:32
Description: run function in multi process function
FilePath: /DLLG-2021-BUG-CV/Python/multiProcess/runProcess.py
'''
import cv2
import numpy as np
import logging
import time
import multiprocessing
import armor.proposal as proposal
import armor.classify as classify
import config.config as config
import shot.angleSlove as shot
from multiProcess.runFunc import armorDetetorFunc

class color():
    """
    enermy color define enum
    """
    BLUE = 0
    RED = 1

class hitModel():
    armor = 0
    energy = 1


def readCameraProcess(img_queue,flag_list,recorder_flag):
    while flag_list[0] == False:
        pass

def readVideoProcess(img_queue,flag_list,recorder_flag):
    # 导入数据集
    video_path = './DataSet/video/smallDataset.mp4'
    capture = cv2.VideoCapture(video_path)

    if recorder_flag == True:
        fps = capture.get(cv2.CAP_PROP_FPS)
        size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video_writer = cv2.VideoWriter('./Debug/outputVideo.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    # 统计帧数
    frameCnt = 1

    while flag_list[0] == False:
        #run
        if capture.isOpened():
            success,img=capture.read() # img 就是一帧图片
            if not success:break # 当获取完最后一帧就结束
            
            logging.info("Process "+str(frameCnt)+" frame")
            # run program
            img_queue.put(img)
            if recorder_flag == True:
                video_writer.write(img)
            frameCnt = frameCnt + 1
    
    capture.release()
    if recorder_flag == True:
        video_writer.release()

def readPictureProcess(img_queue,flag_list,recorder_flag):
    #run
    for picture_number in range(1,6):
        if flag_list[0] == False:
            break
        image_path = './DataSet/picture/picture'+str(picture_number)+'.jpg'
        img = cv2.imread(image_path)
        # 统计图片数
        frameCnt = 1

        logging.info("Process "+str(frameCnt)+" frame")
        # run program
        img_queue.put(img)
        logging.info("Finish Process "+str(frameCnt)+" frame")
        if recorder_flag == True:
            image_write_path = './Debug/picture'+str(picture_number)+'.jpg'
            cv2.imwrite(image_write_path,img)

def serialProcess(serial_conn,flag_list):

    while flag_list[0] == False:
        pass

def infantryDetetorProcess(img_queue,detetor_conn,flag_list):
    enermy_color = color.BLUE
    classifier = classify.Classifier()
    hit_model = hitModel.armor
    hit_prob_thres = float(config.getConfig("shot", "hit_prob_thres"))
    logging.info('infantry Detector initial success!')
    # TODOs: serial recept color and hit model
    if enermy_color == color.BLUE:
        logging.info("enermy color set BLUE!")
    elif enermy_color == color.RED:
        logging.info("enermy color set RED!")
    else:
        logging.error("error enermy color!Use BLUE default")
        
    while flag_list[0] == False:
        # TODOs: serial control
        pass
        img = img_queue.get()
        if hit_model == hitModel.armor:
            # hit armor process
            logging.info('hit model set to hit armor')
            proposal_ROIs = proposal.proposal_ROIs(enermy_color)
            armorDetetorFunc(img,classifier,proposal_ROIs,hit_prob_thres)
        elif hit_model == hitModel.energy:
            logging.info('hit model set to hit energy')
            pass
        else:
            logging.error("hit model set error!Use hit armor default!")
            proposal_ROIs = proposal.proposal_ROIs(enermy_color)
            armorDetetorFunc(img,classifier,proposal_ROIs,hit_prob_thres)

def sentryDetetorProcess(img_queue,detetor_conn,flag_list):
    enermy_color = color.BLUE
    classifier = classify.Classifier()
    hit_prob_thres = float(config.getConfig("shot", "hit_prob_thres"))
    logging.info('sentry Detector initial success!')

    # TODOs: serial recept color and hit model
    if enermy_color == color.BLUE:
        logging.info("enermy color set BLUE!")
    elif enermy_color == color.RED:
        logging.info("enermy color set RED!")
    else:
        logging.error("error enermy color!Use BLUE default")
    logging.info('hit model set to hit armor')

    while flag_list[0] == False:
        img = img_queue.get()
        proposal_ROIs = proposal.proposal_ROIs(enermy_color)
        armorDetetorFunc(img,classifier,proposal_ROIs,hit_prob_thres)

def heroDetetorProcess(img_queue,detetor_conn,flag_list):
    enermy_color = color.BLUE
    classifier = classify.Classifier()
    hit_prob_thres = float(config.getConfig("shot", "hit_prob_thres"))
    logging.info('hero Detector initial success!')
    # TODOs: serial recept color and hit model
    if enermy_color == color.BLUE:
        logging.info("enermy color set BLUE!")
    elif enermy_color == color.RED:
        logging.info("enermy color set RED!")
    else:
        logging.error("error enermy color!Use BLUE default")
    logging.info('hit model set to hit armor')

    while flag_list[0] == False:
        img = img_queue.get()
        proposal_ROIs = proposal.proposal_ROIs(enermy_color)
        armorDetetorFunc(img,classifier,proposal_ROIs,hit_prob_thres)
