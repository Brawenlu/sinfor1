#解析内容的包
import requests,time,logging

from bs4 import BeautifulSoup
# 数据展示 的包
# import numpy as np
import pandas as pd
import wx
import Gui


# from Gui import MyFrame1

# tieba_name = input('请输入想要查询的贴吧名字:\n')
#回帖数设置临界点
# amout = input('请输入想要查询的回帖数临界点，仅仅显示大于该临界点的帖子\n')
# num = input('请输入你要查询的帖子页数\n')


class Tiebawindow(Gui.MyFrame1):
# 首先，咱们从刚刚源文件中将主窗体继承下来.就是修改过name属性的主窗体咯。
    def init_main_window(self):
        # global tiebaname
        # tiebaname = ""

        logger = logging.getLogger()  # logging对象
        fh = logging.FileHandler("log.txt")  # 文件对象
        sh = logging.StreamHandler()  # 输出流对象
        fm = logging.Formatter('%(asctime)s-%(filename)s[line%(lineno)d]-%(levelname)s-%(message)s')  # 格式化对象
        # logging.basicConfig(format=fm,level=logging.error)
        fh.setFormatter(fm)  # 设置格式
        sh.setFormatter(fm)  # 设置格式
        logger.addHandler(fh)  # logger添加文件输出流
        logger.addHandler(sh)  # logger添加标准输出流（std out）
        logger.setLevel(logging.DEBUG)  # 设置从那个等级开始提示
        self.m_textCtrl1.SetValue('请输入想要查询的贴吧名字')
        self.m_textCtrl2.SetValue('请输入想要查询的回帖数临界点，仅仅显示大于该临界点的帖子')
        self.m_textCtrl3.SetValue('请输入你要查询的帖子页数')
        self.m_textCtrl4.SetValue('日志如下(日志文件在软件同级目录的test.log)'+'\n')

    # def clear1(self, event):
    #     self.m_textCtrl1.SetValue("")
    # def clear2(self, event):
    #     self.m_textCtrl2.SetValue("")
    # def clear3(self, event):
    #     self.m_textCtrl3.SetValue("")
    def click(self, event):
        # 从一页中提取 帖子
        def extra_from_one_page(page_lst):
            # 临时列表保存字典数据，每一个帖子都是一个字典数据
            tmp = []
            for i in page_lst:
                    if int(i.find(class_='threadlist_rep_num').text) > int(self.m_textCtrl2.GetValue()):
                        dic = {}
                        # 回帖数
                        dic['回帖数'] = int(i.find(class_='threadlist_rep_num').text)
                        # 帖子名称
                        dic['帖子名称'] = i.find(class_='threadlist_title').text
                        # 帖子地址
                        dic['帖子地址'] = 'https://tieba.baidu.com' + i.find(class_='threadlist_title').a['href']
                        tmp.append(dic)
            return tmp
        def search_n_pages(n):
            target = []
            global tiebaanme
            template_url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}"  # 心理学吧
            template_url2 = 'https://tieba.baidu.com/f?kw={}' #未找到指定贴吧
            # 发送多次get请求
            for i in range(n):

                # 跟踪进度
                # print ('page',i)
                logging.info('正在爬取第{}页'.format(i + 1))
                # self.m_textCtrl4.('\n')
                # self.m_textCtrl4.SetValue('正在爬取第{}页'.format(i + 1))
                # 按照浏览贴吧的自然行为，每一页50条
                target_url = template_url.format(self.m_textCtrl1.GetValue(), 50 * i)
                # print(target_url)
                # res2 =requests.get(template_url2)
                try:
                    res = requests.get(target_url)
                except:
                    logging.error('请求失败,请检查网络连接!')
                    self.m_textCtrl4.AppendText('请求失败,请检查网络连接!\n')
                # 转换bs对象,并将html.parser作为解析器
                soup = BeautifulSoup(res.text, 'html.parser')
                # 获取该页帖子列表
                page_list = soup.find_all(class_='j_thread_list')
                # for target_name in soup.find_all('div',class_='card_title'):
                #     list_a = target_name.find_all('a')
                #     for a in  list_a:
                for a in soup.find_all('a',class_=' card_title_fname'):
                        # print(a)
                        # print(a['class'])
                        # print(a['id'])
                        # print(a['href'])
                    # print(a.string)
                    tiebaanme = a.string.replace('\n','').replace(' ','')
                    # print(tiebaanme)
                if self.m_textCtrl1.GetValue()!=tiebaanme:
                    self.m_textCtrl4.AppendText('没找到指定的贴吧，已为您爬取如下贴吧: '+tiebaanme+'\n')
                # if target_name.find(class_='card_title').text != self.m_textCtrl1.GetValue():
                #     self.m_textCtrl4.AppendText('尚未找到指定的贴吧，已帮你找到如下贴吧\n' + i.find(class_='card_title_fname').text)
                # 该页信息保存到target
                target.extend(extra_from_one_page(page_list))
                self.m_textCtrl4.AppendText('正在爬取第{}页'.format(i + 1) + '\n')
                # 休息0.2秒再访问，友好型爬虫
                time.sleep(0.2)
            return target
        # print (self.m_textCtrl3.GetValue())
        try:
            resopnse = search_n_pages(int(self.m_textCtrl3.GetValue()))
            self.m_textCtrl4.AppendText(
                '本次爬取的是“{}”贴吧中回帖数大于 “{}” 的帖子信息，本次爬取{}页\n'.format(tiebaanme,
                                                                 self.m_textCtrl2.GetValue(),
                                                                 self.m_textCtrl3.GetValue()))
            self.m_textCtrl4.AppendText('爬取结束\n')
            # print(resopnse)
        except ValueError as z:
            # print(z)
            self.m_textCtrl4.AppendText('爬取失败，详细日志如下\n')
            self.m_textCtrl4.AppendText('请在第二行、第三行输入整数(第二行输入帖子数，第三行输入页数)\n')
        # print(type(resopnse))
        # 转化为pandas.DataFrame对象
        if resopnse==[]:
            self.m_textCtrl4.AppendText('爬取成功，但是爬取到指定的资源')
        else:
            data = pd.DataFrame(resopnse)
        # print('以下是{}贴吧中回帖数大于{}的帖子信息'.format(self.m_textCtrl1.GetValue(), self.m_textCtrl2.GetValue()))
        # print(data)
        # print(data.columns)
        # 导出到excel表格
            data.to_excel('{}爬取结果.xlsx'.format(self.m_textCtrl1.GetValue()))
    def click2(self,event):
        self.m_textCtrl4.SetValue('日志如下(日志文件在软件同级目录的test.log)' + '\n')

if __name__ == '__main__':
    app = wx.App()
    main_win = Tiebawindow(None)
    main_win.init_main_window()
    main_win.Show()
    app.MainLoop()




# 1.先检查页数
# 2.再检查网络
# 3.再检查帖子数
