#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/31 16:22
# @Author  : Brawenlu
# @File    : redishao.py
# @Software: Sinfor

import requests,re,hashlib,urllib,ssl,json,wx
import http.cookiejar,redisgui

class Create(redisgui.MyFrame1):
    def __init__(self, parent):
        redisgui.MyFrame1.__init__(self, parent)
        # self.m_textCtrl8.SetValue('/默认用户组')
        # self.m_textCtrl4.SetValue('输入单号')
        # ip = '10.242.1.170'
        # port = '4430'
        # user = 'admin'
        # pwd = 'sangfor123'
        ssl._create_default_https_context = ssl._create_unverified_context

    def click(self, event):
        ip = self.m_textCtrl1.GetValue()
        port = '4430'
        user = self.m_textCtrl3.GetValue()
        pwd = self.m_textCtrl4.GetValue()
        def getsession(ip, port):
            url = "https://{}:{}/cgi-bin/login.cgi?requestname=2&cmd=0".format(ip, port)
            res = requests.get(url=url, verify=False)
            # print(res,res.cookies)
            # for i in res.cookies:
            # print(i)
            cookie = re.findall(r'sinfor_session_id=([^"]+)', str(res.cookies))
            cookiefengehou = cookie[0].split(' ')
            cookie = cookiefengehou[0]
            # print(cookiefengehou[0])
            # print(cookie)
            # print(url)
            return cookie

        def login(ip, user, psw, cookie, port):
            url = "https://{}:{}/cgi-bin/login.cgi?requestname=2&cmd=0".format(ip, port)
            pwd_cookie = psw + cookie  # 秘钥加密方式
            s1 = hashlib.sha1()  # 创建sha1对象
            s1.update(pwd_cookie.encode())  # 指定编码格式，否则会报错 # 对s1进行更新
            pwd = s1.hexdigest()  # 加密处理
            # print(pwd)
            data = {
                'user': '{}'.format(user),
                'password': '{}'.format(pwd),
                'logintime': '1',
                'program': '3',
                'language': 'zh_CN',
                # 'privacy': '1',
            }

            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Length': '107',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': 'language=zh_CN; PHPSESSID=59e6ff9af1f514503f9b55d84291beff; x-act-flag-gcs=; x-anti-csrf-gcs=925ADE0700CAAE76; sinfor_session_id={}'.format(
                    cookie),
                'Host': '{}:{}'.format(ip, port),
                'Origin': 'https://{}:{}'.format(ip, port),
                'Pragma': 'no-cache',
                'Referer': 'https://{}:{}/cgi-bin/login.cgi?requestname=0&cmd=0'.format(ip, port),
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',

            }
            cookies = {}
            # loginres = urllib.request.Request(url=url,data=data,headers=header)
            # print(loginres.text())
            # print('111')
            # print(loginres.headers['Cookie'])
            PHPSESSID1 = re.findall(r'PHPSESSID=([^"]+)', str(header['Cookie']))
            PHPSESSID1 = PHPSESSID1[0].split(';')[0]
            # print(PHPSESSID1)
            cookies['PHPSESSID'] = PHPSESSID1

            login_res2 = requests.post(url=url, data=data, headers=header, verify=False)
            login_res2.encoding = login_res2.apparent_encoding
            # print(login_res2.cookies)
            cookies1 = re.findall(r'sinfor_session_id=([^"]+)', str(login_res2.cookies))
            cookiefengehou = cookies1[0].split(' ')[0]
            # print(cookies1)
            cookies['sinfor_session_id'] = cookiefengehou
            # print(cookies)
            return cookies

        # cookielist = login(ip,user,pwd,getsession(ip,port),port)
        # def Ldapadd(ip,port,cookielist):
        #     PHPSESSID = cookielist['PHPSESSID']
        #     # PHPSESSID='b5e86e233926217ab2d0d561e26dca53'
        #     sinfor_session_id = cookielist['sinfor_session_id']
        #     # print(PHPSESSID)
        #     s1 = hashlib.sha1()
        #     s1.update((cookielist['sinfor_session_id']).encode("utf8"))  # 指定编码格式
        #     tooken = s1.hexdigest()#token是怎么来的加密(必须要这样加密)
        #     # print(tooken)
        #     url ='https://{0}:{1}/cgi-bin/php-cgi/html/delegatemodule/HttpHandler.php?controler=ExtAuth&action=AddLDAP&token={2}'.format(ip,port,tooken)
        #     # print(url)
        #     headers = {
        #         'Accept': '*/*',
        #         'Accept-Encoding': 'gzip, deflate, br',
        #         'Accept-Language': 'zh-CN,zh;q=0.9',
        #         'X-Requested-With': 'XMLHttpRequest',
        #         'Connection': 'keep-alive',
        #         'Content-Length': '634',
        #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #         'Cookie': 'language=zh_CN; PHPSESSID={0}; x-act-flag-gcs=; AlarmLogTime=%222018-07-18%2014%3A30%3A59%22; sinfor_session_id={1}; x-anti-csrf-gcs=89E91B7000692F33'.format(
        #             PHPSESSID, sinfor_session_id),
        #         'Host': '%s:%s' % (ip, port),
        #         'Origin': 'https://{}:{}'.format(ip, port),
        #         'Referer': 'https://{}:{}/html/tpl/ldapMgt.html'.format(ip, port),
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        #     }
        #     data ={"l_bindrc_attr":"",
        #            "charset":'GBK',
        #            'portsStr':'389',
        #            'hostsStr':'["10.242.255.72"]',
        #            'name':'ldap72的1',
        #            'note':'',
        #            'args':'',
        #            'l_admin':'Administrator@sslt.com',
        #            'l_adminpass':'Sangfor123',
        #            'l_userdn':'OU=lwb222,DC=sslt,DC=com',
        #            'l_subtree':'1',
        #            'timeout':'15',
        #            'enable':'1',
        #            'authtype':'0',
        #            'l_userflag':'sAMAccountName',
        #            'l_userfilter':'objectCategory=person',
        #            'l_mobilename':'telephoneNumber',
        #            'l_ipname':'',
        #            'l_ipmaskname':'',
        #            'ladpKeyTypeSelect': 'md5',
        #            'ladpKeyTypeForMd5_len': '0',
        #            'ladpKeyTypeForMd5_word': '0',
        #            'ladpKeyTypeForSha1_word': '0',
        #            'is_enable_role_map': '1',
        #            'grpid': '-1',
        #            'grpid_': '/默认用户组',
        #            'r_mobileid': '',
        #            'r_ipid': '',
        #            'r_ipmaskid': '',
        #            'bindOUStr': '[]',
        #            'bindRoleStr': '',
        #            'password_type': '0',
        #            'l_allow_nil_pwd': '0',
        #            }
        #     res = requests.post(url=url,data=data,headers=headers,verify=False)
        #     # print(res.content)
        #     print(res.json()['message'])

        # print(type(res.content))
        def redisadd(ip, port, cookielist):
            # PHPSESSID = cookielist['PHPSESSID']
            # print(ip,port,cookielist)
            PHPSESSID = cookielist['PHPSESSID']
            # PHPSESSID='b5e86e233926217ab2d0d561e26dca53'
            sinfor_session_id = cookielist['sinfor_session_id']
            # print(PHPSESSID)
            s1 = hashlib.sha1()
            s1.update((cookielist['sinfor_session_id']).encode("utf8"))  # 指定编码格式
            tooken = s1.hexdigest()  # token是怎么来的加密(必须要这样加密)
            # print(tooken)
            url = 'https://{0}:{1}/cgi-bin/php-cgi/html/delegatemodule/HttpHandler.php?controler=ExtAuth&action=AddRadius&token={2}'.format(
                ip, port, tooken)
            # print(url)
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
                'Content-Length': '634',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'language=zh_CN; PHPSESSID={0}; x-act-flag-gcs=; AlarmLogTime=%222018-07-18%2014%3A30%3A59%22; sinfor_session_id={1}; x-anti-csrf-gcs=89E91B7000692F33'.format(
                    PHPSESSID, sinfor_session_id),
                'Host': '%s:%s' % (ip, port),
                'Origin': 'https://{}:{}'.format(ip, port),
                'Referer': 'https://{}:{}/html/tpl/radiusMgt.html'.format(ip, port),
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            }
            data = {"r_makegroup": "",
                    "portsStr": self.m_textCtrl5.GetValue(),
                    'hostsStr': '["{}"]'.format(self.m_textCtrl17.GetValue()),
                    'bindStr	': '',
                    'name': self.m_textCtrl7.GetValue(),
                    'note': '',
                    'args': '',
                    'r_method': '1',
                    'r_secret': self.m_textCtrl8.GetValue(),
                    'charset': 'UTF-8',
                    'timeout': '5',
                    'enable': '1',
                    'radius_cost': '0',
                    'cost_port': '1813',
                    'r_mobileid': '-1',
                    'r_mobilesubid': '-1',
                    'r_ipid': '-1',
                    'r_ipsubid': '-1',
                    'r_ipmaskid': '-1',
                    'r_ipmasksubid': '-1',
                    'grpid': '-1',
                    'grptext': '/默认用户组',
                    'password_type': '',
                    }
            res = requests.post(url=url, data=data, headers=headers, verify=False)
            # print(res.content)
            self.m_textCtrl6.SetValue(res.json()['message'])
            # print(res.json()['message'])
            urlupdate = 'https://{}:{}/cgi-bin/php-cgi/html/delegatemodule/HttpHandler.php?controler=Updater&action=Update&token={}'.format(
                ip, port, tooken)
            headers2 = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'X-Requested-With': 'XMLHttpRequest',
                'Sec-Fetch-Mode':'cors',
                'Connection': 'keep-alive',
                'Content-Length': '29',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'language=zh_CN; PHPSESSID={0}; x-act-flag-gcs=; AlarmLogTime=%222018-07-18%2014%3A30%3A59%22; sinfor_session_id={1}; x-anti-csrf-gcs=89E91B7000692F33'.format(
                    PHPSESSID, sinfor_session_id),
                'Host': '%s:%s' % (ip, port),
                'Origin': 'https://{}:{}'.format(ip, port),
                'Referer': 'https://{}:{}/cgi-bin/login.cgi?requestname=7&cmd=0'.format(ip, port),
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            }

            data2 ={'isNeedCheckCommunication':'true'}
            res2 = requests.post(url=urlupdate,headers=headers2,data=data2,verify=False)
            # print(res2.json())







        redisadd(ip, port, login(ip, user, pwd, getsession(ip, port), port))

        # def update(ip,port,token,cookielist):
        #     url = 'https://{}:{}/cgi-bin/php-cgi/html/delegatemodule/HttpHandler.php?controler=Updater&action=Update&token={}'.format(ip,port,token)




        # update(ip,port,token,login(ip, user, pwd, getsession(ip, port), port))

if __name__=='__main__':
    app = wx.App()
    main_win = Create(None)
    # main_win.init_main_window()
    main_win.Show()
    app.MainLoop()