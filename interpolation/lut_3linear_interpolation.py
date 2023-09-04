import numpy as np
import cv2
import os

from pathlib import Path
import numpy as np


# fd = open('a.CUBE')
# lines = fd.readlines()
# rgbFloatCube = []
# cubeDataStart = False
# for l in lines:
#     if cubeDataStart:
#         rgbStr = l.split(" ")
#         if len(rgbStr) == 3:
#             rgbFloat = (float(rgbStr[0]), float(rgbStr[1]), float(rgbStr[2]))
#             rgbFloatCube.append(rgbFloat)
#     if l.startswith("#LUT data points"):
#         cubeDataStart = True
# print(len(rgbFloatCube))


def cubeIndex(r, g, b, lut_size):
    # return int(r + g * 32 + b * 32 * 32)
    # return int(r*lut_size*lut_size + g*lut_size + b)
    # return (r*lut_size*lut_size + g*lut_size + b).astype(int)

    index = (r*lut_size*lut_size + g*lut_size + b).astype(int)
    # index[index >= lut_size*lut_size*lut_size] = lut_size*lut_size*lut_size-1
    if index >= lut_size*lut_size*lut_size:
        index = lut_size*lut_size*lut_size-1
    return index


def trilinear_interpolation(lut, input_rgb):
    """_summary_
    Args:
        lut_table_path (_type_): _description_
        input_rgb (arr): [0, 1]
    Returns:
        _type_: _description_
    """
    assert np.all(input_rgb <= 1)

    # lut = np.loadtxt(lut_table_path, delimiter='\t')



    # # Normalize input RGB values to range [0, 1]
    # rgb_normalized = input_rgb / 255.0


    # Scale the RGB values to match LUT indices (eg. 0 to 31)
    lut_size = int(np.ceil(len(lut) ** (1/3)))
    # print(lut_size)
    lut_indices = input_rgb * (lut_size - 1)

    # rgb_ceil = np.ceil(lut_indices)
    # rgb_floor = np.floor(lut_indices)

    # index_c = rgb_ceil[0]*lut_size*lut_size + rgb_ceil[1]*lut_size + rgb_ceil[2]
    # index_f = rgb_floor[0]*lut_size*lut_size + rgb_floor[1]*lut_size + rgb_floor[2]


    # Split the indices into integer and fractional parts
    indices_int = np.floor(lut_indices).astype(int)
    indices_frac = lut_indices - indices_int

    # # Get the eight nearest neighbors
    # c000 = lut[indices_int[0], indices_int[1], indices_int[2]]
    # c001 = lut[indices_int[0], indices_int[1], indices_int[2] + 1]
    # c010 = lut[indices_int[0], indices_int[1] + 1, indices_int[2]]
    # c011 = lut[indices_int[0], indices_int[1] + 1, indices_int[2] + 1]
    # c100 = lut[indices_int[0] + 1, indices_int[1], indices_int[2]]
    # c101 = lut[indices_int[0] + 1, indices_int[1], indices_int[2] + 1]
    # c110 = lut[indices_int[0] + 1, indices_int[1] + 1, indices_int[2]]
    # c111 = lut[indices_int[0] + 1, indices_int[1] + 1, indices_int[2] + 1]

    # Get the eight nearest neighbors
    c000 = lut[cubeIndex(indices_int[0], indices_int[1], indices_int[2], lut_size)]
    c001 = lut[cubeIndex(indices_int[0], indices_int[1], indices_int[2] + 1, lut_size)]
    c010 = lut[cubeIndex(indices_int[0], indices_int[1] + 1, indices_int[2], lut_size)]
    c011 = lut[cubeIndex(indices_int[0], indices_int[1] + 1, indices_int[2] + 1, lut_size)]
    c100 = lut[cubeIndex(indices_int[0] + 1, indices_int[1], indices_int[2], lut_size)]
    c101 = lut[cubeIndex(indices_int[0] + 1, indices_int[1], indices_int[2] + 1, lut_size)]
    c110 = lut[cubeIndex(indices_int[0] + 1, indices_int[1] + 1, indices_int[2], lut_size)]
    c111 = lut[cubeIndex(indices_int[0] + 1, indices_int[1] + 1, indices_int[2] + 1, lut_size)]

    # Perform trilinear interpolation for each channel
    c00 = c000 * (1 - indices_frac[2]) + c001 * indices_frac[2]
    c01 = c010 * (1 - indices_frac[2]) + c011 * indices_frac[2]
    c10 = c100 * (1 - indices_frac[2]) + c101 * indices_frac[2]
    c11 = c110 * (1 - indices_frac[2]) + c111 * indices_frac[2]

    c0 = c00 * (1 - indices_frac[1]) + c01 * indices_frac[1]
    c1 = c10 * (1 - indices_frac[1]) + c11 * indices_frac[1]

    c = c0 * (1 - indices_frac[0]) + c1 * indices_frac[0]

    return c






if __name__ =='__main__':
    # save_pathgt_path = './lut_input/data_17.txt'
    save_pathgt_path = './lut/lut_9.txt'
    data = np.loadtxt(save_pathgt_path, delimiter='\t')
    
    # color = np.array([175, 32, 96])
    # # color = np.round(color / 255. * 16.)
    # color = color / 255. * 16.
    # index = color[0]*17*17 + color[1]*17 + color[2]


    # color = np.array([0.562500,	0.375000, 0.375000])*16
    # index = color[0]*17*17 + color[1]*17 + color[2]



    # rgb = np.array([16, 239, 128]) / 255.
    rgb = np.array([0, 159, 64]) / 255.
    interpolated_rgb = trilinear_interpolation(data, rgb)
    print(interpolated_rgb * 255)

