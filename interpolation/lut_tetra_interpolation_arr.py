import numpy as np
import cv2
import os

from pathlib import Path
import numpy as np


def cubeIndex(r, g, b, lut_size):
    # return int(r + g * 32 + b * 32 * 32)
    # return int(r*lut_size*lut_size + g*lut_size + b)
    # return (r*lut_size*lut_size + g*lut_size + b).astype(int)

    index = (r*lut_size*lut_size + g*lut_size + b).astype(int)
    index[index >= lut_size*lut_size*lut_size] = lut_size*lut_size*lut_size-1
    # if index >= lut_size*lut_size*lut_size:
    #     index = lut_size*lut_size*lut_size-1
    return index


def tetrahedral_interpolation(lut, input_rgb):
    assert np.all(input_rgb <= 1)

    lut_size = int(np.ceil(len(lut) ** (1/3)))

    lut_indices = input_rgb * (lut_size - 1)

    # # 将RGB值缩放到0-1
    # scaled_rgb = rgb * (lut.shape[0] - 1)

    # # 获取RGB值的整数和小数部分
    # i = np.floor(scaled_rgb).astype(int)
    # f = scaled_rgb - i

    i = np.floor(lut_indices).astype(int)
    f = lut_indices - i

    # 获取四面体顶点的索引
    offset = np.greater_equal(*f[..., ::-1]).astype(int)
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

