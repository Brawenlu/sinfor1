#!/usr/bin/env python
#!-*- coding:utf-8 -*-
#coding:utf-8
# @Time    : 2019/2/20 14:52
# @Author  : Brawenlu
# @File    : Jd.py
# @Software: PyCharm


import sys
import os
import json
import Tkinter as tk
import tkFileDialog
from ftplib import FTP
import re
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
   reload(sys)
   sys.setdefaultencoding(default_encoding)

print sys.getdefaultencoding()
# reload(sys)
# sys.setdefaultencoding('utf-8')

_XFER_FILE = 'FILE'
_XFER_DIR = 'DIR'


class Xfer(object):
    def __init__(self):
        self.ftp = None
    def __del__(self):
        pass
    def setFtpParams(self, ip, uname, pwd, port=21, timeout=60):
        self.ip = ip
        self.uname = uname
        self.pwd = pwd
        self.port = port
        self.timeout = timeout
    def initEnv(self):      ##链接ftp
        if self.ftp is None:
            self.ftp = FTP()
            print '### connect ftp server: %s ...' % self.ip
            self.ftp.connect(self.ip, self.port, self.timeout)
            self.ftp.login(self.uname, self.pwd)
            print self.ftp.getwelcome()
    def clearEnv(self):
        if self.ftp:
            self.ftp.close()
            print '### disconnect ftp server: %s!' % self.ip
            self.ftp = None
    def uploadDir(self, localdir='./', remotedir='./1/2'):
        # if not os.path.exists(remotedir):
        #      list = localdir.split('\\')
        #      remote = list[-1]
        #      self.ftp.mkd(remote)
        print remotedir
        # print remotedir
        if not os.path.isdir(localdir):
            return
        self.ftp.cwd(remotedir)
        for file in os.listdir(localdir):
            src = os.path.join(localdir, file)
            if os.path.isfile(src):
                self.uploadFile(src, file)
            elif os.path.isdir(src):
                try:
                    self.ftp.mkd(file)         #子目录不存在则创建
                except:
                    sys.stderr.write('the dir is exists %s' % file)
                self.uploadDir(src, file)
        self.ftp.cwd('..')

    def uploadFile(self, localpath, remotepath='./'):
        if not os.path.isfile(localpath):
            return
        print '+++ upload %s to %s:%s' % (localpath, self.ip, remotepath)
        self.ftp.storbinary('STOR ' + remotepath, open(localpath, 'rb'))

    def __filetype(self, src):     ##判断是否为文件夹
        if os.path.isfile(src):
            index = src.rfind('\\')
            # print index
            if index == -1:
                index = src.rfind('/')
            return _XFER_FILE, src[index + 1:]
        elif os.path.isdir(src):
            return _XFER_DIR, ''      #如果是dir就返回dir，filename=''latin-1

    def upload(self, src):
        # filelist = []
        filetype, filename = self.__filetype(src)
        list = src.split('\\')
        remote = list[-1]
        print remote
        # print filetype
        # print filename
        self.initEnv()
        self.ftp.cwd('1/2')
        # print type(self.ftp.dir())
        # print type((self.ftp.nlst()))
        # print remote.encode("utf-8")
        # print type(remote.encode("utf-8"))
        # print type(self.ftp.nlst()[1])
        # for j in range(len(self.ftp.nlst())):
        #     print type(self.ftp.nlst()[j]).decode("utf-8")
        #     filelist[j]=(self.ftp.nlst()[j]).decode('utf-8')
        # print filelist
        print remote.encode("utf-8")
        if  remote.encode("utf-8") in self.ftp.nlst():
            print u'+++ ftp %s 目录已存在' %(remote)
            # self.ftp.rmd(remote)
            # self.ftp.mkd(remote)
        else:
            print u'+++ ftp %s 目录不存在' %(remote)
            self.ftp.mkd(remote)
        if filetype == _XFER_DIR:
            self.srcDir = src
            # print self.srcDir
            self.uploadDir(self.srcDir,remote)
        elif filetype == _XFER_FILE:
            self.uploadFile(src, filename)
        self.clearEnv()


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    srcDir = tkFileDialog.askdirectory()
    srcDir1 = srcDir.encode('utf-8')
    # print type(srcDir1)
    # print srcDir1
    srcDir2 = srcDir1.replace("/","\\")
    srcDir3 = unicode(srcDir2, 'utf-8')
    # srcDir = raw_input(u'请输入你要文件夹上传的路径名，以单号结束\n')
    print type(srcDir3)
    # srcDir1 = srcDi
    # srcDir = r"D:\1"
    list = srcDir.split('\\')
    remote = list[-1]
    # srcFile = r'C:\sytst\sar.c'
    xfer = Xfer()
    xfer.setFtpParams('199.200.1.88', 'test', 'test')
    xfer.upload(srcDir3)
    # xfer.upload(srcFile)