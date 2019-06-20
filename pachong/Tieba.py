#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/20 14:52
# @Author  : Brawenlu
# @File    : Jd.py
# @Software: PyCharm

import requests,time,logging
from bs4 import BeautifulSoup
import pandas as pd
import wx
import Gui
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


class Tiebawindow(Gui.MyFrame1):
    def init_main_window(self):
        logger = logging.getLogger()  # logging对象
        fh = logging.FileHandler("log.txt")  # 文件对象
        sh = logging.StreamHandler()  # 输出流对象
        fm = logging.Formatter('%(asctime)s-%(filename)s[line%(lineno)d]-%(levelname)s-%(message)s')  # 格式化对象
        fh.setFormatter(fm)  # 设置格式
        sh.setFormatter(fm)  # 设置格式
        logger.addHandler(fh)  # logger添加文件输出流
        logger.addHandler(sh)  # logger添加标准输出流（std out）
        logger.setLevel(logging.DEBUG)  # 设置从那个等级开始提示
        self.m_textCtrl1.SetValue('请输入想要查询的贴吧名字')
        self.m_textCtrl2.SetValue('请输入想要查询的回帖数临界点，仅仅显示大于该临界点的帖子')
        self.m_textCtrl3.SetValue('请输入你要查询的帖子页数')
        self.m_textCtrl4.SetValue('日志如下(日志文件在软件同级目录的test.log)'+'\n')
    def click(self, event):
        def extra_from_one_page(page_lst):
            tmp = []
            for i in page_lst:
                    if int(i.find(class_='threadlist_rep_num').text) > int(self.m_textCtrl2.GetValue()):
                        dic = {}
                        dic['回帖数'] = int(i.find(class_='threadlist_rep_num').text)
                        dic['帖子名称'] = i.find(class_='threadlist_title').text
                        dic['帖子地址'] = 'https://tieba.baidu.com' + i.find(class_='threadlist_title').a['href']
                        tmp.append(dic)
            return tmp
        def search_n_pages(n):
            target = []
            # global tiebaanme
            global tiebaanme
            template_url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}"
            for i in range(n):
                logging.info(u'正在爬取第{}页'.format(i + 1))
                target_url = template_url.format(self.m_textCtrl1.GetValue(), 50 * i)  # 按照浏览贴吧的自然行为，每一页50条
                # try:
                res = requests.get(target_url)
                # except:
                #     logging.error(u'请求失败,请检查网络连接!')
                #     self.m_textCtrl4.AppendText(u'请求失败,请检查网络连接!\n')
                soup = BeautifulSoup(res.text, 'html.parser')   # 转为 bs 对象
                page_list = soup.find_all(class_='j_thread_list')   # 获取该页帖子列表
                # for a in soup.find_all('a',class_=' card_title_fname'):
                #     tiebaanme = a.string.replace('\n','').replace(' ','')
                #     print(tiebaanme)
                # print(tiebaanme)
                # if self.m_textCtrl1.GetValue()!=tiebaanme:
                #     self.m_textCtrl4.AppendText('没找到"{}"此贴吧，已为您爬取如下贴吧: '.format(self.m_textCtrl1.GetValue())+tiebaanme+'\n')
                # print(extra_from_one_page(page_list))
                target.extend(extra_from_one_page(page_list))  #该页信息保存到target
                time.sleep(0.2)
                # print(target)
                self.m_textCtrl4.AppendText(u'正在爬取第{}页'.format(i + 1) + '\n')
                time.sleep(0.2)
            return target
        # try:
        resopnse = search_n_pages(int(self.m_textCtrl3.GetValue()))
        self.m_textCtrl4.AppendText(
                '本次爬取的是“{}”贴吧中回帖数大于 “{}” 的帖子信息，本次爬取{}页\n'.format(self.m_textCtrl1.GetValue(),
                                                                 self.m_textCtrl2.GetValue(),
                                                                 self.m_textCtrl3.GetValue()))
        self.m_textCtrl4.AppendText('爬取结束\n文件在软件同级目录的{}爬取结果.xlsx'.format(self.m_textCtrl1.GetValue()) + '\n')
        # self.m_textCtrl4.SetValue('日志如下(日志文件在软件同级目录的test.log)' + '\n')
        data = pd.DataFrame(resopnse)
        print(data)
        data.to_excel('{}爬取结果.xlsx'.format(self.m_textCtrl1.GetValue()))
        # except ValueError as z:
        #     self.m_textCtrl4.AppendText('爬取失败，详细日志如下\n')
        #     self.m_textCtrl4.AppendText('请在第二行、第三行输入整数(第二行输入帖子数，第三行输入页数)\n')
        # if resopnse==[]:
        #     self.m_textCtrl4.AppendText('爬取成功，但是没有爬取到“{}”贴吧中回帖数大于 “{}” 的帖子信息'.format(tiebaanme,
        #                                                          self.m_textCtrl2.GetValue()))
        # else:
    def click2(self,event):
        pass


if __name__ == '__main__':
    app = wx.App()
    main_win = Tiebawindow(None)
    main_win.init_main_window()
    main_win.Show()
    app.MainLoop()
