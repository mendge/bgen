import json
import re
import os
from bs4 import BeautifulSoup
from lxml import etree
import requests
import pymysql

from seleniumtest import settings
from seleniumtest.download import download

class spider():
    def __init__(self, url):
        self.url = url
        self.basevideocmd = 'you-get -o D:\\crawledfile\\video '
        self.baseimgcmd = 'you-get -o D:\\crawledfile\\img '
        self.base_url = 'https://www.bilibili.com'
        self.request = requests.get(url)
        self.html = self.request.text
        #有可能页面不存在
        self.exist = False
        if(self.request.status_code==200):
            self.exist = True
        if(len(re.findall('视频不见了', self.html)) == 0):
            self.exist = True
        self.tree = etree.HTML(self.html)
        self.cmturlformat = 'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&type=1&oid=%s&mode=1'
        self.oid = re.findall('window.__INITIAL_STATE__=\{"aid":(.*?),', self.html)[0]
        '''下面两个变量要运行getinfo()后才有具体值'''
        self.title = ''
        self.BV = ''

    def getinfo(self):
        info = {}

        bv = re.findall('window.__INITIAL_STATE__={"aid":.*?"bvid":"(.{12})', self.html)[0]
        self.BV = bv
        title = self.tree.xpath('//div[contains(@class, "report-wrap-module")]/h1/@title')[0]
        #规范化标题，以便作为文件路径保存
        title = download.stdtitle(title)
        self.title = title
        # introduction = self.tree.xpath('/html/body/div[2]/div[4]/div[1]/div[4]/div[2]/span/text()')[0]
        # introduction = str(introduction)
        #name = self.tree.xpath('/html/body/div[2]/div[4]/div[2]/div[1]/div[2]/div[1]/a[1]/text()')[0]
        # page = self.tree.xpath('/html/body/div[2]/div[4]/div[2]/div[1]/div[2]/div[1]/a[2]/@href')[0]
        # page = str(page)

        view = self.tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div/span[1]/text()')[0]
        view = re.findall('(.*?)播放',view)[0]
        dm = self.tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div/span[2]/text()')[0]
        dm = re.findall('总弹幕数(.*)',dm)[0]
        date = self.tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div/span[3]/text()')[0]
        date = str(date)

        like = self.tree.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/div[1]/span[1]/text()')[0]
        like = re.sub('\n','',re.sub(' ','',like))
        coin = self.tree.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/div[1]/span[2]/text()')[0]
        coin = re.sub('\n','',re.sub(' ','',coin))
        collect = self.tree.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/div[1]/span[3]/text()')[0]
        collect = re.sub('\n','',re.sub(' ','',collect))
        share = self.tree.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/div[1]/span[4]/text()')[0]
        share = re.sub('\n','',re.sub(' ','',share))

        info['BV号'] = bv
        info['视频标题'] = title
        info['上传日期'] = date
        #info['简介'] = introduction
        info['观看数'] = view
        info['弹幕数'] = dm
        info['点赞数'] = like
        info['投币数'] = coin
        info['收藏数'] = collect
        info['转发数'] = share

        return info

    def getlinks(self):
        rec_links = []
        href_links = self.tree.xpath('//div[@class="pic"]/a/@href')
        for link in href_links:
            rec_links.append(self.base_url + str(link))
        return rec_links

    def gethots(self):
        '''返回热评，字典列表'''
        hotsurl = self.cmturlformat % self.oid
        hotstext = requests.get(hotsurl).text
        js = json.loads(hotstext)['data']['hots']
        hotsinfo = []
        for i in js:
            content = i['content']['message']
            like = i['like']
            # replies = i['replies']   回复列表
            #这样的cmtinfo是列表组成的列表形式，其元素第一个是内容，第二个是点赞数，content包含不执行的\r、\n，且只有九条
            hotsinfo.append({'评论点赞数':like, '评论内容':content})
        return hotsinfo

    def getcmts(self):
        '''获取全部评论，字典组成的列表，字典里包括点赞数和内容'''
        cmtinfo = []
        pn = 1
        for p in range(1, 50):
            try:
                flag = False
                cmturl = 'https://api.bilibili.com/x/v2/reply?jsonp=json&type=1&oid=%s&sort=2&pn=%d'
                cmturl = cmturl % (self.oid, p)
                pn += 1
                cmttext = requests.get(cmturl).text
                cmtjs = json.loads(cmttext)['data']['replies']
                for i in cmtjs:
                    like = i['like']
                    content = i['content']['message']
                    if like==None or content==None:
                        flag = True
                        break
                    cmtinfo.append({'评论点赞数':like, '评论内容':content})
                if flag:
                    break
            except Exception as e:
                print(e)
                break
        return cmtinfo

    def yougetvideo(self):
        #去掉多余参数防止报错
        nowurl = re.sub('\?.*', '', self.url)
        filename = self.title + '.mp4 '
        os.system(self.basevideocmd +'-O ' + filename + '--playlist ' + nowurl)

    def downloadimg(self):
        download.getimg(self.url)

    def downloadvideo(self):
        download.dlvideo(self.url)

    def storehots(self):
        hots = self.gethots()

        db = settings.db
        cursor = db.cursor()
        for hot in hots:
            # print(hot['评论点赞数'])
            # print(type(hot['评论内容']), hot['评论内容'])
            try:
                sql = "insert into hots(bv, content, likes) values('%s', '%s',  '%s');"%(self.BV, hot['评论内容'], hot['评论点赞数'])
                cursor.execute(sql)
            except pymysql.err.IntegrityError as e:
                print('重复热评')
                continue
            except pymysql.err.DataError:
                print('过长热论')
            except Exception as e:
                print(e)
        cursor.close()
        db.close()
        print('store hots over')

    def storecmts(self):
        cmts = self.getcmts()
        db = settings.db
        cursor = db.cursor()
        for cmt in cmts:
            # print(cmt['评论点赞数'])
            # print(type(cmt['评论内容']), cmt['评论内容'])
            try:
                sql = "insert into cmts(bv, content, likes) values('%s', '%s',  '%s');"%(self.BV, cmt['评论内容'], cmt['评论点赞数'])
                cursor.execute(sql)
            except pymysql.err.IntegrityError as e:
                print('重复评论')
                continue
            except pymysql.err.DataError:
                print('过长评论')
            except Exception as e:
                print(e)

        cursor.close()
        db.close()
        print('store cmts over')




# url = 'https://www.bilibili.com/video/BV1Dh41167W4?from=search&seid=5806813255345177930&spm_id_from=333.337.0.0'
# s = spider(url)
# info = s.getinfo()
# # for k,v in info.items():
# #     print(k,': ',v)
# # # s.storecmts()
# cmts = s.getcmts()
# for cmt in cmts:
#     print(cmt)



















































