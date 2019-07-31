#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: Hyatt.py


import os
import threading

from HyattHotel import HyattHotel, hotels
from config import data_dir


class Hyatt(HyattHotel):
    def __init__(self):
        self.downloading = []
        self.futures = []
        self.hotels = hotels
        self.check_dir()
        self.__start()
    def check_dir(self):
        # 检查目录
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    def get_date(self, date):
        if date in self.ready():
            try:
                data = self.load_price(date)
                return data
            except:
                self.downloading.append(date)
                return date
        elif date not in self.downloading:
            self.downloading.append(date)
            return date
    def ready(self):
        li = os.listdir(data_dir)
        return li
    def get_date_json(self, date):
        hotels = load_json(date)
        return hotels
    def __start(self):
        t = threading.Thread(target=self.start)
        t.start()
    def start(self):
        while self.downloading != False:
            if len(self.downloading) > 0:
                date = self.downloading[0]
                self.update_price(date)
    def status(self):
        if len(self.downloading) > 0:
            downloading = self.downloading[0]
            percentage = self.Percentage()
            ready = self.ready()
            ready.remove(downloading)
            pending = self.downloading[1:]
        else:
            downloading = None
            percentage = None
            ready = self.ready()
            pending = self.downloading
        d = {'Downloading': downloading, 
             'Percentage': percentage,
             'Ready': ready,
             'Pending': pending}
        return d






if __name__ == '__main__':
    import code as cc
    cc.interact(banner="", local=locals())
