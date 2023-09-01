import numpy as np
import cv2
import os

from pathlib import Path


def generate_image_single(h, w, rows, cols, color_list, save_path):
    """_summary_

    Args:
        h (int): _description_
        w (int): _description_
        rows (int): _description_
        cols (int): _description_
        color_list (list): patch sequences which are used to fill the fixed h*w image
        save_path (str): _description_
    """

    # Create an empty image array
    image = np.zeros((h, w, 3))
    
    # Calculate the size of each patch
    patch_width = w // cols
    patch_height = h // rows
    
    # Loop through each patch
    for i in range(rows):
        for j in range(cols):
            # Determine the start and end indices of each patch
            patch_start_x = j * patch_width
            patch_end_x = (j+1) * patch_width
            patch_start_y = i * patch_height
            patch_end_y = (i+1) * patch_height
            
            # Set the pixel values within the patch region
            if (i*cols + j) < len(color_list):
                image[patch_start_y:patch_end_y, patch_start_x:patch_end_x, :] = color_list[i*cols + j] * 255.0
            
    cv2.imwrite(str(save_path), image[:,:,::-1].copy())
    # return image

# def generate_color_list(normalize=False, interval=4, flag='B'):
#     color_list = []
#     for r in range(0, 256, 256//interval):
#         for g in range(0, 256, 256//interval):
#             for b in range(0, 256, 256//interval):
#                 color_list.append(np.array([r, g, b]))
#                 # print(r//64*interval*interval+ g//64*interval + b//64)
#                 print(np.array([r, g, b]))
#     print(len(color_list))
#     color_arr = np.array(color_list)
#     if normalize:
#         color_arr = color_arr / 256
#     return color_arr
    

def generate_color_list(save_pathgt_path, size=17, flag='B',):
    """_summary_

    Args:
        size (int, optional): patch sequences size. Corresponding with 3d lut size. Defaults to 17.
        flag (str, optional): which channel first in LUT. Defaults to 'B'.

    Returns:
        _type_: _description_
    """
    color_list = []
    interval = 1.0 / (size-1)
    for r in range(size):
        for g in range(size):
            for b in range(size):
                color_list.append(np.array([r*interval, g*interval, b*interval]))
                # print(r*size*size + g*size + b)
                # print(r//64*interval*interval+ g//64*interval + b//64)
                # print(np.array([r, g, b]))
    print(len(color_list))
    color_arr = np.array(color_list)
    np.savetxt(save_pathgt_path, color_arr, fmt='%.6f', delimiter='\t')
    return color_arr





if __name__ =='__main__':
    save_pathgt_path = './lut_input/data_9.txt' #TODO
    color_arr = generate_color_list(save_pathgt_path, size=9)  # specify lut cube size
    # data = np.loadtxt(save_pathgt_path, delimiter='\t')

    h, w = 1440, 2560  # screen's resolution
    rows, cols = 6, 8  # generate patches
    num_fig = len(color_arr) // (rows*cols) # num of figures that color patches can fill
    save_path = Path('./data_9/')   #TODO
    os.makedirs(save_path, exist_ok=True)
    for i in range(num_fig+1):
        if i >= num_fig:
            generate_image_single(h, w, rows, cols, color_arr[i*rows*cols: ], save_path / f'{i}.png') # the rest patches can't fill the fig.
        else:
            generate_image_single(h, w, rows, cols, color_arr[i*rows*cols: (i+1)*rows*cols], save_path / f'{i}.png')


