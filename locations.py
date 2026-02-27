#!/usr/bin/env python
# -*- coding:utf-8 -*-


# @FileName  :locations.py
# @Time      :2024/10/3 16:47
# @Author    :baiyunxiao, lixiaoshuang
# @Desc      :

import random
import math
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


def calculate_distances(point, points_array):
    """
    计算一个点与一组点之间的欧几里得距离。

    :param point: 单个点的坐标 (x, y)
    :param points_array: 其他点的坐标列表 [(x1, y1), (x2, y2), ..., (xn, yn)]
    :return: 一维数组，包含与每个点之间的距离
    """
    # 将输入的点和点数组转换为NumPy数组
    point = np.array(point)
    points_array = np.array(points_array)

    # 计算差值
    differences = points_array - point

    # 计算每个差值的平方和
    squared_diff = np.sum(differences ** 2, axis=1)

    # 计算平方和的平方根，即欧几里得距离
    distances = np.sqrt(squared_diff)

    return distances


# 生成椭圆内的随机点
def random_point_in_ellipse(semi_major, semi_minor):
    t = 2 * math.pi * random.random()
    u = random.random() + random.random()
    r = u if u <= 1 else 2 - u
    x = r * math.cos(t) * semi_major
    y = r * math.sin(t) * semi_minor
    return x, y


# 确保农户之间的距离在6到20米之间
def generate_farmers_in_group(center, num_farmers):
    farmers = [(center[0], center[1])]
    while len(farmers) < num_farmers:

        offset = [random.uniform(-500, 500), random.uniform(-500, 500)]
        x = center[0] + offset[0]
        y = center[1] + offset[1]

        point = (x, y)
        distances = calculate_distances(point, farmers)
        if min(distances) > 10 and min(distances) < 50:
            farmers.append((x, y))
    return farmers


def gernerate_group_center(village_center, group_centers, index):
    point = village_center
    while True:
        offset = [random.uniform(-1500, 1500), random.uniform(-1500, 1500)]
        x = point[0] + offset[0]
        y = point[1] + offset[1]
        group_center = (x, y)
        if index == 0:
            group_centers.append((x, y))
            break
        else:
            distances = calculate_distances(group_center, group_centers)
            if min(distances) > 500 and max(distances) < 3000: #两个组中心位置之间最少隔1500*1.414米，最大不超过3000*1.414米
                group_centers.append((x, y))
                break
    return group_center, group_centers


def generate_village(config, data_collector):
    # 椭圆参数计算
    area_km2 = 500
    area_m2 = area_km2 * 1e6
    semi_major_axis = math.sqrt(area_m2 / math.pi) * 1000  # 半长轴，单位：米
    semi_minor_axis = semi_major_axis / 2  # 半短轴，单位：米

    # 村庄和组的参数
    num_villages = config['env']["num_villages"]
    group_range = (config['env']['group_min_per_village'], config['env']['group_max_per_village'])
    farmers_per_group_range = (config['env']['farmers_min_per_group'], config['env']['farmers_max_per_group'])

    villages = []
    for i in tqdm(range(num_villages), desc="Generating villages..."):
        village_center = random_point_in_ellipse(semi_major_axis, semi_minor_axis)
        num_groups = random.randint(*group_range)
        village = []
        group_centers = []
        for j in tqdm(range(num_groups), desc=f"Generating groups of village {i+1}", leave=False):

            group_center, group_centers = gernerate_group_center(village_center, group_centers, j)

            num_farmers = random.randint(*farmers_per_group_range)

            farmers = generate_farmers_in_group(group_center, num_farmers)

            village.append(farmers)
        villages.append(village)
    return villages

def visiz_location(villages, num_villages):
    # 绘制村庄和农户
    plt.figure(figsize=(12, 12))
    colors = plt.cm.get_cmap('tab10', num_villages)  # 使用10种颜色的colormap

    for i, village in enumerate(villages):
        for group in village:
            x_coords, y_coords = zip(*group)
            plt.scatter(x_coords, y_coords, s=1, color=colors(i), label=f'Village {i+1}' if group == village[0] else "")

    plt.title('Farmers Distribution in Villages')
    plt.xlabel('X Coordinate (m)')
    plt.ylabel('Y Coordinate (m)')
    plt.legend()
    plt.axis('equal')
    plt.show()

    fig, axes = plt.subplots(3, 4, figsize=(20, 15))  # 创建3x4的子图布局
    axes = axes.flatten()

    for i, village in enumerate(villages):
        ax = axes[i]
        for group in village:
            x_coords, y_coords = zip(*group)
            ax.scatter(x_coords, y_coords, s=1)
        ax.set_title(f'Village {i + 1}')
        ax.set_xlabel('X Coordinate (m)')
        ax.set_ylabel('Y Coordinate (m)')
        ax.axis('equal')

    # 移除多余的子图
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
