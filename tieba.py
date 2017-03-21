#coding=utf8

import urllib
import urllib2
import re
import time


# Use 're' module to replace some tags which are unpopular
class TagsTool:

	img_pattern = re.compile(r'<img.*?>| {7}')
	a_pattern = re.compile(r'<a.*?>|</a>')
	line_pattern = re.compile(r'<tr>|<div>|</div>|</p>')
	td_pattern = re.compile(r'<td>')
	p_pattern = re.compile(r'<p.*?>')
	br_pattern = re.compile(r'<br><br>|<br>')
	extra_tag_pattern = re.compile(r'<.*?>')

	# Use 're' module to replace some tags which are unpopular
	def replace(self, content):
		content = re.sub(self.img_pattern, '', content)
		content = re.sub(self.a_pattern, '', content)
		content = re.sub(self.line_pattern, '\n', content)
		content = re.sub(self.td_pattern, '\t', content)
		content = re.sub(self.p_pattern, '\n', content)
		content = re.sub(self.br_pattern, '\n', content)
		content = re.sub(self.extra_tag_pattern, '', content)
		return content.strip()






# 贴吧爬虫，一个实例爬取一个贴子
class TieBaSpider:

	# see_lz: 是否只看楼主发言
	def __init__(self, base_url, see_lz):
		self.base_url = base_url
		self.see_lz = see_lz
		self.tags_tool = TagsTool()
		self.default_filename = u'百度贴吧'
		# 贴吧的楼层
		self.floor = 1
		# 存放结果的文件对象
		self.file = None


	def getPageCode(self, page_num):
		url = self.base_url + '?see_lz=' + str(self.see_lz) + '&pn=' + str(page_num)
		try:
			request = urllib2.Request(url)		
			response = urllib2.urlopen(request)
			return response.read().decode('utf-8', 'ignore')
		except urllib2.URLError as e:
			if hasattr(e, 'reason'):
				print(u'连不上百度贴吧，原因是:' + e.reason)
			return None

	def getTitle(self):
		pageCode = self.getPageCode(1)
		pattern = re.compile(r'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
		match = pattern.search(pageCode)
		if match:
			return match.group(1).strip().encode('utf-8')
		else:
			return None

	def getTotalPageNum(self):
		pageCode = self.getPageCode(1)
		pattern = re.compile(r'<li class="l_reply_num.*?<span class="red">(.*?)</span>', re.S)
		match = pattern.search(pageCode)
		if match:
			return match.group(1).strip()
		else:
			return None

	def getContentByPageNum(self, page_num):
		pageCode = self.getPageCode(page_num)
		pattern = re.compile(r'<div id="post_content.*?class="d_post_content.*?>(.*?)</div>', re.S)
		# If one or more groups are present in the pattern, return a list of groups;  
		# this will be a list of tuples if the pattern has more than one group. 
		items = pattern.findall(pageCode)
		content = []
		for item in items:
			content.append(self.tags_tool.replace(item).encode('utf-8'))
		return content

	# The method should be called firstly before 'writeData2File'
	def createFile(self, filename):
		if filename is not None:
			self.file = open(filename + '.txt', 'w+')
		else:
			self.file = open(self.default_filename + '.txt', 'w+')

	# @Parameter data: a list of byte stream
	def writeData2File(self, data):
		if self.file:
			for item in data:
				self.file.write(item)
				# 定义分隔符
				space = '\n' + '-'*30 + str(self.floor) + u'楼' + '-'*30 + '\n'
				self.file.write(space.encode('utf-8'))
				self.floor += 1


	def start(self):
		try:
			title = self.getTitle()
			print('贴子标题为 :' + str(title))
			total_page_num = self.getTotalPageNum()
			print('该贴子共有' + str(total_page_num) + '页' )
			for i in range(1,int(total_page_num) + 1):
				print('正在写入第' + str(i) + '页')
				self.writeData2File(self.getContentByPageNum(i))
		except IOError as e:
			print("写入文件发生异常，原因是" + e.reason)
		finally:
			print("操作完成...")



if __name__ == '__main__':
	print(u'请输入贴子编号:')
	base_url = 'http://tieba.baidu.com/p/' + str(raw_input('http://tieba.baidu.com/p/'))
	see_lz = raw_input('是否只读取楼主发言，1:yes 0:no \n')
	filename = raw_input('请输入保存的文件名称: ')
	spider = TieBaSpider(base_url, see_lz)
	spider.createFile(filename)
	spider.start()



# http://tieba.baidu.com/p/3138733512






