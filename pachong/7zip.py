# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/20 14:52
# @Author  : Brawenlu
# @File    : Jd.py
# @Software: PyCharm
import tkMessageBox as mb
import tkinter as tk

root = tk.Tk()
root.withdraw()
result = mb.showinfo('提示信息', '上传成功')
# print(result)        # 返回字符串：ok
