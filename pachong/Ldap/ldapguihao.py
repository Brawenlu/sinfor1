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
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"一键配置ldap", pos=wx.DefaultPosition, size=wx.Size(545, 613),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"ldap服务器（10.242.255.72）"), wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"输入VPN设备IP", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        sbSizer1.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        sbSizer1.Add(self.m_textCtrl1, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText2 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"输入控制台账号", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        sbSizer1.Add(self.m_staticText2, 0, wx.ALL, 5)


        self.m_textCtrl3 = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        sbSizer1.Add(self.m_textCtrl3, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText4 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"输入控制台密码", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        sbSizer1.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.m_textCtrl4 = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        sbSizer1.Add(self.m_textCtrl4, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText7 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"输入想要新建的ldap服务器名字", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        sbSizer1.Add(self.m_staticText7, 0, wx.ALL, 5)

        self.m_textCtrl7 = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        sbSizer1.Add(self.m_textCtrl7, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText5 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"输入72ldap上面的AD组名", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        sbSizer1.Add(self.m_staticText5, 0, wx.ALL, 5)

        self.m_textCtrl5 = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        sbSizer1.Add(self.m_textCtrl5, 0, wx.ALL | wx.EXPAND, 5)

        self.m_button1 = wx.Button(sbSizer1.GetStaticBox(), wx.ID_ANY, u"点击一键配置", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer1.Add(self.m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText6 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"返回结果", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        sbSizer1.Add(self.m_staticText6, 0, wx.ALL, 5)

        self.m_textCtrl6 = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        sbSizer1.Add(self.m_textCtrl6, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sbSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.click)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def click(self, event):
        event.Skip()



