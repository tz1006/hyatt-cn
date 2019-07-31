#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: HyattPrice.py


from random import choice
from bs4 import BeautifulSoup

from webloader import webloader
from HyattTool import Hotel
from config import proxy


def get_hotel_price(hotelcode, date):
    hotel = Hotel(hotelcode)
    # NON-CUP Price
    url1 = hotel.url(date, CUP=False)
    webloader1 = webloader(headless=False, image=False)
    if proxy != None:
        p = choice(proxy)
        webloader1.set_proxy(*p)
    html1 = webloader1.get_page(url1, 20)
    price1, currency = extract_price(html1)
    #print('一般价格', price1, currency)
    # CUP Price
    url2 = hotel.url(date, CUP=True)
    webloader2 = webloader(headless=False, image=False)
    if proxy != None:
        p = choice(proxy)
        webloader2.set_proxy(*p)
    html2 = webloader2.get_page(url2, 20)
    price2, currency2 = extract_price(html2)
    #print('CUP价格', price2, currency2)
    if type(price1) == type(1):
        price = int(price1 * 1.16)
    else:
        price = '-'
    if type(price2) == type(1):
        CUP_price = int(price2 * 1.16)
        Total_CUP_price = CUP_price * 3
    else:
        CUP_price = '-'
        Total_CUP_price = '-'
    if type(price1) == type(price2) == type(1):
        discount = round(CUP_price/price, 2)
    else:
        discount = '-'
    if currency == None:
        currency = '-'
    d = {'Code': code,
         'Date': date,
         'Name': hotel.name,
         'Brand': hotel.brand
         'Price': price,
         'Price_CUP': CUP_price,
         'Price_CUP_total': Total_CUP_price,
         'Currency': currency,
         'Discount': discount
             }
    return d



def extract_price(html):
    if len(html) == 4:
        print(html)
        price = None
        currency = None
    else:
        soup = BeautifulSoup(html, "html.parser")
        #alert = soup.selector('div.m-booking-alert')
        alert = soup.find_all('div', attrs={'class':'m-booking-alert'})
        # 不参加CUP
        if len(alert) == 1:
            price = None
            currency = None
        else:
            try:
                price_soup = soup.find_all('div', attrs={'class':'b-text_weight-bold rate-pricing'})[0]
                price = int(price_soup.span.get('data-price'))
                currency = price_soup.find_all('span')[1].text
            except:
                price = None
                currency = None
    return price, currency

