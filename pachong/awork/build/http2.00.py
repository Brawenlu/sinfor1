# -*- coding: utf-8 -*-
# @Time    : 2019/12/16 9:52
# @Author  : LWB
# @FileName: http2.00.py
# @Software: PyCharm
# @project_name :person
# @file_name :http2
# @auth :xiejiangpeng
# @time :2019-12-07
# @software :PyCharm
# @message http2.0
import requests
from hyper.contrib import HTTP20Adapter
# from hyper.contrib import HTTP20Adapter


def get_sys_time():
    """

    """
    host = "https://mall-store.xsyxsc.com"
    path = "/mall-store/common/getSysParam"
    headers = {':method': 'POST',
               ':scheme': 'https',
               ':path': path,
               ':authority': host.replace("https://", ""),
               'accept': 'application/json,text/plain,*/*',
               'content-type': 'application/x-www-form-urlencoded', 'content-length': '75', 'accept-language': 'zh-cn',
               'user-agent': 'Mozilla/5.0(iPhone;CPUiPhoneOS11_4likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Mobile/15F79MicroMessenger/7.0.8(0x17000820)NetType/WIFILanguage/zh_CN',
               'referer': 'https://servicewechat.com/wx6025c5470c3cb50c/96/page-frame.html',
               'accept-encoding': 'br,gzip,deflate'}
    body = {'codes': '7Z_LIMIT_TIME',
            'areaId': 101,
            'userKey': '5a7217e8-ca9a-5a74-8fb7-0896cbbd66b8'}
    session = requests.session()
    session.mount("https://", HTTP20Adapter())
    proxies = {"https": "127.0.0.1:8888"}
    resp = session.post(host + path, data=body, headers=headers, verify=False, proxies=proxies)
    print(resp.json())
    print(resp.request.headers)
    print(resp.raw)
    return resp.json().get("data").get("time")


get_sys_time()
