# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 17:51
# @Author  : LWB
# @FileName: awork2.py
# @Software: PyCharm

import paramiko
import datetime
import os,re
import tkinter as tk
import tkinter
from tkinter import filedialog
import tkinter.messagebox as mb


hostname='10.243.255.242'
username='sangfor'
password='sangfor'
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
        try:
            sftp.put(local_file, remote_dir)
            print('上传文件' + yasuobao + '成功')
            try :
                stdin2, stdout2, stderr2 = ssh.exec_command('chmod 777 {}'.format(remote_dir))
                list4 = stdout2.readlines()
                print(list4)
                stdin, stdout, stderr = ssh.exec_command('tar zxvf {} -C /emm/custom'.format(remote_dir))
                list3 = stdout.readlines()
                print(list3)
            except Exception as a:
                print("压缩命令错误")
            try:
                stdin, stdout, stderr = ssh.exec_command('rm -f /emm/custom/{}'.format(yasuobao))
                list4 = stdout.readlines()
                print(list4)
                print("删除文件成功")
            except Exception as c:
                print('删除命令失败')
        except Exception as e:
            print('上传文件' + yasuobao + '失败')
    except Exception as e:
        print('连接失败，尝试Ping一下封装平台\n')
        print(88, e)


if __name__=='__main__':
    root = tk.Tk()
    root.withdraw()
    remote_dir = '/var/www/sangfor/default/awork'
    local_file=r'D:\SSL-2019100801.zip'
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

