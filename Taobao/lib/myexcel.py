# -*-coding:utf-8-*-
import xlrd
import xlwt
import config
from xlutils.copy import copy
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# 创建一个excel文件，初始化一个表sheet1
def new_excel(filename=config.OUT_FILE):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    book.add_sheet('sheet1', cell_overwrite_ok=True)
    book.save(filename)
    print(u'已成功创建文件%s' %filename)


# 判断文件中是否存在指定的内容
def is_word_exist(word, filename=config.OUT_FILE):
    try:
        workbook = xlrd.open_workbook(filename)
        sheet = workbook.sheet_by_index(0)
        words = sheet.col_values(0)
        if word in words:
            return True
        else:
            return False
    except IOError as e:
        if 'No such file' in e.strerror:
            print(u'function :is_word_exist未找到文件%s' %filename)
        return False


# 写入一个tuple到一个excel文件中的一行
def write_one_line(contents, filename=config.OUT_FILE):
    print(u'正在写入到文本中')
    try:
        name = contents[0]
        if is_word_exist(name, filename):
            print(u'%s已经存在，跳过该内容不写入' % name)
        else:
            readbook = xlrd.open_workbook(filename)
            row = readbook.sheets()[0].nrows
            writebook = copy(readbook)
            sheet = writebook.get_sheet(0)
            count = 0
            for content in contents:
                sheet.write(row, count, content)
                count += 1
            writebook.save(filename)
            print(u'已成功写入到文件%s第%d行' %(filename, int(row)+1))
    except IOError:
        print(u'写入到文件%s的过程出错!' %filename)


# 写文件
def write_to_excel(datas, filename=config.OUT_FILE):
    if len(datas) < 3:
        print(u'数据不完整，不写入文件')
    else:
        name = datas[0]
        comment = datas[1]
        url = datas[2]
        contents = (name, comment, url)
        write_one_line(contents=contents, filename=filename)


# 读取config.COUNT_FILE文件，获得已分析的链接数
def get_count(filename=config.COUNT_FILE):
    try:
        with open(filename, 'r') as fp:
            page = fp.read()
            if not page:
                return 0
            else:
                return page
    except Exception:
        print(u'无法找到文件%s' %filename)
        return 0


def write_count(count, filename=config.COUNT_FILE):
    try:
        with open(filename, 'w') as f:
            f.write(str(count))
            f.close()
    except TypeError:
        print(u'写入页码过程失败')









