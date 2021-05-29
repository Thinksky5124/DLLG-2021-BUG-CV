'''
Author: Thyssen Wen
Date: 2021-05-26 17:17:36
LastEditors: Thyssen Wen
LastEditTime: 2021-05-29 23:06:21
Description: python implement main script
FilePath: /DLLG-2021-BUG-CV/Python/main.py
'''
from types import ModuleType
import cv2
import numpy as np
import logging
import ThreadFunction as run
import multiprocessing
import logger.logger as logger

class color():
    """
    enermy color define enum
    """
    BLUE = 0
    RED = 1
    WHITE = 2

class getImageModel():
    fromCamera = 0
    fromVedio = 1
    fromImage = 2

class recordModel():
    record = 0
    no_record = 1
    
class runModel():
    sentry = 0
    infantry = 1
    hero = 2

class MyProcess(multiprocessing.Process):
    """
    mutiProcess base class

    Args:
        multiprocessing (Process): base Process derive
    """
    def __init__(self, function, args, name=''):
        multiprocessing.Process.__init__(self)
        self.name = name
        self.function = function
        self.args = args
        
    def run(self):
        self.function()

def main(getImageModel_args,runModel_args,recordmodel_args):
    logger.init_logging()
    logging.info('Application Start!')
    process_list = []
    
    if getImageModel_args == getImageModel.fromCamera:
        getImage = MyProcess(function=run.read_camera,args=[],name='getImageProcess')
        process_list.append(getImage)
        logging.info('getImage from camera Process initialzie!')
    elif getImageModel_args == getImageModel.fromVedio:
        getImage = MyProcess(function=run.read_video,args=[],name='getImageProcess')
        process_list.append(getImage)
        logging.info('getImage from video Process initialzie!')
    elif getImageModel_args == getImageModel.fromImage:
        getImage = MyProcess(function=run.read_picture,args=[],name='getImageProcess')
        process_list.append(getImage)
        logging.info('getImage from image Process initialzie!')
    else:
        logging.error('set getImageModel_args error!')
        return

    serial = MyProcess(function=run.serial,args=[],name='serialProcess')
    process_list.append(serial)
    logging.info('serial process initialzie!')
    
    if runModel_args == runModel.infantry:
        detector = MyProcess(function=run.infantryDetetor,args=[],name='detectorProcess')
        process_list.append(detector)
        logging.info('infantry detector Process initialzie!')
    elif runModel_args == runModel.sentry:
        detector = MyProcess(function=run.sentryDetetor,args=[],name='detectorProcess')
        process_list.append(detector)
        logging.info('sentry detector Process initialzie!')
    elif runModel_args == runModel.hero:
        detector = MyProcess(function=run.heroDetetor,args=[],name='detectorProcess')
        process_list.append(detector)
        logging.info('hero detector Process initialzie!')
    else:
        logging.error('set runModel_args error!')
        return
    
    if recordmodel_args == recordModel.no_record:
        logging.info('No recored!')
        pass
    elif recordmodel_args == recordModel.record:
        recorder = MyProcess(function=run.record,args=[],name='recorderProcess')
        process_list.append(recorder)
        logging.info('recorder Process Process initialzie!')
    else:
        logging.error('set recordmodel_args error!')
        return

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
                # TODOs: use message to kill process
                process_exit_flag = True
                for process in process_list:
                    process.join()
                    logging.info(process.name+' Exit!')
                logging.info('Application Exit!')
    except KeyboardInterrupt:
        logging.warning('Application kill Exit!')
        print('Application kill Exit!')
        
    

if  __name__ == '__main__':
    Getmodel_args = getImageModel.fromVedio
    Runmodel_args = runModel.infantry
    Recordmodel_args = recordModel.no_record
    main(getImageModel_args = Getmodel_args,runModel_args = Runmodel_args,recordmodel_args = Recordmodel_args)
    