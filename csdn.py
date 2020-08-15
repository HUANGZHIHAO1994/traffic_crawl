import requests
import time
import random


# from playsound import playsound

PROXY_URL = 'https://blog.csdn.net/Kevin_HZH/article/details/91043392'
PROXY_URL1 = 'https://blog.csdn.net/Kevin_HZH/article/details/82781934'
PROXY_URL2 = 'https://blog.csdn.net/Kevin_HZH/article/details/88850134'
PROXY_URL3 = 'https://blog.csdn.net/Kevin_HZH/article/details/88863967'
PROXY_URL4 = 'https://blog.csdn.net/Kevin_HZH/article/details/81876527'

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

count = 0
while True:
    try:
        count += 1
        print("搞到第{}次".format(count))
        headers = {}
        headers['User-Agent'] = random.choice(USER_AGENTS)
        response = requests.get(PROXY_URL, headers=headers)
        headers['User-Agent'] = random.choice(USER_AGENTS)
        response = requests.get(PROXY_URL1, headers=headers)
        headers['User-Agent'] = random.choice(USER_AGENTS)
        response = requests.get(PROXY_URL2, headers=headers)
        headers['User-Agent'] = random.choice(USER_AGENTS)
        response = requests.get(PROXY_URL3, headers=headers)
        headers['User-Agent'] = random.choice(USER_AGENTS)
        response = requests.get(PROXY_URL4, headers=headers)
    except Exception as e:
        print(e)
        continue
#         playsound('xiyouji.mp3')

    time.sleep(62)
