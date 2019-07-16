# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/20 14:52
# @Author  : Brawenlu
# @File    : Jd.py
# @Software: PyCharm
import Gui2,logging,os,wx
# import PythonMagick
import tkinter as tk
from tkinter import filedialog

class zhuanhuan(Gui2.MyFrame1):
    # global file_path
    def init_main_windows(self):
        logger = logging.getLogger()  # logging对象
        fh = logging.FileHandler("log.txt")  # 文件对象
        sh = logging.StreamHandler()  # 输出流对象
        fm = logging.Formatter('%(asctime)s-%(filename)s[line%(lineno)d]-%(levelname)s-%(message)s')  # 格式化对象
        fh.setFormatter(fm)  # 设置格式
        sh.setFormatter(fm)  # 设置格式
        logger.addHandler(fh)  # logger添加文件输出流
        logger.addHandler(sh)  # logger添加标准输出流（std out）
        logger.setLevel(logging.DEBUG)  # 设置从那个等级开始提示
    # def open(self):
    #     root = tk.Tk()
    #     root.withdraw()
    #     file_path = filedialog.askopenfilename()
    #     print(file_path)


    def view(self, event):
        global file_path
        root = tk.Tk()
        root.withdraw()
        root.title('')
        file_path = filedialog.askopenfilename()
        # print(file_path)
        self.m_textCtrl4.SetValue(file_path)
        picstr = file_path.split('.')[-1]
        # print(picstr)
        piclist = {'jpg','bmp','gif','png','bmp','tiff','psd','jpeg','jfif','jpe','tif','dib','ico'}
        if picstr not in piclist:
            self.m_textCtrl4.SetValue('请选择正确的图片格式!')
            self.m_textCtrl5.SetValue('选择失败！图片格式有误')
        else:
            self.m_textCtrl5.SetValue("选择成功！点击左侧转换")
        return file_path
        #path = os.getcwd()  # 返回当前工作目录的路径
        #filename = input("输入转换的完整图片名\n")
        #filepath = path + '\\' + filename
        # img = PythonMagick.Image(file_path)
        # img.sample('228x228')  # 设置图片格式
        # newpath = path + '//ico.ico'
        # img.write(newpath)

    def click(self, event):
        global file_path
        img = PythonMagick.Image(file_path)
        img.sample('48x48')  # 设置图片格式
        newfile = file_path.split('.')
        # print(newfile)
        newfile2 = newfile[0].split('/')
        if not os.path.exists('D:\\ICO'):
            os.mkdir('D:\\ICO')
        # print(newfile2)
        newpath = 'D:\\ICO\\{}.ico'.format(newfile2[-1])
        img.write(newpath)
        # self.m_textCtrl5.SetValue()
        self.m_textCtrl5.SetValue('转换成功!'+'\n'+'图片路径在D盘目录ICO文件夹')

if __name__ =='__main__':
    app = wx.App()
    main_win = zhuanhuan(None)
    main_win.init_main_windows()
    main_win.Show()
    app.MainLoop()












