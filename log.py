#!/usr/bin/env python
# -*- coding:utf-8 -*-


# @FileName  :log.py
# @Time      :2024/10/12 17:15
# @Author    :baiyunxiao,lixiaoshuang
# @Desc      :

import logging
import json
import os
import time

def init_logging(config):
    """
    初始化日志，将日志输出到指定的文件中。
    """
    log_dir = f"result/{config['runtime']}/{config['situation']}"
    os.makedirs(log_dir, exist_ok=True)
    init_info_log = f"{log_dir}/init_info.txt"
    dynamic_info_log = f"{log_dir}/{config['situation']}.txt"

    formatter = logging.Formatter('%(message)s')

    logger = logging.getLogger("log_init")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(init_info_log, encoding="utf-8", mode="w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger2 = logging.getLogger("log_dynamic")
    logger2.setLevel(logging.INFO)
    file_handler2 = logging.FileHandler(dynamic_info_log, encoding="utf-8", mode="w")
    file_handler2.setLevel(logging.INFO)
    file_handler2.setFormatter(formatter)
    logger2.addHandler(file_handler2)

    return {"init":logger, "dynamic":logger2, "dynamic_info_log_path":dynamic_info_log}
