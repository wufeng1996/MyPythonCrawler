# -*-coding:utf-8 -*-
import time
import sys
from selenium.common.exceptions import NoSuchElementException,TimeoutException,WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from pyquery import PyQuery as pq

from lib import myexcel
import config

reload(sys)
sys.setdefaultencoding("utf-8")


# 把页面下拉一次，尝试触发网页的ajax请求，如果找到目标元素，返回True
# count 是下拉的次数，经过测试之后，每次拉动距离和 count 是平方关系比较科学
def scroll_to_bottom(driver, count):
    print(u'正在尝试第%d次下拉' %count)
    try:
        js = "window.scrollTo(0,document.body.scrollHeight-" + str(count * count* 100) + ")"
        driver.execute_script(js)
    except WebDriverException:
        print(u'下拉寻找过程出错')
    time.sleep(3)
    try:
        driver.find_element_by_css_selector('#J_TjWaterfall li')
    except NoSuchElementException:
        return False
    return True


# 不断调用scroll_to_bottom，直到目标出现或者达到最大下拉次数
def is_fully_load(driver, max_scroll_time=config.MAX_SCROLL_TIME):
    count = 1
    result = scroll_to_bottom(driver, count)
    while not result:
        count += 1
        result = scroll_to_bottom(driver, count)
        if count == max_scroll_time:
            return False
    return True


# 获取宝贝详情页面的源码，如果加载成功，则返回源码，否则返回False
def get_page_code(url):
    driver = config.DRIVER
    timeout = config.TIMEOUT
    max_scroll_time = config.MAX_SCROLL_TIME
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "J_TabBarBox"))
        )
    except TimeoutException:
        return False
    print(u'开始寻找下方推荐宝贝')
    if is_fully_load(driver, max_scroll_time):
        print(u'已经成功加载下方橱窗宝贝推荐栏目')
        return driver.page_source
    else:
        return False


def get_datas_from_one_page(url):
    # datas is a list of dict, each dict is a <li> tag
    datas=[]
    if not url.startswith('http'):
        url = 'https:' + url
    html = get_page_code(url)
    if html:
        doc = pq(html)
        items = doc('#J_TjWaterfall > li').items()
        for item in items:
            url = item.find('a').attr('href')
            if not url.startswith('http'):
                url = 'https:' + url
            # comment_list is a list of tuple,each tuple is a <p> tag
            comment_list = []
            comments = item.find('p').items()
            for comment in comments:
                comment_user = comment.find('b').remove().text()
                comment_content = comment.text()
                comment_list.append((comment_user, comment_content))
            datas.append({'url': url, 'comment_info': comment_list})
        return datas
    else:
        print(u'抓取网页失败，跳过')
        return []


def write_datas_to_file(datas):
    for data in datas:
        url = data.get('url')
        comment_list = data.get('comment_info')
        for item in comment_list:
            comment_user = item[0]
            comment_content = item[1]
            myexcel.write_to_excel((comment_user, comment_content, url))








