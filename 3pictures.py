'''
爬取三张图：
城市快速路概览图102_0250_L : 1
高速公路概览图101_0250_L : 2
长三角城际高速概览100_1001_L : 3
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
# print(os.path.dirname(__file__))

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

base = "data:image/png;base64,"
'''
城市快速路概览图102_0250_L : 1
高速公路概览图101_0250_L : 2
长三角城际高速概览100_1001_L : 3
'''
urls = ["https://shanghaicity.openservice.kankanews.com/public/road/getnowpic/picid/102_0250_L", "https://shanghaicity.openservice.kankanews.com/public/road/getnowpic/picid/101_0250_L", "https://shanghaicity.openservice.kankanews.com/public/road/getnowpic/picid/100_1001_L"]

name = {}
name["102_0250_L"] = "1"
name["101_0250_L"] = "2"
name["100_1001_L"] = "3"
# path = "P3"

def pictures3(url, time):
    headers = {}
    headers['User-Agent'] = random.choice(USER_AGENTS)
    response = requests.get(url, headers=headers, timeout=2000)
    text = json.loads(response.text)
    url_picture = base + text["data"]["0"]
    # print(url_picture)
    # 就三张图不写存图片的线程了
    headers = {}
    headers['User-Agent'] = random.choice(USER_AGENTS)
    data = urllib.request.Request(url_picture, headers=headers)
    resp = urllib.request.urlopen(data)
    data = resp.read()
    path = os.path.join(os.path.dirname(__file__), 'P3')
    if not os.path.exists(path):
        os.mkdir(path)
    picpath = os.path.join(path, name[url.split('/')[-1]])
    if not os.path.exists(picpath):
        os.mkdir(picpath)
    f = open(picpath + "\\" + name[url.split('/')[-1]] + "-" + time + ".png", "wb")
    f.write(data)
    f.close()


if __name__ == '__main__':

    while True:
        t = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(t)
        t = t.replace(" ", "-").replace(":", "-")
        for url in urls:
            pictures3(url, t)
        # 六分钟开启一次
        time.sleep(360)



