# -*-coding:utf-8-*-
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq
import config
import sys
import locale
import re


reload(sys)
sys.setdefaultencoding("utf-8")

shop_list = []
link_list = []


# 通过selenium打开搜索页面，搜索栏接收一个关键词，返回搜索结果的网页内容（第一页）
def begin_search(keyword):
    driver = config.DRIVER
    link = config.SEARCH_LINK
    driver.get(link)
    try:
        # 显式等待:指定搜索页面的搜索框(id="mq")，然后设置最长等待时间。
        # 如果在这个时间还没有找到元素，那么便会抛出异常了
        WebDriverWait(driver, config.TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "mq"))
        )
    except TimeoutException:
        print(u'请求超时，加载搜索页面失败')
    try:
        element = driver.find_element_by_css_selector('#mq')
        print(u'成功定位到搜索栏')
        keyword = keyword.decode('utf-8', 'ignore')
        print(u'输入的关键字为:' + keyword)
        for word in keyword:
            element.send_keys(word)
        element.send_keys(Keys.ENTER)
    except NoSuchElementException:
        print(u'当前页面没有找到搜索栏')
    print(u'正在查询该关键字...')
    try:
        WebDriverWait(driver, config.TIMEOUT).until(
            # 以有商品图片为证说明查询成功
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_ItemList div.productImg-wrap"))
        )
    except TimeoutException:
        print(u'关键字查询超时')
    html = driver.page_source
    return html


# 使用PyQuery解析Html，获得商品的店铺名称+详情链接，将所有链接写入文件
def parse_html(html):
    if html is not None:
        doc = pq(html)
        products = doc('#J_ItemList .product').items()
        for product in products:
            shop = product.find('.productShop-name').text()
            href = product.find('.productImg').attr('href')
            if shop and href:
                if config.FILTER_SHOP:
                    if not shop in shop_list:
                        shop_list.append(shop)
                        link_list.append(href)
                        write_file(href)
                        print(u'当前已采集' + len(shop_list) + u'个店铺')
                    else:
                        print(u'店铺' + shop + u'已经存在')
                else:
                    shop_list.append(shop)
                    link_list.append(href)
                    write_file(href)
                    print(u'当前已采集%d个链接' %len(link_list))


def get_total_pages(html):
    doc = pq(html)
    elements = doc('.ui-page-skip :input').items()
    for element in elements:
        if element.attr('name') == 'totalPage':
            return element.attr('value')
    return 1


# 通过selenium来点击下一页按钮，获得下一页的网页内容
def get_next_page_html():
    print(u'准备采集下一页的宝贝信息')
    driver = config.DRIVER
    # try:
    #     # 把内容滚动到指定的坐标
    #     js = "window.scrollTo(0,document.body.scrollHeight)"
    #     driver.execute_script(js)
    # except WebDriverException:
    #     print(u'页面下拉失败')
    #     return None
    try:
        next_button = driver.find_element_by_css_selector('#content b.ui-page-num > a.ui-page-next')
        next_button.click()
    except NoSuchElementException:
        print(u'找不到翻页按钮')
        return None
    # 令其等待5s加载新页面
    driver.implicitly_wait(5)
    try:
        WebDriverWait(driver, config.TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_ItemList div.productImg-wrap'))
        )
    except TimeoutException:
        print(u'翻页过程查询超时')
        return None
    return driver.page_source


# 完成整个解析关键字过程，将所有的url写入文件
def parse_keyword():
    keyword = raw_input(u"请输入要提取链接的关键字:").decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    print(u'关键字为%s,开始提取内容...' %keyword)
    try:
        clear_file()
        html = begin_search(keyword)
        # total_pages = get_total_pages(html)
        total_pages = 5
        parse_html(html)
        for i in range(1, int(total_pages) + 1):
            print(u'当前完成第%d页' %i)
            html = get_next_page_html()
            parse_html(html)
        print(u'采集结束，共采集%d个链接' % (len(link_list)))
    except Exception:
        print(u'提取过程出错!')
        with open(config.URLS_FILE, 'w') as fp:
            fp.write(config.CONTENT)
            fp.close()
            print(u'已回滚原文件内容')
    finally:
        config.DRIVER.close()


def write_file(content):
    try:
        with open(config.URLS_FILE, 'a') as fp:
            fp.write(content + '\n')
            fp.close()
    except Exception:
        print(u'写入文件过程出错了')


# 清除文件内容，在清除前会把文件内容暂存在内存
def clear_file():
    try:
        with open(config.URLS_FILE, 'r') as fp:
            config.CONTENT = fp.read()
            fp.close()
        print(u'正在清空链接文件')
        with open(config.URLS_FILE, 'w'):
            pass
    except Exception:
        print(u'清空链接文件过程出错')


def get_exist_links():
    try:
        with open(config.URLS_FILE, 'r') as fp:
            content = fp.read()
            pattern = re.compile(r'(.*?//.*?)\s', re.S)
            links = pattern.findall(content)
            return links
    except Exception as e:
        print(u'获取文件中的链接失败，错误原因为 %s' %e.message)


if __name__ == '__main__':
  parse_keyword()











