#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 14:04
# @Author  : Brawenlu
# @Site    : 
# @File    : Test.py
# @Software: PyCharm
import requests
import json
host = 'http://sigma-test.17daxue.cn'
path = '/web-sigma/api/v2/mathsGo/learningRooms'
url = host+path
# print url
header = {'content-type':'application/json; charset=utf-8'}
header2 = {"content_type":"multipart/form-data"}
data = {'query':'{"andCondition":{"courseRoomId":"fa6cb98e44d44cdc88c3915f0206659d"},"orderByCondition":{"createdDt":"desc"},"page":1,"pageObj":{"currentPage":1,"size":1},"pageSize":100}',
        '_token_':'be91c04c0fd539d2e39d6336f75e2b05'}
response = requests.get(url=url,params=data)
res = json.dumps(response.json(),indent=2,ensure_ascii=False)
# print res