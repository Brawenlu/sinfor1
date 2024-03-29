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
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title = u"转换ico图片", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.m_button5 = wx.Button(self, wx.ID_ANY, u"浏览（右侧为路径）", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.m_button5, 0, wx.ALL, 5)

        self.m_textCtrl4 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        gSizer1.Add(self.m_textCtrl4, 0, wx.ALL|wx.EXPAND, 5)

        self.m_button6 = wx.Button(self, wx.ID_ANY, u"点击开始转换", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.m_button6, 0, wx.ALL, 5)

        self.m_textCtrl5 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        gSizer1.Add(self.m_textCtrl5, 0, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(gSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button5.Bind(wx.EVT_BUTTON, self.view)
        self.m_button6.Bind(wx.EVT_BUTTON, self.click)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def view(self, event):
        event.Skip()

    def click(self, event):
        event.Skip()


