# -*- coding: utf-8 -*-
'''
上海旅游景点客流量爬虫
这个要用到selenium和chromedriver，下载驱动用这个网址：
https://sites.google.com/a/chromium.org/chromedriver/downloads
注意驱动版本和chrome版本对应
chrome版本查询：
打开chrome浏览器， chrome://version
爬取网站：https://shanghaicity.openservice.kankanews.com/public/tour/
给了mysql和mongo两种数据库插入版本
'''

import requests
from lxml import etree
import random
import time
import pymongo
from pymongo.errors import DuplicateKeyError
import logging  # 引入logging模块
import json
import re
import os
import threading
import urllib.request

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy.http.response.html import HtmlResponse
from selenium.webdriver.chrome.options import Options

import pymysql
from pymysql import cursors

'''
样本：
{'CODE': '2', 'NAME': '上海野生动物园', 'TIME': '2019-07-21 15:45:00', 'R_TIME': '2019\\/7\\/21 15:44:55', 'NUM': '7318', 'SSD': '舒适', 'DES': '', 'START_TIME': '08:00', 'END_TIME': '18:00', 'INFO': '上海野生动物园是集野生动物饲养、展览、繁育保护、科普教育与休闲娱乐为一体的主题公园。景区于1995年11月18日正式对外开放，地处上海浦东新区，占地153公顷（约2300亩），是首批国家5A级旅游景区。     园区居住着大熊猫、金丝猴、金毛羚牛、朱鹮、长颈鹿、斑马、羚羊、白犀牛、猎豹等来自国内外的珍稀野生动物200余种，上万余只。园区分为车入区和步行区两大参观区域。     步行区，让您在寓教于乐中进一步了解动物朋友。不仅可以观赏到大熊猫、非洲象、亚洲象、长颈鹿、黑猩猩、长臂猿、狐猴、火烈鸟、朱鹮等众多珍稀野生动物，更有诸多特色的动物行为展示和互动体验呈现。     车入区为动物散放养展示形式，保持着 “人在‘笼’中，动物自由”的展览模式，给动物更多的自由空间。使您身临其境的感受一群群斑马、羚羊、角马、犀牛等食草动物簇拥在一起悠闲觅食；又能领略猎豹、东北虎、非洲狮、熊、狼等大型猛兽“部落”展现野性雄姿。     另外，园内还设有5座功能各异的表演场馆。身怀绝技的俄罗斯专业团队携各路动物明星演艺“魔幻之旅”；猎豹、格力犬、蒙 联系电话：021-58036000', 'MAX_NUM': '60000', 'IMAGE': '图片111111_20160302080923201.png', 'TYPE': '正常', 'T_CODE': '5', 'INITIAL': 'SHYSDWY', 'RANK': '5A', 'COUNTY': '浦东新区', 'LOCATION_X': 121.723586, 'LOCATION_Y': 31.05928, 'SWITCH': 1, 'WEATHER_INFO': 1, 'WEATHER_DES': '多云', 'WEATHER_HIGH': '33', 'WEATHER_LOW': '26', 'WEATHER_DIRECTION': '东南风', 'WEATHER_POWER': '3-4级'}
'''

# MongoDb 配置

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'Traffic'

#  mongo数据库的Host, collection设置
client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
collection = client[DB_NAME]["Attractions"]

'''
# SQL 配置
dbparams = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1234',
    # 'database': 'traffic',
    'charset': 'utf8'
}
conn = pymysql.connect(**dbparams)
cursor = conn.cursor()
try:
    sql2 = "CREATE DATABASE IF NOT EXISTS traffic"
    # 执行创建数据库的sql
    cursor.execute(sql2)
except:
    pass

dbparams = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1234',
    'database': 'traffic',
    'charset': 'utf8'
}
conn = pymysql.connect(**dbparams)
cursor = conn.cursor()
try:
    sql = """CREATE TABLE Attraction(
              id varchar(255),
              code varchar(255),
              name_ varchar(255),
              time_ varchar(255),
              real_time varchar(255),
              num varchar(255),
              max_num varchar(255),
              ssd varchar(255),
              start_time varchar(255),
              end_time varchar(255),
              rank varchar(255),
              county varchar(255),
              loc_x varchar(255),
              loc_y varchar(255),
              weather_info varchar(255),
              weather_des varchar(255),
              weather_high varchar(255),
              weather_low varchar(255),
              weather_dir varchar(255),
              weather_pow varchar(255))DEFAULT CHARSET=utf8"""

    cursor.execute(sql)
except Exception as e:
    print(e)
'''

#  随机请求头设置
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

url = 'https://shanghaicity.openservice.kankanews.com/public/tour/filterinfo2'


def attrct():
    headers = {}
    headers['User-Agent'] = random.choice(USER_AGENTS)
    chrome_options = Options()
    headers = random.choice(USER_AGENTS)
    chrome_options.add_argument('--user-agent={}'.format(headers))  # 设置请求头的User-Agent
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    tree_node = etree.HTML(driver.page_source)

    #     tree_node = etree.HTML(driver.page_source.encode('utf8').decode('unicode_escape'))
    #     print(driver.page_source.encode('utf8').decode('unicode_escape'))
    #     print(driver.page_source)
    #     tree_node = etree.HTML(driver.page_source)

    for i in eval(tree_node.xpath("//pre//text()")[0]):
        code = i["CODE"]
        name = str(i["NAME"])
        # print(name)
        time_ = i["TIME"]
        real_time = i["R_TIME"].replace("\\", "").replace("/", "-")
        num = i["NUM"]
        max_num = i["MAX_NUM"]
        ssd = i["SSD"]
        start_time = i["START_TIME"]
        end_time = i["END_TIME"]
        type_ = i["TYPE"]
        rank = i["RANK"]
        county = i["COUNTY"]
        loc_x = str(i["LOCATION_X"])
        loc_y = str(i["LOCATION_Y"])

        weather_info = str(i["WEATHER_INFO"])
        weather_des = i["WEATHER_DES"]
        weather_high = i["WEATHER_HIGH"]
        weather_low = i["WEATHER_LOW"]
        weather_dir = i["WEATHER_DIRECTION"]
        weather_pow = i["WEATHER_POWER"]
        id = code + "-" + time_.replace(" ", '-').replace(":", '-')

        dict_attrct = {"_id": id, "code": code, "name": name,
                       "time": time_, "real_time": real_time, "num": num, "max_num": max_num, "ssd": ssd,
                       "start_time": start_time, "end_time": end_time, "type": type_, "rank": rank, "county": county,
                       "loc_x": loc_x, "loc_y": loc_y, "weather_info": weather_info, "weather_des": weather_des,
                       "weather_high": weather_high, "weather_low": weather_low, "weather_dir": weather_dir,
                       "weather_pow": weather_pow}
        logger.info(str(dict_attrct))
        try:
            collection.insert_one(dict_attrct)
        except DuplicateKeyError as e:
            pass
    driver.close()


'''
        try:
            cursor.execute("""INSERT INTO Attraction (id,code,name_,time_,real_time,num,max_num,ssd,start_time,end_time,rank,county,loc_x,loc_y,weather_info,weather_des,weather_high,weather_low,weather_dir,weather_pow) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(id, code, name, time_, real_time, num, max_num, ssd, start_time, end_time, rank, county, loc_x, loc_y, weather_info, weather_des, weather_high, weather_low, weather_dir, weather_pow))

            conn.commit()
        except Exception as e:
            print(e)


'''

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关
    # 第二步，创建一个handler，用于写入日志文件
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))

    log_path = os.path.join(os.getcwd(), 'Logs')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file = os.path.join(log_path, rq + 'Attractions.log')

    fh = logging.handlers.RotatingFileHandler(log_file, mode='a', maxBytes=1024, backupCount=5)

    #     fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

    #     st = logging.StreamHandler()
    #     st.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

    fh.setFormatter(formatter)
    #     st.setFormatter(formatter)

    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)
    #     logger.addHandler(st)

    t = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logger.info(t)
    attrct()
