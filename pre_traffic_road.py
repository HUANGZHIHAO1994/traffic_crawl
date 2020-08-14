'''
这个文件主要是生成要爬取的列表，除非道路更新，否则直接用total.py即可
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


urls = ["https://shanghaicity.openservice.kankanews.com/public/road/getear/name/%E5%9C%B0%E9%9D%A2%E9%81%93%E8%B7%AF", "https://shanghaicity.openservice.kankanews.com/public/road/getear/name/%E5%BF%AB%E9%80%9F%E9%81%93%E8%B7%AF", "https://shanghaicity.openservice.kankanews.com/public/road/getear/name/%E9%AB%98%E9%80%9F%E9%81%93%E8%B7%AF", "https://shanghaicity.openservice.kankanews.com/public/road/getear/name/%E5%9F%8E%E9%99%85%E9%AB%98%E9%80%9F"]

name = {}
name["1"] = "地面道路"
name["2"] = "快速道路"
name["3"] = "高速道路"
name["4"] = "城际高速"


def total_name(url, count):
    headers = {}
    headers['User-Agent'] = random.choice(USER_AGENTS)
    response = requests.get(url, headers=headers, timeout=2000)
    text = json.loads(response.text.encode('utf8').decode('unicode_escape'))
    print(text)
    t = json.dumps(text)
    f = open(name[str(count)] + ".txt", "w", encoding="utf-8")
    f.write(t)
    f.close()


if __name__ == '__main__':

    count = 0
    for url in urls:
        count += 1
        total_name(url, count)


