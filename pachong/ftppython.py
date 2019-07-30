#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/16 9:52
# @Author  : Brawenlu
# @File    : Ftpxuexi.py
# @Software: Sinfor
from ftplib import FTP,error_perm
import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as mb
# 加载ftp以及tkinker相关模块模块
class FTPsyn():
    conn = FTP() #创建一个ftp对象

    def __init__(self,host,port=21):
        self.conn.connect(host,port) #连接ftp

    def login(self,username,password):
        self.conn.login(username,password)
        self.conn.encoding = "GB2312"
        self.conn.set_debuglevel(0)  #打开调试级别2，显示详细信息
        self.conn.set_pasv(True) #0主动模式 1 #被动模式
        print(self.conn.welcome) #显示登陆成功信息


    def _is_ftp_dir(self,ftp_path):
        """
        用来判断所给的路径是文件还是文件夹
        """
        ftp_path = ftp_path.rstrip('/')
        # print(ftp_path)
        ftp_parent_path = os.path.dirname(ftp_path)  #去掉文件名，返回目录
        # print(ftp_parent_path)
        self.ftp_dir_name = os.path.basename(ftp_path)  #os.path.basename 返回path最后的文件名
        # print(self.ftp_dir_name)
        self._is_dir = False
        # print(self._is_dir)
        if ftp_path=='.' or ftp_path=='./' or ftp_path=='':  #判断是不是为空或者跟路径
            self._is_dir=True
        else:
            try:
                self.conn.cwd(ftp_path)
                self._is_dir=True
                # self.conn.retrlines('LIST %s' % ftp_parent_path, self._ftp_list)   #获得当前ftp路径下所有文件信息
            except error_perm as e:
                return self._is_dir
        return self._is_dir



    def put_file(self,local_path,ftp_path='.'):
        # print(local_path)
        ftp_path = ftp_path.rstrip('/') #去掉尾部的指定字符
        # print(ftp_path)
        if os.path.isfile(local_path):
            file_handle = open(local_path,'rb')  #以二进制方式打开文件返回文件对象
            # print(file_handle)
            local_file_name = os.path.basename(local_path)  #os.path.basename 返回path最后的文件名
            # print(local_file_name)
            # print(self._is_ftp_dir(ftp_path))

            if self._is_ftp_dir(ftp_path):   # 如果远程路径是个目录，则上传文件到这个目录，文件名不变
                # print(ftp_path)
                # print(os.path.join(ftp_path, local_file_name))
                # self.conn.storbinary('STOR %s'%ftp_path, file_handle)  #上传文件至ftp目录
                self.conn.storbinary('STOR %s' % os.path.join(ftp_path, local_file_name), file_handle)   #ftp.storbinaly("STOR filename.txt",file_handel,bufsize) #上传目标文件


            elif self._is_ftp_dir(os.path.dirname(ftp_path)):    #如果远程路径的上层是个目录，则上传文件，文件名按照给定命名
                print("STOR %s" %ftp_path)
                print(1)
                self.conn.storbinary('STOR %s'%ftp_path,file_handle)

            else:  # 如果远程路径不是目录，且上一层的目录也不存在，则提示给定远程路径错误
                print('STOR %s' %ftp_path, file_handle)


    def put_dir(self,local_path,ftp_path=".",begin=True):
        ftp_path = ftp_path.rstrip('/')  # 去掉尾部的指定字符
        # print(ftp_path)
        # print(local_path)
        # print(ftp_path)


        if not os.path.isdir(local_path):  #判断本地路径是否存在
            print('ERROR the local dir %s is not exist'%local_path)
            mb.showinfo('提示信息', '请选择文件夹')
            return
        if begin:# 上传初始化：如果给定的ftp路径不存在需要创建，同时将本地的目录存放在给定的ftp目录下。  # 本地目录下文件存放的路径为ftp_path = ftp_path + os.path.basename(local_path)
            if not self._is_ftp_dir(ftp_path):
                try:
                    self.conn.mkd(ftp_path)
                    # print(ftp_path)
                except Exception as e:
                    pass
            ftp_path=os.path.join(ftp_path,os.path.basename(local_path))
            # print(ftp_path)

        # 如果上传路径是文件夹，则创建目录
        # print(ftp_path)

        if not self._is_ftp_dir(ftp_path):
            try:
                self.conn.mkd(ftp_path)  #创建目录
            except Exception as e:
                pass

        # 进入本地目录，开始递归查询
        os.chdir(local_path)    #os.chdir() 方法用于改变当前工作目录到指定的路径
        # print(os.getcwd())   #返回当前工作目录
        local_files = os.listdir('.')   #os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
        # print(local_files)
        if len(local_files) ==2:
            # print(1)
            # print(local_files[1])
            # print(local_files[0])
            for local_files_cunzai in local_files:
                # print(local_files_cunzai)
                if '~$' in local_files_cunzai:
                    # print(1)
                    local_files.remove(local_files_cunzai)
        for file in local_files:
            ftp_file = os.path.join(ftp_path,file)    #拼接目录字符创建目录，
            print(ftp_file)
            # print(file)
            # 如果file本地路径是目录则递归上传文件（不需要再进行初始化begin的标志修改为False）
            # #如果file本地路径是文件则直接上传文件
            if os.path.isdir(file):
                self.put_dir(file,ftp_file,False)
            else:
                # print(ftp_path)
                self.put_file(file,ftp_path)
        # 如果当前本地目录文件已经遍历完毕返回上一层目录
        os.chdir('..')


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    srcDir = filedialog.askdirectory()
    ftp = FTPsyn('199.200.0.3')
    ftp.login('test', "test")
    # ftp.put_file('D:/resource.csv')
    # ftp._is_ftp_dir('luwenbo//你好')
    ftp.put_dir(srcDir,'/定制提交',begin=True)
    # ftp.cwd('/luwenbo')
    # list = ftp.nlst()
    # print(list)
    if srcDir !='':
        mb.showinfo('恭喜您','上传成功')

