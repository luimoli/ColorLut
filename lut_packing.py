import cv2
import numpy as np

from pathlib import Path


def get_point_index(upper_left, bottom_right, rows, cols):
    """for a single img, get color patches's indexes.

    Args:
        upper_left (_type_): _description_
        bottom_right (_type_): _description_
        rows (_type_): _description_
        cols (_type_): _description_

    Returns:
        _type_: _description_
    """
    upper_left_h, upper_left_w = upper_left
    bottom_right_h, bottom_right_w = bottom_right
    # upper_right = (upper_left_h, bottom_right_w)
    # bottom_left = (bottom_right_h, upper_left_w)
    width_interval = (bottom_right_w - upper_left_w) // (cols - 1)
    height_interval = (bottom_right_h - upper_left_h) // (rows - 1)
    point_list = []
    for i in range(rows):
        for j in range(cols):
            point_h = upper_left_h + i * height_interval
            point_w = upper_left_w + j * width_interval
            point_list.append((point_h, point_w))

    return point_list

def check_point_index(img_path, save_path, point_list):
    img = cv2.imread(img_path)
    for point in point_list:
        cv2.circle(img, (point[1],point[0]), 10, (255, 0, 0), -1)
    cv2.imwrite(save_path, img)


def slice_image(image, h, w, size):
    left = w - size // 2
    top = h - size // 2
    right = left + size
    bottom = top + size
    return image[top:bottom, left:right, :].copy()

def check_slice_img(img, point_list, square_size):
    image = img[:,:,::-1].copy()
    for point in point_list:
        x, y = point[1], point[0]
        top_left = (x - square_size // 2, y - square_size // 2)
        bottom_right = (x + square_size // 2, y + square_size // 2)
        cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
    cv2.imwrite('.test_square.jpg', image)


def get_color(img_root, point_list, cut_range, original_length):
    img_root = Path(img_root)
    img_path_list = [f for f in img_root.iterdir() if f.is_file()]
    img_path_list = sorted(img_path_list)

    lut_list = []
    for path in img_path_list:
        img = cv2.imread(str(path))[:, :, ::-1].copy()

        # for point in point_list:
        #     cv2.circle(img, (point[1],point[0]), 10, (255, 0, 0), -1)
        # cv2.imwrite('./test.jpg', img[:,:,::-1])

        # check_slice_img(img, point_list, cut_range)
        # print('.')

        for point in point_list:
            patch = slice_image(img, point[0], point[1], cut_range)
            lut_list.append(np.mean(patch, axis=(0, 1)))
    
    if len(lut_list) > original_length:
        lut = lut_list[:original_length]
    else:
        lut = lut_list
    return lut


if __name__ ==  '__main__':
    point_list = get_point_index((1967, 1804), (5023, 7368), 6, 8)

    img_root = f'./img_9'
    lut = get_color(img_root, point_list, 200, 9*9*9)

    # save lut
    lut = np.array(lut)
    np.savetxt('./lut/lut_9_255.txt', lut, fmt='%.6f', delimiter='\t')