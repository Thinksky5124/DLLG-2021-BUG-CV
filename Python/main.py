'''
Author: Thyssen Wen
Date: 2021-05-26 17:17:36
LastEditors: Thyssen Wen
LastEditTime: 2021-06-03 20:38:29
Description: python implement main script
FilePath: /DLLG-2021-BUG-CV/Python/main.py
'''
import cv2
import numpy as np
import logging
import multiProcess.singalProcess as run_singal
import multiProcess.multiProcessManager as run_multi
import multiprocessing
import logger.logger as logger
import os
        
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

class codeStatus():
    debug = 0
    release = 1

if  __name__ == '__main__':
    # set pwd
    os.chdir(os.path.dirname(__file__)+'/../')
    # ! set run args
    Getmodel_args = getImageModel.fromVideo
    Runmodel_args = runModel.infantry
    Recordmodel_args = recordModel.no_record
    CodeStatus_args = codeStatus.debug
    
    # application run
    # ! watch up and change logging file config if change operater systerm 
    logger.init_logging()
    if CodeStatus_args == codeStatus.release:
        logging.info('application set in release model(multiProcess)!')
        # multi process run
        run_multi.multiProcessManager(getImageModel_args = Getmodel_args,runModel_args = Runmodel_args,recordmodel_args = Recordmodel_args)
    elif CodeStatus_args == codeStatus.debug:
        logging.info('application set in debug model(singalProcess)!')
        # signal process run
        run_singal.runSingalProcess(getImageModel_args = Getmodel_args,runModel_args = Runmodel_args,recordmodel_args = Recordmodel_args)
    else:
        logging.error('application set error!')
    