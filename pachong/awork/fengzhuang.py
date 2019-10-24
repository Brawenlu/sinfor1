#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/16 9:52
# @Author  : Brawenlu
# @File    : Ftpxuexi.py
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
def upload(local_dir,remotedir):
    try:
        #连接linux
        t = paramiko.Transport((hostname,port))
        t.connect(username=username,password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print('upload file start %s ' % datetime.datetime.now())
        danhao = local_dir.split('\\')[-1]
        print(danhao)
        remotedir = os.path.join(remotedir,danhao)

        #检测文件夹是否存在
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)
        stdin, stdout, stderr = ssh.exec_command('ls -name /emm/custom/')
        # print(stdout.readlines())
        list2 = stdout.readlines()
        print(list2)
        # print(type(stdout.readlines()))
        for i in range(len(list2)):
            print(i,list2[i])
            # print(type(list2[i]))
            an = re.search(danhao, list2[i])
            if an:
                mb.showinfo('提示', '定制单号已存在,点击继续')
                break
            else:
                sftp.mkdir(remotedir)
                break
        # if stdout.readline() != '':
        #     print("exist")
        # else:
        #     print("not exist")
        # if  sftp.stat(remotedir):
        #     mb.showinfo('提示', '定制单号已存在')
        # # print(remotedir)
        # # print(local_dir)
        # else: sftp.mkdir(remotedir)
            # print(1)





        print('创建文件夹'+remotedir+'成功')
        remotedir = remotedir +'/'
        #如果是空文件夹不会上传
        for root, dirs, files in os.walk(local_dir):
            # print('[%s][%s][%s]' % (root,dirs,files))
            for filepath in files:
                local_file = os.path.join(root,filepath)
                # print(local_file)
                # print(11,'[%s][%s][%s][%s]' %(root,filepath,local_file,local_dir))
                # a = local_file.replace(local_dir,'').replace('//','/').lstrip('/')  #lstrip用户截掉字符串左边的/返回后面的
                a = local_file.replace(local_dir,'').replace('\\','/').lstrip('/')  #lstrip用户截掉字符串左边的/返回后面的
                # print('01',a,'[%s]' % remotedir)
                remotefile = os.path.join(remotedir,a)
                # print(21,local_file)
                # print(22,remotefile)
                try:
                    sftp.put(local_file,remotefile)
                    print('上传文件'+remotefile+'成功')
                except Exception as e:
                    # print(os.path.split(remotefile))  #将文件名和路径分割开实际上，该函数的分割并不智能，它仅仅是以 "PATH" 中最后一个 '/' 作为分隔符，分隔后，将索引为0的视为目录（路径），将索引为1的视为文件名，
                    # print(os.path.split(remotefile)[0])
                    sftp.mkdir(os.path.split(remotefile)[0])
                    print('文件夹'+os.path.split(remotefile)[0]+'创建成功')
                    sftp.put(local_file,remotefile)
                    print('文件夹里面'+remotefile+'文件上传成功')
                    # print('66 upload %s to remote %s' %(local_file,remotefile))
            # 如果是空文件夹也上传
            # for name in dirs:
            #     # remotedir2 = remotedir
            #     # remotedir1 = remotedir2
            #     print(name)
            #     local_path = os.path.join(root,name)
            #     print(0,local_path,local_dir)
            #     a = local_path.replace(local_dir,'').split('\\')[-1]
            #     print(1,a)
            #     print(1,remotedir)
            #     remote_path =  os.path.join(remotedir,a)
            #     print(33,remote_path)
            #     try:
            #         sftp.mkdir(remote_path)
            #         print(44,'mkdir path %s'% remote_path)
            #         print('创建文件夹成功')
            #         # remotedir = remote_path+'/'
            #     except Exception as e:
            #         print('创建文件夹失败')
            #         print(55,e)
        print('upload file success %s ' % datetime.datetime.now())
        t.close()
        mb.showinfo('恭喜您', '上传成功')
    except Exception as e:
        print('连接失败，尝试Ping一下封装平台\n')
        print(88, e)

if __name__=='__main__':
    root = tk.Tk()
    root.withdraw()
    # file_path = sys.argv[1]
    local_dir = filedialog.askdirectory()
    if not os.path.isdir(local_dir):  # 判断本地路径是否存在
        # print('ERROR the local dir %s is not exist' % local_path)
        mb.showinfo('没有上传', '没有上传任何文件夹，重新上传')
    else:
        # print(local_dir)
        local_dir = local_dir.replace('/','\\')
        # print(local_dir)
        # local_dir = r'D:\SSL-2019030408'
        remote_dir = '/emm/custom/'
        upload(local_dir, remote_dir)

