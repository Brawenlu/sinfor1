#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/30 9:16
# @Author  : Brawenlu
# @Site    : 
# @File    : Gui.py
# @Software: PyCharm
# -*- coding: utf-8 -*-

import wx
import wx.xrc

class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"贴吧爬取", pos=wx.DefaultPosition, size=wx.Size(825,550),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, u"请输入爬取贴吧名", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTRE)
        bSizer1.Add(self.m_textCtrl1, 0, wx.ALL | wx.EXPAND, 5)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, u"请输入指定回帖数", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTRE)
        bSizer1.Add(self.m_textCtrl2, 0, wx.ALL | wx.EXPAND, 5)

        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, u"请输入爬取的页数", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTRE)
        bSizer1.Add(self.m_textCtrl3, 0, wx.ALL | wx.EXPAND, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"点击进行爬取", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
        bSizer1.Add(self.m_button2, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"爬取的日志如下，excel文件在桌面", wx.DefaultPosition, wx.DefaultSize, style = wx.ALIGN_CENTER)
        self.m_staticText1.Wrap(-1)
        bSizer1.Add(self.m_staticText1, 0, wx.ALL | wx.EXPAND, 5)

        self.m_textCtrl4 = wx.TextCtrl(self, wx.ID_ANY, u"日志记录", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE| wx.TE_READONLY | wx.TE_CENTER)
        bSizer1.Add(self.m_textCtrl4, 1, wx.ALL | wx.EXPAND, 5)

        self.m_button21 = wx.Button(self, wx.ID_ANY, u"清空日志", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button21, 0, wx.ALL, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.m_button2.Bind(wx.EVT_BUTTON, self.click)
        self.m_button21.Bind(wx.EVT_BUTTON, self.click2)



    def __del__(self):
        pass

    def click(self, event):
        event.Skip()

