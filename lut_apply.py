import numpy as np
import cv2
import os

from pathlib import Path
import numpy as np

# from lut_3linear_interpolation import trilinear_interpolation
from interpolation.lut_3linear_interpolation_arr import trilinear_interpolation
from interpolation.lut_nearest_interpolation_arr import nearest_interpolation
from tqdm import tqdm


if __name__ =='__main__':
    # img_path = Path('./test/kit-suman-5mcnzeSHFvE-unsplash.jpg')
    # img_path = Path('./image/marvin-kuhn-uHrRgJKPPAk-unsplash.jpg')
    # img_path = Path('./data_9/0.png')

    lut_table_path = 'lut\lut_9.txt'
    lut = np.loadtxt(lut_table_path, delimiter='\t')

    image_root = Path('./image')
    img_path_list = [f for f in image_root.iterdir() if f.is_file()]
    for img_path in img_path_list:
        img = cv2.imread(str(img_path))
        # img = cv2.resize(img, None, fx=0.25, fy=0.25)
        img = img[:, :, ::-1].copy() / 255.

        # res = trilinear_interpolation(lut, img) * 255.
        res = nearest_interpolation(lut, img)

        res = res[:, :, ::-1].copy() * 255.
        cv2.imwrite(str(img_path.parent.parent / 'test' / f'{img_path.stem}_nearest{img_path.suffix}'), res)
    
