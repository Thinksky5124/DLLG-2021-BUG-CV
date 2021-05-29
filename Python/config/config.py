'''
Author: Thyssen Wen
Date: 2021-05-27 18:41:30
LastEditors: Thyssen Wen
LastEditTime: 2021-05-29 11:53:09
Description: config module
FilePath: /DLLG-2021-BUG-CV/Python/config/config.py
'''
import configparser
import os
import cloghandler

#获取config配置文件
def getConfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/config.conf'
    config.read(path)
    return config.get(section, key)