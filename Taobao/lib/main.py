# -*-coding:utf-8-*-
import config
import sys
import os
from lib import myrecommends, mylinks, myexcel

reload(sys)
sys.setdefaultencoding("utf-8")


# 将一个页面的数据写入文件
def scrap(url):
    datas = myrecommends.get_datas_from_one_page(url)
    myrecommends.write_datas_to_file(datas)


def start_from_input():
    print(u'准备从输入中采集链接，请稍等')
    print(u'请输入宝贝链接:')
    url = raw_input()
    driver = config.DRIVER
    driver.get(config.LOGIN_URL)
    print(u'完成登录之后，输入任意键，开始执行爬取')
    raw_input()
    scrap(url)
    print(u'采集结束')


def start_from_file():
    print(u'准备从文件中采集链接,请稍等')
    driver = config.DRIVER
    driver.get(config.LOGIN_URL)
    print(u'完成登录之后，输入任意键，开始执行爬取')
    raw_input()
    # 获得链接总数
    link_list = mylinks.get_exist_links()
    config.TOTAL_URLS_COUNT = len(link_list)
    # 获得已读数目
    num_of_done = myexcel.get_count()
    print(u'文件中共有%d个链接，上次爬取到第%d个' %(int(config.TOTAL_URLS_COUNT), int(num_of_done)))
    print(u'输入１继续爬取，输入２重新爬取')
    command = raw_input()
    if command == '2':
        print(u'开始重新爬取')
        num_of_done = 0
    if int(num_of_done) < int(config.TOTAL_URLS_COUNT):
        for count in range(int(num_of_done), int(config.TOTAL_URLS_COUNT)):
            url = link_list[count]
            print(u'正在爬取第%d个网页，共%d个' %(count+1, config.TOTAL_URLS_COUNT))
            scrap(url)
            count += 1
            myexcel.write_count(count)
        print(u'采集结束')
    else:
        print(u'链接上次已经全部采集完毕')


# 如果相关文件不存在则创建
def create_all_files():
    print(u'正在准备相关文件，请稍等')
    if not os.path.exists(config.URLS_FILE):
        with open(config.URLS_FILE, 'w'):
            pass
    if not os.path.exists(config.COUNT_FILE):
        with open(config.COUNT_FILE, 'w'):
            pass
    if not os.path.exists(config.OUT_FILE):
        myexcel.new_excel(config.OUT_FILE)


def start():
    print('*'*20 + u'天猫宝贝评论采集' + '*'*20)
    create_all_files()
    print(u'如果需要重新选择关键字进行评论采集，请输入0')
    command = raw_input()
    if command == "0":
        mylinks.parse_keyword()
    print(u'从文件采集数据请输入１，手动指定宝贝链接请输入２')
    command = raw_input()
    if command == '1':
        start_from_file()
    elif command == '2':
        start_from_input()
    else:
        print(u'请输入正确参数')
        config.DRIVER.close()


if __name__ == '__main__':
    start()
