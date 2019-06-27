# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/20 14:52
# @Author  : Brawenlu
# @File    : Jd.py
# @Software: PyCharm
import os

folder_name = input("请输入文件夹：")
os.chdir(folder_name)
file_names = os.listdir("./")
for name in file_names:
    print("是不是文件：", os.path.isfile(name))
    if os.path.isfile(name):
        name = os.path.abspath(name)
        # 返回一个元组，元组第二个元素是扩展名
        if os.path.splitext(name)[1] == ".zip":
            cmd = '\"C:\\Program Files\\7-Zip\\7z.exe\" x \"{0}\" -oe:/测试解压/new *.mp4 -r'.format(name)
            os.popen(cmd)