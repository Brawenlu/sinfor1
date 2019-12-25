#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 14:58
# @Author  : Brawenlu
# @File    : Fengzhuang.py
# @Software: Sinfor
import paramiko
import datetime,sys,time,random
import os,re
import tkinter as tk
import tkinter

from tkinter import filedialog
import tkinter.messagebox as mb


hostname='10.243.255.243'
username='sangfor'
password='sangfor@123'
port=22

suijishu = random.randint(0, 100)
localfile1=r'\\199.200.0.3\临时文件夹\应用封装'
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

        danhao = yasuobao.split('.')[0]
        print('单号为:'+danhao)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)
        stdin, stdout, stderr = ssh.exec_command('ls  /emm/custom/')
        list2 = stdout.readlines()
        print(list2)
        print('上传记录为'+local_file,remote_dir)
        chongfu = remote_dir.split('.')[0]
        print(chongfu)

        try :
            sftp.stat(chongfu)
            # print('1')
            print('单号已存在')
            # mb.showinfo('提示', '定制单号已存在,点击继续')
            stdin, stdout, stderr = ssh.exec_command('mv /emm/custom/{} /emm/custom/{}bak{}'.format(danhao,danhao,suijishu))
            print('输入完成')
            list3 = stdout.readlines()
            print(list3)
            print('旧的定制单号已备份')
            time.sleep(5)
        except:
            print('之前没有定制单号')


        try:
            sftp.put(local_file, remote_dir)
            time.sleep(5)
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
    remote_dir = '/emm/custom'
    localdanhao = sys.argv[1]
    # local_file=r'D:\SSL-2019030408.zip'
    local_file = localfile1 + '\\' + localdanhao
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
