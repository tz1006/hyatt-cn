#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: HyattHotel.py


from datetime import datetime
from pytz import timezone
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

#from HyattCode import hotels
from HyattPrice import get_hotel_price
from HyattTool import Hotel
from config import max_workers


class HyattHotel():
    def __init__(self):
        self.hotels = hotels
        self.futures = []
    def update_date(self, date):
        # 验证日期
        ddate = datetime.strptime(date, '%Y-%m-%d')
        today = datetime.now(timezone('Asia/Shanghai')).date()
        if (today - ddate) > 0:
            raise BaseException
        # Pending
        pending = []
        for i in self.hotels:
            try:
                hotel = Hotel(i)
                hotel.load(date)
            except:
                pending.append(i)
        # download
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for i in pending:
                self.futures.append(executor.submit(get_hotel_price, i, date))
            kwargs = {'total': len(self.futures)}
            for f in tqdm(as_completed(self.futures), **kwargs):
                pass
    def Percentage(self):
        count = 0
        total = len(self.futures)
        if total == 0:
            return None
        for i in self.futures:
            if i.done() == True:
                count += 1
        percentage = round((count / total), 4)
        return percentage
    def load_date(self, date):
        d = []
        for i in self.hotels:
            hotel = Hotel(i)
            dd = hotel.load(date)
            d.append(dd)
        d = d.sort(key=lambda item:item[1]['Name'])
        return d



