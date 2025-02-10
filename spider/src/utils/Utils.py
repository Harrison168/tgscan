#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import platform
import time
from enum import Enum
import json
import socket
import base64
import logging
import logging.handlers
import re
import traceback

import unicodedata



class Os(Enum):
    WINDOWS="windows"
    LINUX="linux"
    MACOS="macos"
    OTHER="other"


def currentOs():
    sys_platform = platform.platform().lower()
    if "windows" in sys_platform:
        return Os.WINDOWS
    elif "darwin" in sys_platform:
        return Os.MACOS
    elif "linux" in sys_platform:
        return Os.LINUX
    else:
        return Os.OTHER

def current_dir():
    return os.path.dirname(os.path.abspath(__file__))

def data_dir():
    return f'{current_dir()}\\..\\..\\data'

def getConfig():
    config = {}
    configPath = data_dir()+'\\config.json'
    if os.path.exists(configPath):
        with open(configPath) as f:
            config = json.load(f)

    return config

# 日志配置
def createLogger(log_name):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    if not os.path.exists(logger_path):
        os.mkdir(logger_path)
    file_path = f'{logger_path}\\{log_name}'
    handler = logging.handlers.TimedRotatingFileHandler(filename=file_path, encoding='utf-8', when="midnight", interval=1, backupCount=7)
    handler.suffix = "%Y-%m-%d.log"
    handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s'))
    logger.addHandler(handler)
    return logger
logger_path = f'{current_dir()}\\..\\..\\logs'
logger_file_name = f'spider.log'
logger = createLogger(logger_file_name)

def removeChromeLog():
    try:
        file_path = f'{current_dir()}\\..\\chromedriver.log'
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as ex:
        logger.error('remove chromedriver.log error, ', traceback.format_exc())


_TIME_FORMAT_DATE = "%Y-%m-%d"
_TIME_FORMAT_DATE_NUM = "%Y%m%d"
_TIME_FORMAT_DATE_TIME = "%Y-%m-%d %H:%M:%S"

def getNowTimeStr():
    nowTime = time.strftime(_TIME_FORMAT_DATE_TIME, time.localtime())
    return nowTime

def getTimeByStr(data):
    nowTime = time.strptime(data, _TIME_FORMAT_DATE_TIME)
    return nowTime

def isNumber(content):
    if str.isdigit(content) or content=='':
        return True
    else:
        return False

def isNotEmpty(str=None):
    if str == None or len(str) == 0:
        return False
    return True


if __name__ == '__main__':

    print("gimana dongg tehh😁🤣😭" == "gimana dongg tehh😁🤣😭")


