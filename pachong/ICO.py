#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/26 17:50
# @Author  : Brawenlu
# @File    : ICO.py
# @Software: PyCharm

# PythonMargick包可以到Unofficial Windows Binaries for Python Extension Packages下载
import PythonMagick
import os
path =  os.getcwd() #返回当前工作目录的路径
filename = input("输入转换的完整图片名\n")
filepath = path + '\\'+ filename
img = PythonMagick.Image(filepath)
img.sample('228x228')#设置图片格式
newpath = path + '//ico.ico'
img.write(newpath)




