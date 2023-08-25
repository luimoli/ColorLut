import numpy as np
import cv2

def generate_cube_file(input_colors, output_colors, cube_size, file_path):
    # 创建一个空的3D LUT数组
    lut = np.zeros((cube_size, cube_size, cube_size, 3), dtype=np.uint8)

    # 将输入颜色映射到输出颜色
    for i in range(len(input_colors)):
        input_color = input_colors[i]
        output_color = output_colors[i]
        lut[input_color[0], input_color[1], input_color[2]] = output_color

    # 将LUT保存为.cube文件
    with open(file_path, 'w') as f:
        f.write('LUT_3D_SIZE {}\n'.format(cube_size))
        for r in range(cube_size):
            for g in range(cube_size):
                for b in range(cube_size):
                    f.write('{} {} {}\n'.format(lut[r, g, b, 0], lut[r, g, b, 1], lut[r, g, b, 2]))

# 输入颜色和对应的输出颜色
input_colors = [(0, 0, 0), (255, 255, 255)]  # 示例输入颜色
output_colors = [(0, 0, 0), (128, 128, 128)]  # 示例输出颜色

# 生成.cube文件
generate_cube_file(input_colors, output_colors, 16, 'output.cube')
