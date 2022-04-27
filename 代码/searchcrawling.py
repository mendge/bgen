from time import sleep

import pymysql

from seleniumtest import settings
from seleniumtest.search import search
from seleniumtest.spider import spider

class crawl():
    '''传入搜索结果url，指定爬取的页数，直接爬取信息到数据库，并且下载响应视频和封面'''
    def __init__(self,url,page=2):
        self.url = url
        self.page = page

    def crawling(self):
        db = settings.db
        cursor = db.cursor()

        sear = search(self.url)
        pages = sear.getpages(self.page)
        for pageurl in pages:
            sleep(1)
            print(pageurl)
            urls = sear.geturls(pageurl)
            for url in urls:
                try:
                    print(url)
                    s = spider(url)
                    if(s.exist==False):
                        continue
                    info = s.getinfo()
                    sql = "insert into info(BV, title, date, views, dms, likes, coins, collects, shares) \
                                                   values('{}', '{}',  '{}',  '{}', '{}', '{}', '{}', '{}', '{}');"\
                                                    .format(info['BV号'], info['视频标题'], info['上传日期'],info['观看数'],\
                                                     info['弹幕数'], info['点赞数'], info['投币数'], info['收藏数'], info['转发数'] )
                    cursor.execute(sql)
                except Exception as e:
                    print(e)
                    # print('不能存储url:' + url)
                    continue
                else:
                    print('store info over')
                    s.storehots()
                    # s.storecmts()
                    s.downloadvideo()
                    s.downloadimg()

                # s.downloadimg()
                # s.yougetvideo()

        print("reaserch crawling over")
        cursor.close()
        db.close()


# searchurl = 'https://search.bilibili.com/all?keyword=%E6%90%9E%E7%AC%91'
# c = crawl(searchurl)
# c.crawling()

