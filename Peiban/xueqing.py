#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/8 9:20
# @Author  : Brawenlu
# @Site    : 
# @File    : xueqing.py
# @Software: PyCharm
import requests,json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
value = []
room_id='04d92a7b626648e6aa2600e3f214b3fe'
request = 'https://sigma.17daxue.com/web-sigma/api/v2/mathsGo/courseReports/'+room_id
req1 = requests.get(url=request)
# print json.dumps(req1.json(),indent=2,sort_keys=True,ensure_ascii=False)
name = '知识快问快答-1'
responmse = req1.json()
# print responmse['obj']['courseRoomProblemReportVOList']
for value in responmse['obj']['courseRoomProblemReportVOList']:
    while name ==value['rateInCourse'].encode("utf-8"):
        print (value['rateInCourse']+'的详细数据为:'+str(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)))
        print('当前的提问数为:'+str(value['askNum']))
        break