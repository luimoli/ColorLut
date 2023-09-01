import numpy as np
import cv2
import os

from pathlib import Path
import numpy as np

# from lut_3linear_interpolation import trilinear_interpolation
from lut_3linear_interpolation_arr import trilinear_interpolation
from tqdm import tqdm


if __name__ =='__main__':
    # img_path = Path('./test/kit-suman-5mcnzeSHFvE-unsplash.jpg')
    img_path = Path('./data_9/0.png')

    img = cv2.imread(str(img_path))
    # img = cv2.resize(img, None, fx=0.25, fy=0.25)
    img = img[:, :, ::-1].copy() / 255.

    lut_table_path = 'lut\lut_9.txt'
    lut = np.loadtxt(lut_table_path, delimiter='\t')

    # res = np.zeros_like(img)
    # h, w, c = img.shape
    # for i in tqdm(range(h)):
    #     for j in range(w):
    #         interpolated_rgb = trilinear_interpolation(lut, img[i][j])
    #         res[i][j] = interpolated_rgb
    
    res = trilinear_interpolation(lut, img) * 255.

    res = res[:, :, ::-1].copy()
    cv2.imwrite(str(img_path.parent / f'{img_path.stem}_new{img_path.suffix}'), res)
    
