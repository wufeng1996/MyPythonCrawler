# -*-coding:utf-8-*-
from selenium import webdriver

# 存放所有已经爬取到的urls
URLS_FILE = 'file/urls.txt'
# 存放爬取结果的文件
OUT_FILE = 'file/result.xls'
# 存放已经爬取的链接数，方便断点需传
COUNT_FILE = 'file/count.txt'


DRIVER = webdriver.Chrome()

TIMEOUT = 10

MAX_SCROLL_TIME = 15

TOTAL_URLS_COUNT = 0

NOW_URL_COUNT = 0

LOGIN_URL = 'https://login.taobao.com/member/login.jhtml?spm=a21bo.50862.754894437.1.pp6jGw&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F'

SEARCH_LINK = 'https://www.tmall.com/?spm=a220m.1000858.a2226n0.1.kM59nz'

CONTENT = ''

PAGE = 25

FILTER_SHOP = False

ANONYMOUS_STR = '***'