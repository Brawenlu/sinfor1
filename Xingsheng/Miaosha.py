# -*- coding: utf-8 -*-
# @Time    : 2021/6/2 11:37
# @Author  : LWB
# @FileName: Miaosha.py
# @Software: PyCharm
import time
import datetime
#打印当前时间
# now_time = datetime.datetime.now().replace(second=0)
# now_data = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
import requests,json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  #移除SSL警告标签
from hyper.contrib import HTTP20Adapter
session = requests.session()
session.mount("https://mall.xsyxsc.com", HTTP20Adapter())  #使用http2.0的请求，来模拟headers里面带有:,报文格式不一样
now_time = time.strftime("%Y-%m-%d")
# print(now_time)
# print(time.localtime(int(time.time())))
# print(int(time.time()))  #当前时间的浮点数，从1970年
#自定义秒杀时间
miaosha_time = '{} 09:00:00'.format(now_time)
print(miaosha_time)

# print(strtime_to_timestamp(miaosha_time))
# print(miaosha_time-int(time.time()))
#设置打印日志输出，定义一个可变元祖的函数
def printkaishi(*shuzhi):
    print("当前时间runinfo为:"+str(datetime.datetime.now().replace(microsecond=0))+":"+"".join(*shuzhi))

printkaishi("当前时间还没到")
def wait_time(user,store_info):
    printkaishi()

def wait_time_now(user, diff_time=15):
    #为避免当前时间和北京时间差小于difftime，自动断开,在最后15秒前进行日志输出
    flag = True
    while True:
        now_time = int(time.time())
        # print(str_to_timestrmp(miaosha_time))
        if str_to_timestrmp(miaosha_time) - now_time <= diff_time:
            printkaishi("检测到当前时间{} 距离秒杀时间{} 小于{}秒！！，系统自动调用兴盛优选的接口返回时间".format(timestramp_to_date(now_time),miaosha_time,diff_time))
            # print("准备开始日志输出")
            break
        else:
            if  flag:
                #如果flag为false执行下面，也就是如果秒杀时间和本地时间差大于15秒就执行，也就是只执行一次
                printkaishi("您设置的秒杀时间为{} 本地时间为{} 当前秒杀客户为{}, 系统会在距离最后秒杀时间{}秒的时候进行日志输入，请稍等".format(miaosha_time,timestramp_to_date(now_time),user,diff_time))
                flag=False




def str_to_timestrmp(strtime):
    #字符串时间转换成秒级别用于减法
    try:
        # timearray = time.strptime(strtime, "%Y-%m-%d %H:%M:%S")
        timearr = time.strptime(strtime, "%Y-%m-%d %H:%M:%S")
        #格式化时间为元组函数根据指定的格式把一个时间字符串解析为时间元组。
        # print(timearr)
        # print(type(timearr))
    except:
        # print("das")
        printkaishi("你输入的秒杀时间{}不是一个正确的格式的时间，请重新输入：例子为如下：{}".format(strtime,"2021-06-09 10:00:00"))
        exit()
    #将秒杀时间列表转化为浮点数的秒来表示。字符串的时间转化成秒级时间戳
    return int(time.mktime(timearr))
# str_to_timestrmp(miaosha_time)
# print(str_to_timestrmp(miaosha_time))

def timestramp_to_date(timestrmp):
    #时间戳转日期,格式化时间戳为本地的时间
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(timestrmp)))

# print(timestramp_to_date(str_to_timestrmp(miaosha_time)))
# print(time.localtime(int(str_to_timestrmp(miaosha_time))))

wait_time_now("陆文博")

USERKEY = {"陆文博":{'userkey':"45ceb70c-09fa-4b59-871b-fa285bc36b4d"},
           "龙源泉":{'userkey':'c092fc88-4dee-48ef-9f53-ed32a2328229'},
            "龙源泉1":{'userkey':'c092fc88-4dee-48ef-9f53-ed32a23282291'},
           }

class User():
    def __init__(self,username,sleeptime):

        self.username = username
        self.sleeptime = sleeptime
        self.userkey = USERKEY.get(self.username).get('userkey')
        self.wechatinfor = self.get_user_inof()
        self.storeinfor = self.get_storeinfo_by_storid(self.wechatinfor['currentStoreId'])
        self.sku_list = self.col_all_sku()
        # 实例化方法用来直接调用

    def get_user_inof(self):
        # 通过userkey获取用户的相关信息,类中的方法调用不用传参，类外面的要传参
        url = 'https://user.xsyxsc.com/api/member/user/getUserInfo'
        # headers = {}
        # url = "https://user.xsyxsc.com/api/member/user/getUserInfo"
        # headers1 = {'Host': 'user.xsyxsc.com',
        #             'Content-Type': 'application/x-www-form-urlencoded',
        #             'Accept-Encoding': 'br,gzip,deflate',
        #             'Connection': 'keep-alive',
        #             'Accept': 'application/json,text/plain,*/*',
        #             'User-Agent': 'Mozilla/5.0(iPhone;CPUiPhoneOS11_4likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Mobile/15F79MicroMessenger/7.0.8(0x17000820)NetType/WIFILanguage/zh_CN',
        #             'Referer': 'https://servicewechat.com/wx6025c5470c3cb50c/97/page-frame.html',
        #             'Content-Length': '44',
        #             'Accept-Language': 'zh-cn'}
        # resp = requests.post(url=url, data=body, verify=False, headers=header).json().get("data")
        # print(resp)
        headers = {'Host': 'user.xsyxsc.com',
                   'Connection':'keep-alive',
                   'Content-Length': '44',
                   'Accept': 'application/json, text/plain, */*',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
                   'content-type': 'application/x-www-form-urlencoded',
                   'source': 'applet',
                   'userKey':self.userkey,
                   'version': '1.12.3',
                   ',Referer': 'https://servicewechat.com/wx6025c5470c3cb50c/326/page-frame.html',
                   'Accept-Encoding': 'gzip, deflate, br'}
        body = {"userKey":self.userkey}
        userres = requests.post(url=url,data=body,headers=headers,verify=False).json()
        userinfo = userres['data']
        # userres = requests.post(url=url, data=body, headers=headers, verify=False).json().get('data')
        # print(type(userinfo))
        # print(userres)
        # print(userinfo)
        if userinfo is None:
            printkaishi("用户{}的userkey过期.请及时更新,接口返回值:{}".format(self.username,userres['rspDesc']))
            exit()
        weixinginfo  = {'userId':userinfo['userId'],
                        'userName':userinfo['userName'],
                        "wechatNickName":userinfo['wechatNickName'],
                         "mobileNo":userinfo['mobileNo'],
                        'openId':userinfo['openId'],
                        'userType':userinfo['userType'],
                        'shareStoreId':userinfo['shareStoreId'],
                        'wechatImage':userinfo['wechatImage'],
                        'currentStoreId':userinfo['currentStoreId'],
                        'tmRegistry':userinfo['tmRegistry']
                        }
        # print(weixinginfo)
        printkaishi("根据{},获取到的用户为:{}".format(self.userkey,weixinginfo['wechatNickName']))
        return weixinginfo

    def get_storeinfo_by_storid(self,store_id):
        # 通过store_id来获取store的相关信息,自提点信息等
        url = 'https://mall-store.xsyxsc.com/mall-store/store/getStoreInfo'
        # url = "https://mall-store.xsyxsc.com/mall-store/store/getStoreInfo"
        headers = {"Host":"mall-store.xsyxsc.com",
                   "Connection":"keep-alive",
                   "Content-Length":"22",
                   "Accept":"application/json, text/plain, */*",
                   "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
                   "content-type":"application/x-www-form-urlencoded",
                   "userKey":self.userkey,
                   "preBuy":"true",
                   "source":"applet",
                   "version":"1.12.8",
                   "Referer":"https://servicewechat.com/wx6025c5470c3cb50c/333/page-frame.html",
                   "Accept-Encoding":"gzip, deflate, br"
                   }
        body = {"userKey":self.userkey,"storeId":store_id}
        # print(body)
        res = session.post(url=url, data=body, verify=False, headers=headers).json()['data']
        # res = json.dumps(res,ensure_ascii=False, sort_keys=True,indent=2)
        # print(type(res))
        # print(res)
        store_info = {"storeId":res['storeId'],
                      "storeCode":res['storeCode'],
                      "areaId":res['areaId'],
                      "areaName":res['areaName'],
                      "storeName":res['storeName'],
                      "detailAddress":res['detailAddress'],
                      "contactsTel":res['contactsTel'],
                      "wechatGroupName":res['wechatGroupName'],
                      "provinceId":res['provinceId'],
                      "countyId":res['countyId'],
                      "cityId":res['cityId']
                     }
        # print(store_info)
        printkaishi("根据store_id:{}获取到的自提点名称为:{}".format(store_id,store_info['storeName']))
        return store_info

    def col_all_sku(self):
        sku = Skuinfo(userkey=self.userkey,store_info=self.storeinfor)
        return sku


class Skuinfo():
    #获得商品信息类
    def __init__(self,userkey,store_info):
        self.userkey = userkey
        self.store_infor = store_info
        print(self.userkey,self.store_infor)
        self.url = 'https://mall.xsyxsc.com'
        # self.loadproducet_sku = self.get_windows_id()
        self.load_index_sku = self.xiazai_sku_index(**self.get_windows_id())

    def get_windows_id(self):
        """根据首页的id来获取首页商品信息id,"""
        headers = {"Host":"mall.xsyxsc.com",
                   "Connection": "keep-alive",
                   "Content-Length": "98",
                   "Accept":"application/json, text/plain, */*",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
                   "content-type": "application/x-www-form-urlencoded",
                   "preBuy": "true",
                   "source": "applet",
                   "userKey": self.userkey,
                   "version": "1.12.11",
                   "Referer": "https://servicewechat.com/wx6025c5470c3cb50c/336/page-frame.html",
                   "Accept-Encoding": "gzip, deflate, br"}
        body = {"userKey":self.userkey,
                "storeId":self.store_infor['storeId'],
                "areaId":self.store_infor['areaId'],
                "openBrandHouse":"OPEN"}
        index_windowsinfor = {}
        # /user/product/indexSortWindows  老接口  新街口/user/product/Windows 用老接口数据多
        resp = session.post(url=self.url+"/user/product/indexSortWindows",data=body,headers=headers,verify=False).json()['data']
        # print(resp)
        """找个接口返回了activityWindows、brandHouseWindows、classifyWindows,老街口是windows"""
        for window in resp['windows']:  #便利列表
            """只搜索windows类的商品"""
            # print(type(resp['windows']))  #由字典组成的列表
            # print(type(window)) #每个字典
            # print(window)
            printkaishi("搜索到标题为'{}',windows_id为'{}',类型为'{}'".format(window['windowName'],window['windowId'],window['windowType']))
            index_windowsinfor[str(window['windowId'])+'&'+window['windowType']] = window['windowName']
        # for window_1 in resp['classifyWindows']:
        #     """只搜索classifyWindows类的商品"""
        #     index_windowsinfor[str(window_1['windowId'])+'&'+window_1['windowType']] = window_1['windowName']
        # print(index_windowsinfor)
        printkaishi("累计搜到的activityWindows个数为{}".format(len(index_windowsinfor)))
        return index_windowsinfor


    def xiazai_sku_index(self,**awag):
        """将首页所有信息都存到表中"""
        # print(type(awag))
        print(awag)
        now = time.time()  #获得时间戳
        api_timestamp = round(now*1000)   #13位再四舍五入舍弃.后面的
        # print(now*1000)
        # print(api_timestamp)
        for id_type in awag:
            window_id,window_type = id_type.split('&')
            # print(id_type)
            # print(window_id,window_type)
            # if window_type in ['ACTIVITY','CLASSIFY']:
            #     url = self.url + ''
        url = self.url+'/user/product/getConfigWindowProducts'
        headers = {":method":"POST",
                   ":scheme":"https",
                   ":path":"/user/product/getConfigWindowProducts",
                   ":authority":"mall.xsyxsc.com",
                   "content-type":"application/json",
                   "accept":"application/json, text/plain, */*",
                   "version":"1.12.15",
                   "userkey":self.userkey,
                   "api-version":"V3",
                   "source":"applet",
                   "accept-language":"zh-cn",
                   "accept-encoding":"gzip, deflate, br",
                   "api-sign":"88bc16010de349b6cc6b37b1d0ae195e",
                   "clienttype":"MINI_PROGRAM",
                   "user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.1(0x1800012a) NetType/WIFI Language/zh_CN",
                   "prebuy": "true",
                   "api-timestamp": str(api_timestamp),
                   "referer": "https://servicewechat.com/wx6025c5470c3cb50c/341/page-frame.html",
                   "content-length": "261",
                   }
        body = {'clientType':'MINI_PROGRAM',
                'userKey':self.userkey,
                'areaId':self.store_infor['areaId'],
                'storeId':self.store_infor['storeId'],
                'provinceCode':self.store_infor['provinceId'],
                'cityCode':self.store_infor['cityId'],
                'areaCode':self.store_infor['countyId'],
                'saleRegionCode':self.store_infor['areaId'],
                'channelUse':'WXAPP',
                'requireCoupon':'TRUE',
                'userScopeTypes':["NORMAL"],
               }
        res = session.post(url=url,data=body,headers=headers,verify=False)
        print(res.text)



    # def










if __name__ == '__main__':
    user = User(username='龙源泉',sleeptime=14)
    # user.get_user_inof()
    







