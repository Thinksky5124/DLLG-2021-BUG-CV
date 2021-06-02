'''
Author: Thyssen Wen
Date: 2021-06-02 15:04:44
LastEditors: Thyssen Wen
LastEditTime: 2021-06-02 20:21:29
Description: singal process function
FilePath: /DLLG-2021-BUG-CV/Python/multiProcess/singalProcess.py
'''
import cv2
import numpy as np
import logging
import time
import camera.camera as camera
import armor.proposal as proposal
import armor.classify as classify
import config.config as config
import shot.angleSlove as shot
import multiProcess.runFunc as run

class color():
    """
    enermy color define enum
    """
    BLUE = 0
    RED = 1

class getImageModel():
    fromCamera = 0
    fromVideo = 1
    fromImage = 2

class recordModel():
    record = 0
    no_record = 1
    
class runModel():
    sentry = 0
    infantry = 1
    hero = 2

class hitModel():
    armor = 0
    energy = 1

class heroDetetor():
    def __init__(self):
        self.enermy_color = color.BLUE
        self.classifier = classify.Classifier()
        self.hit_prob_thres = float(config.getConfig("shot", "hit_prob_thres"))
        logging.info('hit model set to hit armor')
        logging.info('hero Detector initial success!')
    
    def Deteting(self,img):
        # TODOs: serial recept color and hit model
        if self.enermy_color == color.BLUE:
            logging.info("enermy color set BLUE!")
        elif self.enermy_color == color.RED:
            logging.info("enermy color set RED!")
        else:
            logging.error("error enermy color!Use BLUE default")
        
        proposal_ROIs = proposal.proposal_ROIs(self.enermy_color)
        show_img = run.armorDetetorFunc(img,self.classifier,proposal_ROIs,self.hit_prob_thres)

        return show_img

class sentryDetetor():
    def __init__(self):
        self.enermy_color = color.BLUE
        self.classifier = classify.Classifier()
        self.hit_prob_thres = float(config.getConfig("shot", "hit_prob_thres"))
        logging.info('hit model set to hit armor')
        logging.info('sentry Detector initial success!')
        
    
    def Deteting(self,img):
        # TODOs: serial recept color and hit model
        if self.enermy_color == color.BLUE:
            logging.info("enermy color set BLUE!")
        elif self.enermy_color == color.RED:
            logging.info("enermy color set RED!")
        else:
            logging.error("error enermy color!Use BLUE default")
        
        proposal_ROIs = proposal.proposal_ROIs(self.enermy_color)
        show_img = run.armorDetetorFunc(img,self.classifier,proposal_ROIs,self.hit_prob_thres)

        return show_img

class infantryDetetor():
    def __init__(self):
        # ! must modify
        self.enermy_color = color.BLUE
        self.classifier = classify.Classifier()
        self.hitModel = hitModel.armor
        self.hit_prob_thres = float(config.getConfig("shot", "hit_prob_thres"))
        logging.info('infantry Detector initial success!')
    
    def Deteting(self,img):
        # TODOs: serial recept color and hit model
        if self.enermy_color == color.BLUE:
            logging.info("enermy color set BLUE!")
        elif self.enermy_color == color.RED:
            logging.info("enermy color set RED!")
        else:
            logging.error("error enermy color!Use BLUE default")
        
        if self.hitModel == hitModel.armor:
            # hit armor process
            logging.info('hit model set to hit armor')
            proposal_ROIs = proposal.proposal_ROIs(self.enermy_color)
            show_img = run.armorDetetorFunc(img,self.classifier,proposal_ROIs,self.hit_prob_thres)
        elif self.hitModel == hitModel.energy:
            logging.info('hit model set to hit energy')
            pass
        else:
            logging.error("hit model set error!Use hit armor default!")
            proposal_ROIs = proposal.proposal_ROIs(self.enermy_color)
            show_img = run.armorDetetorFunc(img,self.classifier,proposal_ROIs,self.hit_prob_thres)

        return show_img

def read_video(runModel_args,recordmodel_args):
    # 导入数据集
    video_path = './DataSet/video/smallDataset.mp4'
    capture = cv2.VideoCapture(video_path)
    if recordmodel_args == recordModel.record:
        # 回显视频
        fps = capture.get(cv2.CAP_PROP_FPS)
        size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video_writer = cv2.VideoWriter('./Debug/outputVideo.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    # 统计帧数
    frameCnt = 1

    # initial detector
    if runModel_args == runModel.infantry:
        Detetor = infantryDetetor()
    elif runModel_args == runModel.sentry:
        Detetor = sentryDetetor()
    elif runModel_args == runModel.hero:
        Detetor = heroDetetor()
    else:
        logging.error('set runModel_args error!')
        return
    #run
    while capture.isOpened():
        success,img=capture.read() # img 就是一帧图片
        if not success:break # 当获取完最后一帧就结束
        
        # Start time
        start = time.time()
        logging.info("Process "+str(frameCnt)+" frame")
        # run program
        show_img  = Detetor.Deteting(img)
        logging.info("Finish Process "+str(frameCnt)+" frame")
        # End time
        end = time.time()
        # Time elapsed
        seconds = end - start
        if seconds > 0:
            fps = int(1 / seconds)
        else:
            fps = 100
        cv2.putText(show_img,'fps:'+str(fps),(550,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

        # cv2.imshow("show_img",show_img)
        # cv2.waitKey(10)
        frameCnt = frameCnt + 1
        if recordmodel_args == recordModel.record:
            video_writer.write(img)
    # 释放空间
    capture.release()
    if recordmodel_args == recordModel.record:
        video_writer.release()

def read_picture(runModel_args):
    # initial detector
    if runModel_args == runModel.infantry:
        Detetor = infantryDetetor()
    elif runModel_args == runModel.sentry:
        Detetor = sentryDetetor()
    elif runModel_args == runModel.hero:
        Detetor = heroDetetor()
    else:
        logging.error('set runModel_args error!')
        return
    #run
    for picture_number in range(1,6):
        image_path = './DataSet/picture/picture'+str(picture_number)+'.jpg'
        img = cv2.imread(image_path)
        # 统计图片数
        frameCnt = 1

        # Start time
        start = time.time()
        logging.info("Process "+str(frameCnt)+" frame")
        # run program
        show_img  = Detetor.Deteting(img)
        logging.info("Finish Process "+str(frameCnt)+" frame")
        # End time
        end = time.time()
        # Time elapsed
        seconds = end - start
        fps = 1 / seconds
        cv2.putText(show_img,'fps:'+str(fps),(600,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        
        cv2.imshow("show_img",show_img)
        cv2.waitKey(10)

        image_write_path = './Debug/picture'+str(picture_number)+'.jpg'
        cv2.imwrite(image_write_path,img)

def read_camera(runModel_args,recordmodel_args):
    # init camera
    cameraCapture = camera.Camera()
    
    if recordmodel_args == recordModel.record:
        # 回显视频
        fps = 32
        size = (640, 480)
        video_writer = cv2.VideoWriter('./Debug/outputVideo.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
        logging.info('model set record data!')

    # 统计帧数
    frameCnt = 1

    # initial detector
    if runModel_args == runModel.infantry:
        Detetor = infantryDetetor()
    elif runModel_args == runModel.sentry:
        Detetor = sentryDetetor()
    elif runModel_args == runModel.hero:
        Detetor = heroDetetor()
    else:
        logging.error('set runModel_args error!')
        return
    #run
    success,img = cameraCapture.getfromCamera()
    while success:
        # Start time
        start = time.time()
        logging.info("Process "+str(frameCnt)+" frame")
        # run program
        show_img  = Detetor.Deteting(img)
        logging.info("Finish Process "+str(frameCnt)+" frame")
        # End time
        end = time.time()
        # Time elapsed
        seconds = end - start
        fps = 1 / seconds
        cv2.putText(show_img,'fps:'+str(fps),(600,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        # cv2.imshow("show_img",show_img)
        # cv2.waitKey(10)
        frameCnt = frameCnt + 1
        success,img = cameraCapture.getfromCamera()
        if recordmodel_args == recordModel.record:
            video_writer.write(img)
    # 释放空间
    cameraCapture.camera_release()
    if recordmodel_args == recordModel.record:
        video_writer.release()

def runSingalProcess(getImageModel_args,runModel_args,recordmodel_args):
    logging.info('Application Start!')
    if getImageModel_args == getImageModel.fromCamera:
        logging.info('getImage from camera')
        read_camera(runModel_args,recordmodel_args)
    elif getImageModel_args == getImageModel.fromVideo:
        logging.info('getImage from video')
        read_video(runModel_args,recordmodel_args)
    elif getImageModel_args == getImageModel.fromImage:
        logging.info('getImage from picture')
        read_picture(runModel_args)
    else:
        logging.error('set getImageModel_args error!')
    logging.info('Application Exit!')