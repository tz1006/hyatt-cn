#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: HyattTool.py


import os
import json
from urllib.parse import urlencode
from datetime import datetime, timedelta

from config import data_dir


class Hotel():
    def __init__(self, hotelcode):
        self.code = hotelcode
        self.name = hotels[hotelcode]['name']
        self.brand = hotel_brand(self.name)
    def save(self, d):
        date = d['Date']
        save_json(self.code, date d)
    def load(self, date):
        load_json(self.code, date)
    def url(self, date, CUP):
        url = hotelcode2url(self.code, date, CUP)
        return url


def hotel_brand(name):
    brand = '未知'
    if '柏悦' in name:
        brand = '柏悦'
    elif '君悦' in name:
        brand = '君悦'
    elif '嘉轩' in name:
        brand = '凯悦嘉轩'
    elif '嘉寓' in name:
        brand = '凯悦嘉公寓'
    elif '凯悦酒店' in name:
        brand = '凯悦'
    elif '素凯泰' in name:
        brand = 'SLH'
    return brand


def hotelcode2url(hotelcode, date, CUP):
    if CUP:
        offercode = 'CUP19'
        checkoutdate = datechange(date, 3)
    else:
        offercode = ''
        checkoutdate = datechange(date, 1)
    # url
    url = 'https://www.hyatt.com/zh-CN/shop/rates/%s?' % hotel_code
    payload = {'rooms': 1,
               'adults': 1,
               'checkinDate': date,
               'checkoutDate': checkoutdate,
               'kids': 0,
               'offercode': offercode,
               'rateFilter': 'standard'}
    url += urlencode(payload)
    return url

def datechange(date, change):
    change = int(change)
    date = datetime.strptime(date, '%Y-%m-%d').date()
    new_date = date + timedelta(days=change)
    new_date_string = new_date.strftime('%Y-%m-%d')
    return new_date_string


def save_json(hotelcode, date, d):
    # 检查目录
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    dir_path = '%s/%s' % (data_dir, date)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # 保存JSON
    path = '%s/%s.json' % (dir_path, hotelcode)
    with open(path, 'w'), as f:
        content = json.dumps(d)
        f.write(content)
    print('保存', path)


def load_json(hotelcode, date):
    # 检查目录
    path = '%s/%s/%s.json' % (data_dir, date, hotelcode)
    if not os.path.exists(path):
        raise FileNotFoundError
    else:
        # 载入JSON
        with open(path, 'r') as f:
            content = f.read()
            d = json.loads(content)
        return d

