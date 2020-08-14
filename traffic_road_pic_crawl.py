'''
上海各路段交通图片抓取
抓取网站https://shanghaicity.openservice.kankanews.com/public/road/timing
先运行pre_traffic_road.py得到txt文件
'''

import requests
from lxml import etree
import random
import time
import json
import re
import threading
import os
import urllib.request

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; Avant Browser; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
    'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0'
]


# name = {}
# name["1"] = "地面道路"
# name["2"] = "快速道路"
# name["3"] = "高速道路"
# name["4"] = "城际高速"


class Traffic:
    '''
    全部道路的图片抓取
    调用类的时候把名字输入进去：如：
    "地面道路"
    "快速道路"
    "高速道路"
    "城际高速"
    '''

    base = "data:image/png;base64,"
    url = "https://shanghaicity.openservice.kankanews.com/public/road/getnowpic/picid/"

    def __init__(self, name):
        self.name = name

    def road1(self):
        '''
        地面道路
        '''
        f = open("{}.txt".format(self.name), encoding='utf-8')
        roads = eval(f.read().encode('utf8').decode('unicode_escape'))
        f.close()
        for road in roads:
            t = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print(t)
            t = t.replace(" ", "-").replace(":", "-")
            url1 = Traffic.url + road["picid"]
            print(url1)
            # 测试下来虽然项目多，但速度可以，多线程看情况使用
            # thr = threading.Thread(target=pictures, args=(url1, road["road0"], road["road1"], t))
            # thr.setDaemon(False)
            # thr.start()
            self.pictures(url1, road["road0"], road["road1"], t)

    def pictures(self, url, road0, road1, time):
        headers = {}
        headers['User-Agent'] = random.choice(USER_AGENTS)
        response = requests.get(url, headers=headers, timeout=2000)
        # print(response.text)
        try:
            text = json.loads(response.text)
            url_picture = Traffic.base + text["data"]["0"]
        except Exception as e:
            print(e)
            return
        # print(url_picture)

        headers = {}
        headers['User-Agent'] = random.choice(USER_AGENTS)
        data = urllib.request.Request(url_picture, headers=headers)
        resp = urllib.request.urlopen(data)
        data = resp.read()
        path = os.path.join(os.path.dirname(__file__), 'total')
        if not os.path.exists(path):
            os.mkdir(path)
        picpath = os.path.join(path, self.name)
        if not os.path.exists(picpath):
            os.mkdir(picpath)
        f = open(picpath + "\\" + road0 + "-" + road1 + time + ".png", "wb")
        f.write(data)
        f.close()


if __name__ == '__main__':
    tra = Traffic("高速道路")
    tra.road1()
    '''
    tra = Traffic("地面道路")
    tra.road1()
    tra = Traffic("城际道路")
    tra.road1()
    tra = Traffic("快速道路")
    tra.road1()
    '''
