#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 14:04
# @Author  : Brawenlu
# @Site    : 
# @File    : Test.py
# @Software: PyCharm
import tkinter as tk
from tkinter import  filedialog
root = tk.Tk()
root.withdraw()
file_path =  filedialog.askopenfilename()
print(file_path)