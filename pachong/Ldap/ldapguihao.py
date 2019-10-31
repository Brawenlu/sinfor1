#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/30 17:05
# @Author  : Brawenlu
# @File    : ldapguihao.py
# @Software: Sinfor

# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"一键配置ldap服务器", pos=wx.DefaultPosition,
                          size=wx.Size(737, 573), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"输入vpn设备ip", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer2.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_textCtrl1, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"输入控制台账号", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer2.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_textCtrl2, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"输入控制台密码", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        bSizer2.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_textCtrl3, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"输入新建ldap服务器名称，自定义即可，不重复", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        bSizer2.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.m_textCtrl4 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_textCtrl4, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"输入ldap上用户组名（默认10.242.255.72）", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        bSizer2.Add(self.m_staticText5, 0, wx.ALL, 5)

        self.m_textCtrl5 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_textCtrl5, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"映射到本地某组（比如/默认用户组）", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        bSizer2.Add(self.m_staticText7, 0, wx.ALL, 5)

        self.m_textCtrl8 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_textCtrl8, 0, wx.ALL | wx.EXPAND, 5)


        self.m_button1 = wx.Button(self, wx.ID_ANY, u"点击一键配置", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"返回结果如下", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        bSizer4.Add(self.m_staticText6, 0, wx.ALL, 5)

        self.m_textCtrl7 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_textCtrl7, 1, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.click)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def click(self, event):
        event.Skip()


