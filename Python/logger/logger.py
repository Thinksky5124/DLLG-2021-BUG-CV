'''
Author: Thyssen Wen
Date: 2021-05-27 17:18:56
LastEditors: Thyssen Wen
LastEditTime: 2021-05-27 18:25:19
Description: logger funtion
FilePath: \DLLG-2021-BUG-CV\Python\logger\logger.py
'''
import logging
import os
import yaml
from logging import config

def init_logging():
    """
    启动Logger
    版权声明：本文为CSDN博主「善良的小聪哥」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
    原文链接：https://blog.csdn.net/u012798083/article/details/105215801
    """
    logging_config_file = './Python/config/logging_config.yaml'
    with open(logging_config_file, 'r') as f:
        logging_yaml = yaml.safe_load(f.read())
        logging.config.dictConfig(config=logging_yaml)
    logging.getLogger(__name__)


