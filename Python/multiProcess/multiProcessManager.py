'''
Author: Thyssen Wen
Date: 2021-05-30 10:45:42
LastEditors: Thyssen Wen
LastEditTime: 2021-05-30 15:33:57
Description: multi process managr module
FilePath: /DLLG-2021-BUG-CV/Python/multiProcess/multiProcessManager.py
'''
import cv2
import numpy as np
import logging
import multiProcess.runProcess as run
import multiprocessing


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

def multiProcessManager(getImageModel_args,runModel_args,recordmodel_args):
    logging.info('Application Start!')
    process_list = []
    # initial communication class
    img_queue = multiprocessing.Queue()
    flag_list = multiprocessing.Manager().list()
    serial_conn, detetor_conn = multiprocessing.Pipe()

    if recordmodel_args == recordModel.no_record:
        recorder_flag = False
        logging.info('No recored!')
        pass
    elif recordmodel_args == recordModel.record:
        recorder_flag = True
        logging.info('recorder flag initialzie!')
    else:
        logging.error('set recordmodel_args error!')
        return
    
    if getImageModel_args == getImageModel.fromCamera:
        getImage = multiprocessing.Process(target=run.readCameraProcess,args=(img_queue,flag_list,recorder_flag,),name='getImageProcess')
        process_list.append(getImage)
        logging.info('getImage from camera Process initialzie!')
    elif getImageModel_args == getImageModel.fromVideo:
        getImage = multiprocessing.Process(target=run.readVideoProcess,args=(img_queue,flag_list,recorder_flag,),name='getImageProcess')
        process_list.append(getImage)
        logging.info('getImage from video Process initialzie!')
    elif getImageModel_args == getImageModel.fromImage:
        getImage = multiprocessing.Process(target=run.readPictureProcess,args=(img_queue,flag_list,recorder_flag,),name='getImageProcess')
        process_list.append(getImage)
        logging.info('getImage from image Process initialzie!')
    else:
        logging.error('set getImageModel_args error!')
        return

    serial = multiprocessing.Process(target=run.serialProcess,args=(serial_conn,flag_list,),name='serialProcess')
    process_list.append(serial)
    logging.info('serial process initialzie!')
    
    if runModel_args == runModel.infantry:
        detector = multiprocessing.Process(target=run.infantryDetetorProcess,args=(img_queue,detetor_conn,flag_list,),name='detectorProcess')
        process_list.append(detector)
        logging.info('infantry detector Process initialzie!')
    elif runModel_args == runModel.sentry:
        detector = multiprocessing.Process(target=run.sentryDetetorProcess,args=(img_queue,detetor_conn,flag_list,),name='detectorProcess')
        process_list.append(detector)
        logging.info('sentry detector Process initialzie!')
    elif runModel_args == runModel.hero:
        detector = multiprocessing.Process(target=run.heroDetetorProcess,args=(img_queue,detetor_conn,flag_list,),name='detectorProcess')
        process_list.append(detector)
        logging.info('hero detector Process initialzie!')
    else:
        logging.error('set runModel_args error!')
        return

    process_exit_flag = False
    flag_list.append(process_exit_flag)
    for process in process_list:
        # ! Set up daemon
        process.setDaemon(True) 
        # ! Process start
        process.start()
        logging.info(process.name+' Start!')
    
    # ! Process exit manager
    try:
        while True:
            key_num = cv2.waitKey(500)
            if chr(key_num) == 'q':
                logging.warning('Application press key to Exit!')
                flag_list[0]=True
                for process in process_list:
                    process.join()
                    logging.info(process.name+' Exit!')
                logging.info('Application Exit!')
    except KeyboardInterrupt:
        logging.warning('Application kill Exit!')
        print('Application kill Exit!')