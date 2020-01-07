# @project_name :person
# @file_name :xingshengyouxuan_http2
# @auth :xiejiangpeng
# @time :2019-12-09
# @software :PyCharm
# @messagehttp2.0版本
import requests
import pandas as pd
import datetime
import os
import time
import json
import threading
import queue as Queue
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
from hyper.contrib import HTTP20Adapter

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

event = threading.Event()

SESSION = requests.session()
SESSION.mount("https://", HTTP20Adapter())


class MyTread(threading.Thread):

    def __init__(self, thread_name, q):
        super().__init__()
        self.name = thread_name
        self.q = q

    def run(self):
        myprint("开始线程{}".format(self.name))
        while True:
            try:
                user, sleep_time, sku_name = self.q.get(timeout=1)
                if not self.q.qsize():
                    event.set()  # 当队列全部被取完的时候，放行全部的线程
                event.wait()
                user = User(username=user, sleep_time=sleep_time)
                user.to_buy_sku(sku_name_list=sku_name)
            except Queue.Empty:
                break
            # except Exception as ex:
            #     myprint("线程 {} 发生未知错误 错误信息为{}".format(threading.current_thread().getName(), ex))
        myprint("线程{}结束了".format(threading.current_thread().getName()))


USER_INFO = {
    '谢江鹏': {
        'userkey': '15dbd5ef-3f9c-4f22-bc9c-537a5c6f9b54',
    },
    '谢江鹏小号': {
        'userkey': '9980b8ef-ebab-41fa-9b51-daf14c713634',
    },
    '彭敏': {
        'userkey': 'c2f8a702-e79b-4ec6-b9c1-1c59d2de8810',
    },
    '彭敏小号': {
        'userkey': '67ce9a73-77f3-4bb6-9cb0-05c01607e16b',
    },
    '曾元明一号': {
        'userkey': 'c9fc9dc7-39f3-46a2-8138-cf753afa8727'
    },
    '曾元明二号': {
        'userkey': 'c1410a8f-a0fb-4e18-bc44-f865f8f9f42d'
    },
    '曾元明三号': {
        'userkey': '2d646317-4684-485a-b8f2-621974ea52c2'
    },
    '曾元明四号': {
        'userkey': '43e480de-d495-481d-87eb-4057bc6a987b'
    },
    '刘清铭': {
        'userkey': '7eae4380-61e5-43e3-a466-ca1384555ec8'
    },
    '刘清铭小号': {
        'userkey': '1951e84e-99dc-4f78-8c40-2bd38ea9579c'
    },
    '易磊': {
        'userkey': 'e94bbbbf-1b5b-4247-91d2-8147c2a70823'
    },
    '陆文博': {
        'userkey': '0a7d98e4-6750-4493-9070-d054ec53bf19'
    },
    '方才': {
        'userkey': '2fa28220-a089-45b4-89c1-95ba46fe6821'
    },
    '罗峥': {
        'userkey': '81f26266-9d5b-425a-89f4-8c8ff171b403'
    },
    '陆文博小号': {
        'userkey': '7f836e5c-33a3-4536-bfa8-893f554754bc'
    },
    '朱勇': {
        'userkey': 'd3475d93-51a8-4ebf-819f-2372cca11a3c'
    } ,
    '蒋宗涛': {
        'userkey': '2171051f-e783-4efa-91a2-8cc30aa2d058'
    },
}

now_data = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
# START_TIME = str(input("请在下方输入您需要秒杀的时间 例如'{} 10:00:00'\n".format(now_data))).strip()
START_TIME = '{} 10:30:00'.format(now_data)
DIFF_TIME = 2  # 本机与北京时间的最大时间差 单位：秒,值如果小于真实时间差，可能导致秒杀不到商品


def myprint(*con):
    print("RunInfo----" + str(datetime.datetime.now().replace(microsecond=0)) + ":" + "".join(*con))


def wait_time(user, store_info):
    wait_time_now(user=user, diff_time=DIFF_TIME)
    while True:
        sys_time = str(get_sys_time(store_info=store_info))
        if strtime_to_timestamp(sys_time) >= strtime_to_timestamp(START_TIME):
            myprint("达到秒杀开始时间{} 正在准备秒杀".format(sys_time))
            break
        else:
            myprint("暂未到开始秒杀时间 您设置的秒杀时间为{} 兴盛优选显示时间为{}--当前秒杀客户为{}".format(START_TIME, sys_time, user))


def wait_time_now(user, diff_time=20):
    """为了避免频繁调取兴盛优选获取时间接口，此方法主要用于长期等待，若当前时间跟秒杀时间相差小于diff_time秒时，自动断开

    """
    flag = False
    while True:
        now_time = int(time.time())
        if strtime_to_timestamp(START_TIME) - now_time <= diff_time:
            myprint("检测到当前时间'{}'与秒杀时间距离小于{}秒！！，系统自动采取兴盛优选接口返回时间。".format(timestamp_to_date(now_time), diff_time))
            break
        else:
            if not flag:
                myprint(
                    "您设置的秒杀时间为{}  本地时间为{}--当前秒杀客户为{},系统会在距离最后秒杀时间{}秒的时候继续进行日志输出，请耐心等候".format(START_TIME,
                                                                                              timestamp_to_date(
                                                                                                  now_time),
                                                                                              user,
                                                                                              diff_time))
                flag = True


def get_sys_time(store_info):
    """调用兴盛优选的接口获取当前时间

    """
    url = "https://mall-store.xsyxsc.com/mall-store/common/getSysParam"
    body = {'codes': '7Z_LIMIT_TIME',
            'areaId': store_info.get("areaId"),
            'userKey': '5a7217e8-ca9a-5a74-8fb7-0896cbbd66b8'}
    resp = requests.post(url=url, data=body, verify=False).json()
    return resp.get("data").get("time")


def strtime_to_timestamp(str_time):
    """

    :param str_time: 字符串的时间转化成秒级时间戳
    """
    try:
        timearray = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    except:
        myprint("您输入的秒杀时间'{}'不符合日期格式 请重新输入  正确例子：{}".format(str_time, "2019-08-23 10:10:00"))
        exit()
    return int(time.mktime(timearray))


def timestamp_to_date(timestamp):
    """时间戳转日期时分秒

    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))


class User(object):
    def __init__(self, username, sleep_time):
        """实例化一个用户

        :param username: 用户名称
        """
        self.username = username
        self.sleep_time = sleep_time
        self.userkey = USER_INFO.get(username).get("userkey")
        self.base_param = {'userKey': self.userkey}
        self.header = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/7.0.4(0x17000428) NetType/WIFI Language/zh_CN'}
        self.wechat_info = self.get_user_info()
        self.store_info = self.get_store_info_by_store_id(self.wechat_info.get("currentStoreId"))
        self.all_sku_list = self.coll_all_sku()

    def get_user_info(self):
        """根据userkey获取用户的相关信息12.09 抓包的时候 这个接口还不是http2.0

        :return:返回用户信息
        """
        url = "https://yd.frxs.cn/api/user/user/getUserInfo"
        header = {'Host': 'user.xsyxsc.com', 'Content-Type': 'application/x-www-form-urlencoded',
                  'Accept-Encoding': 'br,gzip,deflate', 'Connection': 'keep-alive',
                  'Accept': 'application/json,text/plain,*/*',
                  'User-Agent': 'Mozilla/5.0(iPhone;CPUiPhoneOS11_4likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Mobile/15F79MicroMessenger/7.0.8(0x17000820)NetType/WIFILanguage/zh_CN',
                  'Referer': 'https://servicewechat.com/wx6025c5470c3cb50c/97/page-frame.html', 'Content-Length': '44',
                  'Accept-Language': 'zh-cn'}
        body = {'userKey': self.userkey}
        resp = requests.post(url=url, data=body, verify=False, headers=header).json().get("data")
        if resp is None:
            myprint("用户{} 的userkey失效，请更新 接口返回响应为 {}".format(self.username,
                                                            requests.post(url=url, data=body, verify=False).json().get(
                                                                "rspDesc")))
            exit()
        wechat_info = {'userId': resp.get("userId"),
                       'userName': resp.get("userName"),
                       'mobileNo': resp.get("mobileNo"),
                       'wechatNickName': resp.get("wechatNickName"),
                       'openId': resp.get("openId"),
                       'openType': resp.get("openType"),
                       'userType': resp.get('userType'),
                       'currentStoreId': resp.get("currentStoreId"),
                       'wechatImage': resp.get("wechatImage")}
        myprint("根据{} 获取到当前用户的微信名为'{}'".format(self.userkey, wechat_info.get("wechatNickName")))
        return wechat_info

    def get_store_info_by_store_id(self, sotre_id):
        """通过storeid获取相关信息（团长/自提点）

        :param sotre_id: 自提点id
        """
        url = "https://mall-store.xsyxsc.com/mall-store/store/getStoreInfo"
        headers = {':method': 'POST', ':scheme': 'https', ':path': '/mall-store/store/getStoreInfo',
                   ':authority': 'mall-store.xsyxsc.com', 'accept': 'application/json,text/plain,*/*',
                   'content-type': 'application/x-www-form-urlencoded', 'content-length': '67',
                   'accept-language': 'zh-cn',
                   'user-agent': 'Mozilla/5.0(iPhone;CPUiPhoneOS11_4likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Mobile/15F79MicroMessenger/7.0.8(0x17000820)NetType/4GLanguage/zh_CN',
                   'referer': 'https://servicewechat.com/wx6025c5470c3cb50c/97/page-frame.html',
                   'accept-encoding': 'br,gzip,deflate'}
        body = {'storeId': sotre_id, 'userKey': self.userkey}
        resp = SESSION.post(url=url, data=body, verify=False, headers=headers).json().get("data")
        store_info = {'storeId': resp.get("storeId"),
                      'storeCode': resp.get("storeCode"),
                      'areaId': resp.get("areaId"),
                      'areaName': resp.get("areaName"),
                      'storeName': resp.get("storeName"),
                      'warehouseName': resp.get("warehouseName"),
                      'warehouseId': resp.get("warehouseId"),
                      'detailAddress': resp.get("detailAddress"),
                      'contactsTel': resp.get("contactsTel"),  # 自提点号码
                      'wechatGroupName': resp.get("wechatGroupName"),  # 自提点微信名
                      'lineId': resp.get("lineId"),  # 线路id
                      'lineName': resp.get("lineName")  # 线路名称
                      }
        myprint("根据store_id {} 获取得到自提点名称为'{}'".format(sotre_id, store_info.get("storeName")))
        return store_info

    def coll_all_sku(self):
        """收集所有的商品信息
        """
        sku = Sku(user_key=self.userkey, store_info=self.store_info)
        return sku.sku_info_list

    def to_buy_sku(self, sku_name_list):
        """

        :param sku_name_list: 商品名称列表
        """
        Order(username=self.username, user_key=self.userkey, store_info=self.store_info, wechat_info=self.wechat_info,
              all_sku_list=self.all_sku_list, listname=sku_name_list, sleep_time=self.sleep_time)


class Sku(object):
    def __init__(self, user_key, store_info):
        self.userkey = user_key
        self.store_info = store_info
        self.base_param = {'userKey': self.userkey}
        self.header = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/7.0.4(0x17000428) NetType/WIFI Language/zh_CN'}
        self.url = "https://mall.xsyxsc.com"
        self.sku_info_list = []
        self.sku_name = {}  # 用于去重
        self.load_index_sku(**self.get_windows_id())
        self.to_excel_data()

    def get_windows_id(self):
        """获取首页返回的windowId

        :return: 首页window信息 key为id&tpye value为标题
        """
        headers = {':method': 'POST', ':scheme': 'https', ':path': '/user/product/indexSortWindows',
                   ':authority': 'mall.xsyxsc.com', 'accept': 'application/json,text/plain,*/*',
                   'content-type': 'application/x-www-form-urlencoded', 'content-length': '78',
                   'accept-language': 'zh-cn',
                   'user-agent': 'Mozilla/5.0(iPhone;CPUiPhoneOS11_4likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Mobile/15F79MicroMessenger/7.0.8(0x17000820)NetType/4GLanguage/zh_CN',
                   'referer': 'https://servicewechat.com/wx6025c5470c3cb50c/97/page-frame.html',
                   'accept-encoding': 'br,gzip,deflate'}
        index_window_info = {}
        body = {'areaId': self.store_info.get("areaId"),
                'storeId': self.store_info.get("storeId")}
        body.update(self.base_param)
        resp = SESSION.post(url=self.url + "/user/product/indexSortWindows", data=body, headers=headers,
                            verify=False).json().get(
            "data")
        """其实这个接口返回了
           windows brandHouseWindows  classifyWindows
           细心观察可知  windows才是全部的 其次分类界面所有的分类也是属于其中
           """
        for window in resp.get("windows"):
            # if "秒杀" not in window.get("windowName"):  # 只购买秒杀商品
            #     continue
            myprint("搜索到标题为'{}'  windows_id为'{}'  类型为'{}'".format(window.get("windowName"), window.get("windowId"),
                                                                  window.get("windowType")))
            index_window_info[str(window.get("windowId")) + "&" + window.get("windowType")] = window.get("windowName")
        myprint("合计搜索到的windows个数为{}".format(len(index_window_info)))
        return index_window_info

    def load_index_sku(self, **kwargs):
        """将首页的所有商品信息添加到sku列表中

        :param kwargs: 函数 get_windows_id的返回值
        """
        for id_type in kwargs:
            windowid, windowtype = id_type.split("&")
            if windowtype in ("ACTIVITY", "CLASSIFY"):
                url = self.url + "/user/product/{}Products".format(windowtype.lower())
                if windowtype == "ACTIVITY":
                    body = {'windowId': windowid, 'openBrandHouse': 'OPEN', 'storeId': self.store_info.get("storeId"),
                            'areaId': self.store_info.get("areaId")}
                    headers = {':method': 'POST', ':scheme': 'https', ':path': '/user/product/activityProducts',
                               ':authority': 'mall.xsyxsc.com', 'accept': 'application/json,text/plain,*/*',
                               'content-type': 'application/x-www-form-urlencoded', 'content-length': '109',
                               'accept-language': 'zh-cn',
                               'user-agent': 'Mozilla/5.0(iPhone;CPUiPhoneOS11_4likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Mobile/15F79MicroMessenger/7.0.8(0x17000820)NetType/4GLanguage/zh_CN',
                               'referer': 'https://servicewechat.com/wx6025c5470c3cb50c/97/page-frame.html',
                               'accept-encoding': 'br,gzip,deflate'}
                else:
                    body = {'windowId': windowid, 'areaId': self.store_info.get("areaId"),
                            'storeId': self.store_info.get("storeId"), 'excludeAct': 'N'}
                    headers = {':method': 'POST', ':scheme': 'https', ':path': '/user/product/classifyProducts',
                               ':authority': 'mall.xsyxsc.com', 'accept': 'application/json,text/plain,*/*',
                               'content-type': 'application/x-www-form-urlencoded', 'content-length': '103',
                               'accept-language': 'zh-cn',
                               'user-agent': 'Mozilla/5.0(iPhone;CPUiPhoneOS11_4likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Mobile/15F79MicroMessenger/7.0.8(0x17000820)NetType/4GLanguage/zh_CN',
                               'referer': 'https://servicewechat.com/wx6025c5470c3cb50c/97/page-frame.html',
                               'accept-encoding': 'br,gzip,deflate'}
            else:
                url = self.url + "/user/brandhouse/window/getProducts"
                body = {'windowId': windowid, 'areaId': self.store_info.get("areaId"),
                        'storeId': self.store_info.get("storeId"),
                        'excludeAct': 'N',
                        'pageIndex': '1', 'pageSize': '10'}
                headers = {':method': 'POST', ':scheme': 'https', ':path': '/user/brandhouse/window/getProducts',
                           ':authority': 'mall.xsyxsc.com', 'accept': 'application/json,text/plain,*/*',
                           'content-type': 'application/x-www-form-urlencoded', 'content-length': '126',
                           'accept-language': 'zh-cn',
                           'user-agent': 'Mozilla/5.0(iPhone;CPUiPhoneOS11_4likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Mobile/15F79MicroMessenger/7.0.8(0x17000820)NetType/4GLanguage/zh_CN',
                           'referer': 'https://servicewechat.com/wx6025c5470c3cb50c/97/page-frame.html',
                           'accept-encoding': 'br,gzip,deflate'}

            body.update(self.base_param)
            if windowtype == "BRAND_HOUSE":
                pass
                for pageIndex in range(1, 10000):
                    body.update({'pageIndex': pageIndex})
                    resp = SESSION.post(url=url, data=body, verify=False, headers=headers).json().get("data")
                    if resp.get("records") is None:
                        del url, body
                        break
                    self.sku_append_by_list(windos_name=kwargs.get(id_type), sku_info=resp.get("records"))
            else:
                resp = SESSION.post(url=url, data=body, headers=headers, verify=False).json()
                self.sku_append_by_list(windos_name=kwargs.get(id_type), sku_info=resp.get("data"))
            myprint("累计搜索到{}个商品.".format(len(self.sku_info_list)))

    def sku_append_by_list(self, windos_name, sku_info):
        """追加商品到sku列表中

        :param windos_name: 名称
        :param sku_info: 返回响应数据
        """
        sku = {}
        for com_info in sku_info:
            if com_info.get("prName").strip() not in self.sku_name.keys():
                self.sku_name[com_info.get("prName")] = ""  # 用于去重
                sku["prName"] = com_info.get("prName").strip()  # 名称
                sku["saleAmt"] = com_info.get("saleAmt")  # 价格
                sku["marketAmt"] = com_info.get("marketAmt")  # 原价
                sku["tmBuyStart"] = com_info.get("tmBuyStart")  # 开始购买时间
                sku["tmBuyEnd"] = com_info.get("tmBuyEnd")  # 结束购买时间
                sku["ulimitQty"] = com_info.get("ulimitQty")  # 单人限购
                sku["limitQty"] = com_info.get("limitQty")  # 限量
                sku["shelfLife"] = com_info.get("shelfLife")  # 保质期
                sku["prId"] = com_info.get("prId")  # 产品id用于下单 对应提交订单接口itemList.pi字段
                sku["acId"] = com_info.get("acId")  # 活动id用于下单 对应提交订单接口itemList.pai字段
                sku["sku"] = com_info.get("sku")  # sku 用于下单 对应提交订单接口itemList.sku字段
                sku["prType"] = com_info.get("prType")  # prType用于下单 对应提交订单接口itemList.prType字段
                sku["windos_name"] = windos_name  # 标题名称
                if "秒杀" in windos_name:
                    myprint("活动标题'{}'下找到商品'{}'".format(windos_name, sku.get("prName")))
                self.sku_info_list.append(sku)
                sku = {}
            else:
                if "秒杀" in windos_name:
                    myprint(
                        "活动标题'{}'下找到商品'{} 此商品已经存在 直接过滤'".format(windos_name, com_info.get("prName")))

    def to_excel_data(self):
        """将sku信息写入excel

        """
        windos_name = []
        sku_name = []
        sku_price = []
        sku_raw_price = []
        sku_buy_start = []
        sku_buy_end = []
        sku_prid = []
        sku_acid = []
        sku_sku = []
        sku_prtype = []
        sku_excel_dict = {}

        for sku in self.sku_info_list:
            windos_name.append(sku.get("windos_name"))
            sku_name.append(sku.get("prName"))
            sku_price.append(sku.get("saleAmt"))
            sku_raw_price.append(sku.get("marketAmt"))
            sku_buy_start.append(sku.get("tmBuyStart"))
            sku_buy_end.append(sku.get("tmBuyEnd"))
            sku_prid.append(sku.get("prId"))
            sku_acid.append(sku.get("acId"))
            sku_sku.append(sku.get("sku"))
            sku_prtype.append(sku.get("prType"))
        sku_excel_dict["标题名称"] = windos_name
        sku_excel_dict["商品名称"] = sku_name
        sku_excel_dict["目前售价"] = sku_price
        sku_excel_dict["原始价格"] = sku_raw_price
        sku_excel_dict["开始购买时间"] = sku_buy_start
        sku_excel_dict["结束购买时间"] = sku_buy_end
        sku_excel_dict["产品id(itemList.pi)"] = sku_prid
        sku_excel_dict["活动id(itemList.pai)"] = sku_acid
        sku_excel_dict["sku编号(itemList.sku)"] = sku_sku
        sku_excel_dict["prType(itemList.prType)"] = sku_prtype
        file_path = r'兴盛优选商品数据_%s.xlsx' % (time.strftime('%Y-%m-%d', time.localtime(time.time())))
        writer = pd.ExcelWriter(file_path)
        df = pd.DataFrame(sku_excel_dict)
        df.to_excel(writer, columns=sku_excel_dict.keys(), index=False, encoding='utf-8',
                    sheet_name='兴盛优选商品数据')
        writer.save()
        myprint("写入excel成功 写入路径为{}".format(os.getcwd() + r"/" + file_path))


class Order(object):
    def __init__(self, username, user_key, store_info, wechat_info, all_sku_list, listname, sleep_time):
        self.userkey = user_key
        self.sleep_time = sleep_time
        self.user = username
        self.base_param = {'userKey': self.userkey}
        self.store_info = store_info
        self.wechat_info = wechat_info
        self.all_sku_list = all_sku_list
        self.listname = listname
        self.header = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/7.0.4(0x17000428) NetType/WIFI Language/zh_CN'}
        self.url = "https://trade.xsyxsc.com"
        self.create_order_by_listname(listname)

    def create_order_by_listname(self, listname):
        """创建订单，通过商品名称列表

        :param listname:
        """
        itemlist = self.listname_to_itemlist(listname)
        if len(itemlist) >= 1:
            self.save_order_by_order_itemlist(itemlist, listname)
        else:
            myprint("您输入的商品{}在系统库中均没找到！".format(listname))

    def listname_to_itemlist(self, listname):
        itemlist = []
        for to_buy_sku_name in listname:
            item_info_dict = self.get_order_oneitemdict_by_sku_name(to_buy_sku_name)
            if item_info_dict is None:
                myprint("'{}' 在兴盛优选商品库中找不到此商品！".format(to_buy_sku_name))
            else:
                "逐次将商品itemlist添加到self.itemlist中"
                itemlist.append(item_info_dict)
        return itemlist

    def get_order_oneitemdict_by_sku_name(self, name):
        """根据商品名称，获取商品到itemlist信息（单个）--支持模糊匹配

        :param name:
        :return:
        """
        for sku in self.all_sku_list:
            if sku.get("prName") == name or name in sku.get("prName"):
                myprint(
                    "'{}' 明细参数为acId:'{}'  sku:'{}' prId:'{}  prType:'{}''".format(name, sku.get("acId"),
                                                                                  sku.get("sku"),
                                                                                  sku.get("prId"),
                                                                                  sku.get("prType")))
                return {"pai": sku.get("acId"),
                        "q": 1,
                        "sku": sku.get("sku"),
                        "pi": sku.get("prId"),
                        "pt": sku.get("prType")}
            else:
                pass
        return None

    def save_order_by_order_itemlist(self, itemlist, listname):
        """创建订单，通过 itemlist

        :param itemlist: 用于提交订单
        :param listname: 用于日志输出
        """
        url = self.url + "/tradeorder/order/create"
        """itemList说明： 
        q为数量 
        pt为类型(BRAND_HOUSE CHOICE)
        pai 为活动id  activityId
        pi为产品id  productId 
        sku为sku编号 """
        order_info = {"r": self.wechat_info.get("wechatNickName"),
                      "p": self.wechat_info.get("mobileNo"),
                      "si": self.wechat_info.get("currentStoreId"),  # 自提点ID
                      "iv": 0,
                      "re": "",
                      "sna": str(self.store_info.get("storeName")) + "店",
                      "sn": self.store_info.get("storeCode"),
                      "sad": self.store_info.get("detailAddress"),
                      "st": self.store_info.get("contactsTel"),
                      "ai": self.store_info.get("areaId"),
                      "an": self.store_info.get("areaName"),
                      "ui": self.wechat_info.get("userId"),
                      "un": self.wechat_info.get("mobileNo"),
                      "oo": "",
                      "a": self.store_info.get("detailAddress"),
                      "whi": self.store_info.get("warehouseId"),
                      "whn": self.store_info.get("warehouseName"),
                      "wi": self.wechat_info.get("wechatImage"),
                      "wn": self.wechat_info.get("wechatNickName"),
                      "ot": "CHOICE",
                      "ct": 'MINI_PROGRAM',  # 更改会提示客户来源不正确
                      "li": self.store_info.get("lineId"),
                      "lin": self.store_info.get("lineName"),
                      "lins": "",
                      "itemList": itemlist}
        body = {'order': json.dumps(order_info)}
        headers = {':method': 'POST', ':scheme': 'https', ':path': '/tradeorder/order/create',
                   ':authority': 'trade.xsyxsc.com', 'accept': 'application/json,text/plain,*/*',
                   'content-type': 'application/x-www-form-urlencoded', 'content-length': '1720',
                   'accept-language': 'zh-cn',
                   'user-agent': 'Mozilla/5.0(iPhone;CPUiPhoneOS11_4likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Mobile/15F79MicroMessenger/7.0.8(0x17000820)NetType/4GLanguage/zh_CN',
                   'referer': 'https://servicewechat.com/wx6025c5470c3cb50c/97/page-frame.html',
                   'accept-encoding': 'br,gzip,deflate'}
        body.update(self.base_param)
        """等待到秒杀时间 在提交创建订单接口"""
        myprint("用户:'{}'  秒杀商品:'{}' 已经准备好！ 延迟时间为{}".format(self.user, listname, self.sleep_time))
        wait_time(user=self.user, store_info=self.store_info)
        time.sleep(float(self.sleep_time))
        resp = SESSION.post(url=url, data=body, verify=False, headers=headers).json()
        if resp.get("rspCode") == "success":
            myprint("账号:'{}' 创建订单成功！，订单号为{}，购买的商品为{}".format(self.user, resp.get("data").get("orderId"), listname))
            exit()
        else:
            myprint("账号:'{}' 创建订单失败！！，错误信息为{}  错误码为{}".format(self.user, resp.get("rspDesc"), resp.get("rspCode")))
            time.sleep(2)
            exit()
            self.save_order_by_order_itemlist(itemlist, listname)
            # myprint("本次请求参数为{}".format(order_info))
            # time.sleep(float(self.sleep_time) * 1.5)
            # self.save_order_by_order_itemlist(itemlist, listname)


def main():
    # 批量设置用户，对应购买的商品，默认秒杀时间=当天的早上十点--所有用户必须是湖南区域，如果不是 需要在每个线程去获取真实的秒杀时间
    user_dict = {
        '蒋宗涛&0.7': [''],
        '陆文博&0.7': [''],
        # '陆文博小号&0.8': ['烽味 古铜方形宫廷酒精炉 1个 19X19X9cm','旺迪 家庭胶带特惠装 1盒 胶带14卷十剪刀1把','布艺工坊 韩版可爱防污袖套 2双/份 33X18cm 颜色随机','客家谣 4.6英寸直口碗 4个/份 直径约11.8cm 高5.8cm'],
        # '朱勇&0.9': ['烽味 古铜方形宫廷酒精炉 1个 19X19X9cm','旺迪 家庭胶带特惠装 1盒 胶带14卷十剪刀1把','布艺工坊 韩版可爱防污袖套 2双/份 33X18cm 颜色随机','客家谣 4.6英寸直口碗 4个/份 直径约11.8cm 高5.8cm']
        # '罗峥&0.71': ["Apple ipad 1台 金色 128G WIFI版"],
        # '铭哥&0.72': ["Apple ipad 1台 金色 128G WIFI版"],
        # '麦子&0.725': ["Apple ipad 1台 金色 128G WIFI版"],
        # '彭敏&1': ["浔江月 蜂蜜米露 430ml/瓶 新老包装随机"],
        # '谢江鹏小号&1.2': ["比趣 家居保暖拖鞋 1双 38至45码随机 颜色随机"]
        # '陆文博&0': ["云南菜业", "邓叔叔的白沙豆腐", "大渔印象"],
        # '易磊&0': ["云南菜业", "邓叔叔的白沙豆腐", "大渔印象"],

    }
    workqueue = Queue.Queue(len(user_dict))
    thread_num = len(user_dict)  # 线程数等于用户数
    thread_name_list = [str(i) + str(j) for i, j in zip(["线程"] * thread_num, list(range(1, thread_num + 1)))]
    threads = []
    # 将用户和需要购买的商品填充到队列，同时创建线程
    for user, sku_name in user_dict.items():
        workqueue.put([user.split("&")[0], user.split("&")[1], sku_name])

    for threadname in thread_name_list:
        thread = MyTread(threadname, workqueue)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
