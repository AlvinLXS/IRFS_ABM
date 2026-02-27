#!/usr/bin/env python
# -*- coding:utf-8 -*-


# @FileName  :main.py
# @Time      :2024/10/8 21:13
# @Author    :baiyunxiao,lixiaoshuang
# @Desc      :

#import yaml
from ruamel.yaml import YAML

yaml = YAML()

from visual_data import plot_data
from locations import generate_village
from simulation_env import SimulationEnv
from log import init_logging
from multiprocessing import cpu_count
from tools import set_random_seed


import sys

def parse_arguments(argv):
    args = {}
    i = 1
    # print(argv)
    while i < len(argv):

        if argv[i].startswith('-'):
            key = argv[i]
            if i + 1 < len(argv) and not argv[i + 1].startswith('-'):
                args[key] = argv[i + 1]
                i += 1
            else:
                args[key] = None
        i += 1

    return args


def convert_string(value):
    # 检查是否为布尔值
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False

    # 尝试转换为整数
    try:
        return int(value)
    except ValueError:
        pass

    # 尝试转换为浮点数
    try:
        return float(value)
    except ValueError:
        pass

    # 如果以上都不是，则返回原字符串
    return value

def init_all_config(config, arguments):

    for key in arguments:
        new_key = key[1:]
        k_v = arguments[key]
        if key == "-situation":
            v = k_v
        elif key == "-runtime":
            v = k_v
        else:
            if k_v.startswith("Lst_"):
                v = [eval(item) for item in k_v.split("_")[1:]]
            else:
                v = eval(k_v)
        config[new_key] = v
    
    if "skill_train_num_range" in config:
        config["env"]["skill_train_num_min"] = config["skill_train_num_range"][0]
        config["env"]["skill_train_num_max"] = config["skill_train_num_range"][1]

    # for section in config:
    #     print(f"Section: {section}")
    #     # 遍历该 section 中的所有键值对
    #     try:
    #         for key, value in config[section].items():
    #             print(f"  {key} = {value}")
    #     except:
    #         print(f"{section} = {config[section]}")



if __name__ == "__main__":
    arguments = parse_arguments(sys.argv)
    # arguments = {}
    # arguments["-total_compensation_per_farmer"] = "5000"
    # arguments['-skill_train_num_range'] = "Lst_0_0"
    # arguments['-compensation_years'] = "10"
    # arguments['-policy'] = "3"
    # arguments['-random_seed'] = "2024"
    # arguments["-situation"] = f"total_compensation_per_farmer_{arguments['-total_compensation_per_farmer']}_skill_train_num_range_{arguments['-skill_train_num_range']}_compensation_years_{arguments['-compensation_years']}_policy_{arguments['-policy']}_random_seed_{arguments['-random_seed']}"
    # arguments["-runtime"] = "241208175221"



    # 读取CONF文件
    path = "config.yaml"
    with open('config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.load(file)
    init_all_config(config, arguments)

    set_random_seed(config)

    data_collector = init_logging(config)

    villages = generate_village(config, data_collector)
    simuEnv = SimulationEnv(config, villages, data_collector)
    simuEnv.run()
    plot_data(data_collector["dynamic_info_log_path"])
    
    print(f"Done {arguments['-situation']}")



