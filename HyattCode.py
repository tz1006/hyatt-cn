#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: HyattCode.py


import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

from config import temp_dir


ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
header = {'User-Agent': ua,
          'accept-language': 'zh-CN,zh;q=0.9'}



def get_cn_hotels():
    # 生成url
    url = 'https://www.hyatt.com/zh-CN/explore-hotels/partial?'
    payload = {'regionGroup': '5-Asia',
               'categories': '',
               'brands': ''}
    url += urlencode(payload)
    #headers = {Accept-Language': en,zh-CN}
    #print(url)
    # soup
    with requests.session() as s:
        r = s.get(url, headers=header)
    html = r.content
    soup = BeautifulSoup(html, "html.parser")
    cn_soup = soup.find_all('li', attrs={'data-js-country':'大中华地区'})[0]
    cn_hotels = cn_soup.find_all('li', attrs={'class':'property b-mb2'})
    hotel_list = []
    for i in cn_hotels:
        name = i.a.text
        code = i.get('data-js-property')
        link = i.a.get('href')
        span = i.a.span
        if span == None:
            tag = ''
        else:
            tag = span.text
        d = {'name': name,
             'code': code,
             'link': link,
             'tag': tag}
        hotel_list.append(d)
    return hotel_list



class HyattCode():
    def __init__(self):
        pass
    def get(self):
        try:
            d = self.load()
            return d
        except:
            d = self.download()
            return d
    def load(self):
        path = '%s/hotelcode.json' % temp_dir
        if not os.path.exists(path):
            raise FileNotFoundError
        else:
            # 载入JSON
            with open(path, 'r') as f:
                content = f.read()
                d = json.loads(content)
            return d
    def download(self):
        # 检查目录
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        hotels = get_cn_hotels()
        # 保存JSON
        path = '%s/hotelcode.json' % temp_dir
        with open(path, 'w') as f:
            content = json.dumps(hotels)
            f.write(content)
        print('HyattCode保存', path)
        return hotels



hyattcode = HyattCode()
hotels = hyattcode.get()


if __name__ == '__main__':
    import code as cc
    cc.interact(banner="", local=locals())
