#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 9:33
# @Author  : Brawenlu
# @Site    : 
# @File    : Fenye.py
# @Software: PyCharm
# python在发送请求的时候最好用''，get用params，post用data  sort_keys=True排序，indent缩进
import requests
import json
import sys
# reload(sys)
sys.setdefaultencoding('utf-8')
# 解决的方案很简单，修改默认的编码模式，我们可以通过sys.setdefaultencoding(‘utf-8’)来将当前的字符处理模式修改为utf-8编码模式，值得注意的是，如果单纯这么调用的话，Python会抛出一个AttributeError异常：需要调用一次reload(sys)。
currentPage = 0
Name = []
name ='1.1.1数集与点集的区别（BC）4'
print (type(name))
host = 'http://sigma-test.17daxue.cn'
path = '/web-sigma/api/v2/mathsGo/learningRooms'
url = host+path
# print url
header = {'content-type':'application/json; charset=utf-8'}
header2 = {"content_type":"multipart/form-data"}
data = {'query':'{"andCondition":{"courseRoomId":"fa6cb98e44d44cdc88c3915f0206659d"},"orderByCondition":{"createdDt":"desc"},"page":1,"pageObj":{"currentPage":1,"size":2},"pageSize":100}',
        '_token_':'be91c04c0fd539d2e39d6336f75e2b05'}
response = requests.get(url=url, params=data)
response = response.json()
print (response)
total = response['obj']['totalElements']
pagesize = response['obj']['currentPage']
if total % 2 == 0:
    pagesum = total/pagesize
else:
    pagesum = (total+1)/pagesize
while currentPage<pagesum:
    data = {
        'query': {"andCondition":{"courseRoomId":"fa6cb98e44d44cdc88c3915f0206659d"},"orderByCondition":{"createdDt":"desc"},"page":1,"pageObj":{currentPage:1,"size":1},"pageSize":100},
        '_token_': 'be91c04c0fd539d2e39d6336f75e2b05'}
    request1 = requests.get(url=url, params=data)
    response1 = request1.json()
    for value in response1['obj']['list']:
        # print type(name)
        # print type(value['name'])
        # print value['name']
        if name==value['name'].encode("utf-8"):
            # raise Exception('找到了' + value['name'])
            # print 'dadas'
            print ("当前页数为:"+str(currentPage+1))
            print(value['name'].encode("utf-8") + '的详细数据为'+str(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False)))
        Name.append(value['name'])
    currentPage+=1
print ('教室的个数为:'+str(len(Name)))





# response2 = response.json()
# print response2
# res = (json.dumps(response.json(),indent=4,ensure_ascii=False))
# for value in response2['obj']['list']:
#     print value['name']
