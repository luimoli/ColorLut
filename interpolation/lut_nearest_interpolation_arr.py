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


def nearest_interpolation(lut, input_rgb):
    """_summary_
    Args:
        lut_table_path (_type_): _description_
        input_rgb (arr): [0, 1]
    Returns:
        _type_: _description_
    """
    assert np.all(input_rgb <= 1)

    # lut = np.loadtxt(lut_table_path, delimiter='\t')


    # Scale the RGB values to match LUT indices (eg. 0 to 31)
    lut_size = int(np.ceil(len(lut) ** (1/3)))
    # print(lut_size)
    lut_indices = input_rgb * (lut_size - 1)


    # Split the indices into integer and fractional parts
    indices_int = np.floor(lut_indices).astype(int)
    indices_frac = lut_indices - indices_int

    # Get the eight nearest neighbors
    c000 = lut[cubeIndex(indices_int[..., 0], indices_int[..., 1], indices_int[..., 2], lut_size)]
    c111 = lut[cubeIndex(indices_int[..., 0] + 1, indices_int[..., 1] + 1, indices_int[..., 2] + 1, lut_size)]

    c = c000 + (c111 - c000) * indices_frac
    # c = c000 * (1 - indices_frac) + c111 * indices_frac

    return c






if __name__ =='__main__':
    save_pathgt_path = './lut_input/data_17.txt'
    data = np.loadtxt(save_pathgt_path, delimiter='\t')
    
    # color = np.array([175, 32, 96])
    # # color = np.round(color / 255. * 16.)
    # color = color / 255. * 16.
    # index = color[0]*17*17 + color[1]*17 + color[2]


    # color = np.array([0.562500,	0.375000, 0.375000])*16
    # index = color[0]*17*17 + color[1]*17 + color[2]



    # rgb = np.array([16, 239, 128]) / 255.
    # rgb = np.array([255, 255, 255]) / 255.
    # interpolated_rgb = trilinear_interpolation(data, rgb)
    # print(interpolated_rgb * 255)

