#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 14:58
# @Author  : Brawenlu
# @File    : Fengzhuang.py
# @Software: Sinfor
import paramiko
import datetime
import os,re
import tkinter as tk
import tkinter
from tkinter import filedialog
import tkinter.messagebox as mb


hostname='10.243.255.243'
username='sangfor'
password='sangfor@123'
port=22

def upload(local_file,remote_dir):
    try:
        #连接linux
        t = paramiko.Transport((hostname,port))
        t.connect(username=username,password=password)
        sftp = paramiko.SFTPClient.from_transport(t)

        print('upload file start %s ' % datetime.datetime.now())
        yasuobao = local_file.split('\\')[-1]
        # print(yasuobao)
        remote_dir = remote_dir+'/'+yasuobao
        print('单号以及远程目录为：'+yasuobao,remote_dir)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)
        stdin, stdout, stderr = ssh.exec_command('ls  /emm/custom/')
        list2 = stdout.readlines()
        print(list2)
        print('上传记录为'+local_file,remote_dir)
        try :
            # stdin, stdout, stderr = ssh.exec_command('cd /emm/custom/')
            stdin, stdout, stderr = ssh.exec_command('tar zxvf {} -C /emm/custom'.format(remote_dir))
            # stdin, stdout, stderr = ssh.exec_command('sangfor@123')
            list3 = stdout.readlines()
            print(list3)
        except Exception as a:
            print("压缩命令错误")

    except Exception as e:
        print('连接失败，尝试Ping一下封装平台\n')
        print(88, e)


if __name__=='__main__':
    root = tk.Tk()
    root.withdraw()
    remote_dir = '/emm/custom'
    local_file=r'D:\SSLPK-WRAP-IMPROVE-SJJ-20190219011.zip'
    upload(local_file, remote_dir)
    # file_path = sys.argv[1]
    # local_dir = filedialog.askdirectory()

    # if not os.path.isdir(local_dir):  # 判断本地路径是否存在
    #     # print('ERROR the local dir %s is not exist' % local_path)
    #     mb.showinfo('没有上传', '没有上传任何文件夹，重新上传')
    # else:
    #     # print(local_dir)
    #     local_dir = local_dir.replace('/','\\')
    #     # print(local_dir)
    #     # local_dir = r'D:\SSL-2019030408'
    #     remote_dir = '/emm/custom/'
    #     upload(local_dir, remote_dir)
