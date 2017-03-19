#coding=utf8


import urllib
import urllib2
import re
import time
# 核心代码
# page=1
# url='http://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
# # Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36
# headers = {'User-Agent':user_agent}
# try:
# 	request = urllib2.Request(url,headers=headers)
# 	response = urllib2.urlopen(request)
# 	content = response.read().decode('utf-8','ignore')
# 	pattern = re.compile(r'<div class="newArticleHead">.*?<span class="touch-user-name-a">(.*?)</span>.*?'
# 				+ '<div class="content-text">.*?<span>(.*?)</span>(.*?)article_info.*?data-votes=.*?>(.*?)</span>', re.S)
# 	items = re.findall(pattern, content)
# 	for item in items:
# 		hasImg = re.search('img',item[2])
# 		if not hasImg:
# 			print(item[0] + '\t\t' + item[3] + '\n' + item[1] + '\n')
# except urllib2.URLError as e:
# 	if hasattr(e, 'code'):
# 		print(e.code)
# 	if hasattr(e, 'reason'):
# 		print(e.reason)
# 	print(type(e))




# Note:这是用正则表达式匹配的方式来抓取网页数据的，所以如果网站改版，正则表达式是要自己修正的
# 爬取糗事百科的搞笑段子
class QiuBaiSpider:

	QiuBai_url = 'http://www.qiushibaike.com/hot/page/'

	# 构造器
	def __init__(self):
		# 下一次要加载的页码
		self.pageIndex = 1
		self.user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
		self.headers = {'User-Agent':self.user_agent}
		# 每个元素为一页糗百内容
		self.page_stories = []
		# 是否连载的标志位
		self.enable = False

	# 接收页码,返回页面源代码
	def getCodeByIndex(self, pageIndex):
		try:
			url = QiuBaiSpider.QiuBai_url + str(pageIndex)
			request = urllib2.Request(url, headers=self.headers)
			response = urllib2.urlopen(request)
			pageCode = response.read().decode('utf-8', 'ignore')
			return pageCode
		except urllib2.URLError as e:
			if hasattr(e, 'reason'):
				print('Can\'t connect to %s, the reason is %s' %(url, e.reason))
			return None

	# 接收页码，返回本页不带图片的段子列表（过滤了带图片的段子）
	def getStoriesByIndex(self, pageIndex):
		# 存放当前页面的段子列表
		stories_list = []
		pageCode = self.getCodeByIndex(pageIndex)
		if not pageCode:
			print("Fail to load the page")
			return None
		pattern = re.compile(r'<div class="newArticleHead">.*?<span class="touch-user-name-a">(.*?)</span>.*?'
			+ '<div class="content-text">.*?<span>(.*?)</span>(.*?)article_info.*?data-votes=.*?>(.*?)</span>', re.S)
		items = pattern.findall(pageCode)
		# item[0]:用户名称 	item[1]:段子文本  item[2]:网页中杂七杂八的内容，可能会有图片   item[3]:点赞数
		for item in items:
			hasImg = re.search('<img', item[2])
			if not hasImg:
				text = re.sub('<br/>', '\n' , item[1])
				stories_list.append([item[0].strip(), item[3].strip(), text.strip()])
		return stories_list

	# 加载新一页，提取内容加入到列表
	def loadNewPage(self):
		if self.enable == True:
			curr_page_stories = self.getStoriesByIndex(self.pageIndex)
			if curr_page_stories:
				self.page_stories.append(curr_page_stories)
				self.pageIndex += 1

	# 加载一页段子，逐个展示
	def showOneStory(self, slist, page_number):
		for story in slist:
			cmd = raw_input()
			if cmd == 'Q' or cmd == 'q':
				self.enable = False
				return 
			print(u'正在阅读第%s页, 作者: %s \t\t点赞数: %s \n %s' %(page_number, story[0], story[1], story[2]))



	# start
	def start(self):
		print(u'正在加载糗事百科...按任意键开始阅读，按Q|q退出')
		begin_time = time.time()
		self.enable = True
		# 先加载两页
		self.loadNewPage()
		self.loadNewPage()
		current_page_number = 0
		while self.enable:
			current_page_number += 1
			slist = self.page_stories[0]
			del self.page_stories[0]
			self.showOneStory(slist, current_page_number)
			self.loadNewPage()
		print(u'程序退出')
		end_time = time.time()
		print(u'你一共在线观看了%s s' %str(end_time-begin_time))


if __name__ == '__main__':
	spider = QiuBaiSpider()
	spider.start()
			










