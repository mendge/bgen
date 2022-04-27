'''某个搜索结果下的所有视频，提供翻页'''
import urllib.parse
from time import sleep

from lxml import etree
import requests

class search():
    def __init__(self, url):
        '''传入原始搜索结果url'''
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43'}
        self.base_prefix = 'https:'
        self.html = requests.get(url,headers=self.header).text
        self.tree = etree.HTML(self.html)
        self.cmturlformat = url

    def geturls(self,url):
        '''传入一页搜索结果，返回该页面全部视频url'''
        nowhtml = requests.get(url,headers=self.header)
        #查看网页返回状态码
        #nowcode = nowhtml.status_code
        #print(nowcode)
        nowhtml = nowhtml.text
        nowtree = etree.HTML(nowhtml)
        urls = []
        #先获取固定区域html代码
        txt = nowtree.xpath('//ul[contains(@class,"video-list")]')[0]
        links = txt.xpath('//li[contains(@class,"video-item")]/a/@href')
        for link in links:
            urls.append(self.base_prefix + link)
        return urls

    def getpages(self, n=2):
        '''根据传入参数翻页，返回每页搜索结果url地址'''
        pages = []
        for i in range(1,n+1):
            url = self.cmturlformat+'&page=%d' % (i);
            url = urllib.parse.unquote(url)
            pages.append(url)
        return pages


# url = 'https://search.bilibili.com/all?keyword=%E6%90%9E%E7%AC%91'
# s = search(url)
# pages = s.getpages(10)
# for page in pages:
#     print(page)
#     urls = s.geturls(page)
#     for url in urls:
#         print(url)
#     print('\n')
#
#
#
