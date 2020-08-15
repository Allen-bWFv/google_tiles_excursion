#!/usr/bin/evn python
# -*- coding:utf-8 -*-
from PIL import Image
import os

def IsValidImage(img_path):
    """
    判断文件是否为有效（完整）的图片
    :param img_path:图片路径
    :return:True：有效 False：无效
    """
    bValid = True
    try:
        Image.open(img_path).verify()
    except:
        bValid = False
    return bValid


def transimg(img_path, output_dir):
    """
    转换图片格式
    :param img_path:图片路径
    :return: True：成功 False：失败
    """
    if IsValidImage(img_path):
        try:
            file_name = os.path.split(img_path)[1]
            str = file_name.rsplit(".", 1)
            output_img_path =output_dir + "/" + str[0] + ".jpeg"
            im = Image.open(img_path)
            im.save(output_img_path)
            return True
        except:
            return False
    else:
        return False


if __name__ == '__main__':
    root_path = "D:/work/project/tea_weather/tiles/google_tiles/6"
    output_dir = "D:/work/project/tea_weather/tiles/google_tiles_fix/6"
    if not os.path.exists(output_dir):
    	os.mkdir(output_dir)
    images = os.listdir(root_path)
    for image in images:
        transimg(os.path.join(root_path,image),output_dir)
    print("转换完成")
