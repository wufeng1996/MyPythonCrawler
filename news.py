# coding=utf-8


# 本demo爬取网易新闻排行榜的数据
# 采用requests module 发起http请求
# 通过正则表达式 / xpath的路径表达式 抓取数据
# 持久化数据到 txt 文件


import os
import re
from lxml import etree
import requests
import time


# Create file if not exist and write the list of tuple encoded with utf-8
def save_file(filepath, filename, lists):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    absolutefilename = filepath + '/' + filename + '.txt'
    with open(absolutefilename, 'w+') as fp:
        for item in lists:
            fp.write("%s\t\t%s\n" % (item[0].encode("utf8"), item[1].encode("utf8")))


# 爬取网易新闻排行榜首页数据，爬取数据格式为：类别名+链接
def crawl_home_page(home_page):
    return re.findall(
        r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>',
        home_page, re.S)


# 采用XPath的路径表达式爬取 网易新闻排行版的具体栏目 条目
# Return type : list of tuple
def crawl_concrete_page(concrete_page):
    '''Regex(slowly) or Xpath(fast)   采用正则耗时300-400s，采用路径表达式耗时3-6s    '''
    # infos = re.findall(r'<td class=".*?">.*?<a href="(.*?)\.html".*?>(.*?)</a></td>', concrete_page, re.S)
    # results = []
    # for url, item in infos:
    #     results.append((item, url + '.html'))
    # return results
    dom = etree.HTML(concrete_page)
    news_items = dom.xpath('//tr/td/a/text()')
    news_url = dom.xpath('//tr/td/a/@href')
    assert(len(news_items) == len(news_url))
    return zip(news_items, news_url)


def start_crawl(url):
    i = 0
    print('Downloading ' + url)
    homepage_code = requests.get(url).content.decode("gbk")
    homepage_results = crawl_home_page(homepage_code)
    filepath = u'网易新闻排行榜'
    save_file(filepath, str(i) + "_" + u'新闻排行榜', homepage_results)
    i += 1
    for item, url in homepage_results:
        print('Downloading ' + url)
        concretepage_code = requests.get(url).content.decode("gbk")
        concretepage_results = crawl_concrete_page(concretepage_code)
        filename = str(i) + "_" + u'新闻排行榜'
        save_file(filepath, filename, concretepage_results)
        i += 1


if __name__ == '__main__':
    print('start crawl-----')
    start_time = time.time()
    start_crawl('http://news.163.com/rank/')
    end_time = time.time()
    print('end crawl-----')
    print('It costs ' + str(end_time-start_time))
