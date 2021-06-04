'''
Author: Thyssen Wen
Date: 2021-05-30 13:27:33
LastEditors: Thyssen Wen
LastEditTime: 2021-06-04 17:34:16
Description: serial communication module
FilePath: /DLLG-2021-BUG-CV/Python/serial/serial.py
'''
import logging
import os
import serial
import threading
import config.config as config

class Serial():
    def __init__(self):
        self.data='' #读取的数据
        self.read_flag=True  #读取标志位
        self.port_name = config.getConfig("serial", "port_name")
        self.bps = int(config.getConfig("serial", "bps"))
        self.timeout = int(config.getConfig("serial", "timeout"))
        self.open()
        logging.info('initial class success!')

    def open(self):
        # open serial
        try:
            # 打开串口，并得到串口对象
            self.serial = serial.Serial(self.port_name, self.bps, timeout=self.timeout)
            #判断是否打开成功
            if(self.serial.is_open):
                threading.Thread(target=self.ReadSerial, args=(self.serial,)).start()
                logging.info('initial serial threading success!')
        except Exception as e:
            logging.error('initial serial fail!')

    def ReadSerial(self):
        while self.read_flag:
            if self.serial.in_waiting:
                self.data = self.serial.read(serial.in_waiting).decode('hex')
                return self.data

    def ColsePort(self):
        self.read_flag = False
        self.serial.close()

    def SendSerial(self,data):
        success_bytes = self.serial.write(data.encode('hex'))
        return success_bytes

    def getEnermyColor(self):
        pass

    def sendShotCommand(self,yawErr,pictchErr,distance):
        pass

    def getHitModel(self):
        pass
