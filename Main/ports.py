import numpy as np
from django.conf import settings
import json
import tifffile as tiff


def CloudController(img, threshold, band):
    try:
        # 读取文件
        image = tiff.imread((settings.STATIC_URL + img).strip('/'))
        # 读取文件的图层数和长宽像素
        x, y, z = image.shape
        # 创建一个初始值全为0的uint8的长宽与读取文件一致的numpy数组
        newimage = np.zeros((y, z), np.uint8)
        # 判断传入的波段序号是否超过文件的图层数，若超过，返回code：202和错误信息
        if x <= band:
            return json.dumps({'code': 202, "info": "请选择正确的波段"})
        # 循环遍历选中图层，判断每个像素点的值是否超过阈值，若超过阈值，则设置为255，反之则设置为0
        for i in range(y):
            for j in range(z):
                if image[band - 1][i][j] > threshold:
                    newimage[i][j] = 255
                else:
                    newimage[i][j] = 0
        # 将处理后的numpy数组以tiff文件保存再选择路径下，并在原文件的最后加上_cloud便于下载
        tiff.imwrite("_cloud.".join((settings.STATIC_URL + img).split(".")).strip("/"), newimage)
        # 执行成功后返回code:200和Success信息
        return json.dumps({'code': 200, "info": "Success"})
    except:
        # 如果出现其他问题，返回code：201和Error信息
        return json.dumps({'code': 201, "info": "Error"})


def WaterController(img, threshold, band_green, band_nir):
    try:
        # 读取文件
        image = tiff.imread((settings.STATIC_URL + img).strip('/'))
        # 读取文件的图层数和长宽像素
        x, y, z = image.shape
        # 创建一个初始值全为0的uint8的长宽与读取文件一致的numpy数组
        newimage = np.zeros((y, z), np.uint8)
        # 判断传入的波段序号是否超过文件的图层数，若超过，返回code：202和错误信息
        if x <= band_green or x <= band_nir:
            return json.dumps({'code': 202, "info": "请选择正确的波段"})
        # 根据公式计算水体检测图片
        water_image = (image[band_green - 1] - image[band_nir - 1]) / (image[band_green - 1] + image[band_nir - 1])
        # 循环遍历水体检测图片，判断每个像素点的值是否超过阈值，若超过阈值，则设置为255，反之则设置为0
        for i in range(y):
            for j in range(z):
                if water_image[i][j] > threshold:
                    newimage[i][j] = 255
                else:
                    newimage[i][j] = 0
        # 将处理后的numpy数组以tiff文件保存再选择路径下，并在原文件的最后加上_water便于下载
        tiff.imwrite("_water.".join((settings.STATIC_URL + img).split(".")).strip("/"), newimage)
        # 执行成功后返回code:200和Success信息
        return json.dumps({'code': 200, "info": "Success"})
    except:
        # 如果出现其他问题，返回code：201和Error信息
        return json.dumps({'code': 201, "info": "Error"})


def TreeController(img, band_nir, band_red):
    try:
        # 读取文件
        image = tiff.imread((settings.STATIC_URL + img).strip('/'))
        cloudImage = tiff.imread("_cloud.".join((settings.STATIC_URL + img).split(".")).strip("/"))
        waterImage = tiff.imread("_water.".join((settings.STATIC_URL + img).split(".")).strip("/"))
        # 读取文件的图层数和长宽像素
        x, y, z = image.shape
        # 判断传入的波段序号是否超过文件的图层数，若超过，返回code：202和错误信息
        if x <= band_red:
            return json.dumps({'code': 202, "info": "请选择正确的波段"})
        # 根据公式计算EVI和EVI_norm的值
        EVI = 2.5 * (image[band_nir - 1] - image[band_red - 1]) / (image[band_nir - 1] + 2.4 * image[band_red - 1] + 1)
        EVI_norm = (EVI.max() - EVI) / (EVI.max() - EVI.min())
        # 对EVI_norm进行掩膜操作
        newimage = np.zeros((y, z), np.float32)
        for i in range(y):
            for j in range(z):
                newimage[i][j] = waterImage[i][j]*cloudImage[i][j]*EVI_norm[i][j]
        # 将处理后的numpy数组以tiff文件保存再选择路径下，并在原文件的最后加上_tree便于下载
        tiff.imwrite("_tree.".join((settings.STATIC_URL + img).split(".")).strip("/"), newimage)
        # 执行成功后返回code:200和Success信息
        return json.dumps({'code': 200, "info": "Success"})
    except:
        # 如果出现其他问题，返回code：201和Error信息
        return json.dumps({'code': 201, "info": "Error"})


def LandsideController(img, threshold):
    try:
        # 读取文件
        image = tiff.imread("_tree.".join((settings.STATIC_URL + img).split(".")).strip("/"))
        # 读取文件的长宽像素
        x, y = image.shape
        # 创建一个初始值全为0的uint8的长宽与读取文件一致的numpy数组
        newimage = np.zeros((x, y), np.uint8)
        # 循环遍历植被检测图片，判断每个像素点的值是否超过阈值，若超过阈值，则设置为255，反之则设置为0
        for i in range(x):
            for j in range(y):
                if image[i][j] > threshold:
                    newimage[i][j] = 255
                else:
                    newimage[i][j] = 0
        # 将处理后的numpy数组以tiff文件保存再选择路径下，并在原文件的最后加上_result便于下载
        tiff.imwrite("_result.".join((settings.STATIC_URL + img).split(".")).strip("/"), newimage)
        # 执行成功后返回code:200和Success信息
        return json.dumps({'code': 200, "info": "Success"})
    except:
        # 如果出现其他问题，返回code：201和Error信息
        return json.dumps({'code': 201, "info": "Error"})
