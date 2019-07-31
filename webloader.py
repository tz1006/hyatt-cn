#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: webloader.py
# useage: webloader = webloader(debug=False, image=False)
#         webloader.set_proxy('127.0.0.1',1080)
#         webloader.get_page(url)


import time

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class webloader():
    def __init__(self, headless=False, image=False, debug=False):
        self.proxy = None
        self.headless = headless
        self.image = image
        self.debug = debug
    def set_option(self):
        self.option = ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.option.add_argument('--no-sandbox')
        self.option.add_argument('--disable-dev-shm-usage')
        #self.option.add_argument(‘lang=zh_CN.UTF-8‘)
        self.option.add_argument('--window-size=500,300') #指定浏览器分辨率
        #self.option.add_argument('--disable-extensions')
        #self.option.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
        #self.option.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
        if not self.image:
            self.option.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
        if self.headless:
            self.option.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        if self.proxy != None:
            self.option.add_argument('--proxy-server=http://%s:%d' % self.proxy)
    def set_proxy(self, ip, port):
        self.proxy = (ip, port)
    def init_chrome(self):
        self.set_option()
        self.driver = Chrome(options=self.option)
        self.driver.set_page_load_timeout(self.timeout)
        #self.driver.minimize_window()
    def get_page(self, url, timeout=30):
        self.timeout = timeout
        self.init_chrome()
        #print(url)
        try:
            html = '连接错误'
            start_time = time.time()
            try:
                self.driver.get(url)
            except:
                self.driver.get(url)
            html = '页面打开'
            self.wait()
            html = '等待结束'
            end_time = time.time()
            loading_time = int(end_time - start_time)
            print('载入用时约%d秒' % loading_time)
            html = self.driver.page_source
            return html
        except:
            print('载入失败')
        finally:
            if type(self.debug) == type(1):
                time.sleep(self.debug)
                self.driver.quit()
            elif self.debug == True:
                pass
            else:
                self.driver.quit()
            return html
    def wait(self):
        start_time = time.time()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
        end_time = time.time()
        loading_time = int(end_time - start_time)
        print('跳转用时约%d秒' % loading_time)




if __name__ == '__main__':
    ip = 'https://ip.cn'
    a = webloader(headless=False, image=False, debug=True)
    #a.set_proxy('127.0.0.1',1080)
    url = 'https://www.hyatt.com/zh-CN/shop/rates/shacr?offercode=&rateFilter=standard&kids=0&rooms=1&checkinDate=2019-06-29&adults=1&checkoutDate=2019-06-30'
    b = a.get_page(url)
    import code
    code.interact(banner="", local=locals())
