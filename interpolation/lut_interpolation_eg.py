import numpy as np
import cv2
import os

from pathlib import Path
import numpy as np



def tetrahedral_interpolation(lut, rgb):
    # 将RGB值缩放到0-1
    scaled_rgb = rgb * (lut.shape[0] - 1)

    # 获取RGB值的整数和小数部分
    i = np.floor(scaled_rgb).astype(int)
    f = scaled_rgb - i

    # 获取四面体顶点的索引
    offset = np.greater_equal(*f[::-1]).astype(int)
    indices = [
        i,
        i + np.array([offset[0], offset[1], offset[2]]),
        i + np.array([offset[0], offset[1] + 1 - offset[2], offset[2]]),
        i + np.array([offset[0] + 1 - offset[1], offset[1], offset[2]])
    ]

    # 计算插值权重
    weights = [
        1 - f[0] - f[1] - f[2],
        f[0] - offset[0],
        f[1] - offset[1],
        f[2] - offset[2]
    ]

    # 计算插值结果
    result = np.zeros(3)
    for index, weight in zip(indices, weights):
        result += weight * lut[tuple(index)]

    return result

def trilinear_interpolation(lut, rgb):
    # 将RGB值缩放到0-1
    scaled_rgb = rgb * (lut.shape[0] - 1)

    # 获取RGB值的整数和小数部分
    i = np.floor(scaled_rgb).astype(int)
    f = scaled_rgb - i

    # 获取插值立方体的8个顶点
    points = [
        lut[i[0], i[1], i[2]],
        lut[i[0], i[1], i[2] + 1],
        lut[i[0], i[1] + 1, i[2]],
        lut[i[0], i[1] + 1, i[2] + 1],
        lut[i[0] + 1, i[1], i[2]],
        lut[i[0] + 1, i[1], i[2] + 1],
        lut[i[0] + 1, i[1] + 1, i[2]],
        lut[i[0] + 1, i[1] + 1, i[2] + 1],
    ]

    # 在每个维度上进行插值
    result = (1 - f[0]) * ((1 - f[1]) * ((1 - f[2]) * points[0] + f[2] * points[1]) + f[1] * ((1 - f[2]) * points[2] + f[2] * points[3])) \
             + f[0] * ((1 - f[1]) * ((1 - f[2]) * points[4] + f[2] * points[5]) + f[1] * ((1 - f[2]) * points[6] + f[2] * points[7]))

    return result