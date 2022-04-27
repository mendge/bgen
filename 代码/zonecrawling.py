from time import sleep
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import _thread
import pymysql

from seleniumtest import settings
from seleniumtest.zone import zone
from seleniumtest.spider import spider
class crawl():
    '''传入分区url，指定其不同分类每类的爬取页数，将基本信息存入数据库，并且下载对应视频和封面到指定路径'''
    def __init__(self,url,pn=2):
        self.url = url
        self.pn = pn

    def crawling(self):
        '''多线程失败版本，只用单线程'''
        db = settings.db
        cursor = db.cursor()
        z = zone(self.url)
        class_ = z.geturls(pn=2)
        #利用线程池
        #出问题没做出来
        # pool = ThreadPoolExecutor()
        # print(len(class_))
        for c in class_:
            v = list(c.values())
            # print(v)
            self.action(v[0],cursor)
            # pool.submit(self.action,v[0], cursor)
        # pool.shutdown()

        cursor.close()
        db.close()
        print("zone Crawling over")

    def action(self, list, cursor=None):
        '''爬取传入url列表视频的基本信息、视频、图片'''
        if(cursor==None):
            print('Invalied cursor')
            return
        for url in list:
            sleep(1)
            try:
                s = spider(url)
                if(s.exist==False):
                    print('请求错误')
                    continue
                # print(url)
                info = s.getinfo()
                sql = "insert into info(BV, title, date, views, dms, likes, coins, collects, shares) \
                                values('{}', '{}',  '{}',  '{}', '{}', '{}', '{}', '{}', '{}');" \
                                .format(info['BV号'], info['视频标题'], info['上传日期'], info['观看数'],\
                            info['弹幕数'], info['点赞数'], info['投币数'], info['收藏数'], info['转发数'])

                cursor.execute(sql)
            except pymysql.err.IntegrityError as e:
                print('视频信息已存储过')
                continue
            except pymysql.err.DataError:
                print('插入数据库错误')
                continue
            except Exception as e:
                print(e)
                print('出问题url:' + url)
            else:
                print('store info over')
                s.storehots()
                s.storecmts()
                s.downloadimg()
                s.downloadvideo()

# T1 = time.perf_counter()
# url = 'https://www.bilibili.com/v/cinephile/?spm_id_from=333.5.b_7072696d6172794368616e6e656c4d656e75.57'
# c = crawl(url)
# c.crawling()
# T2 = time.perf_counter()
# print('程序运行时间:%s秒' % ((T2 - T1)))

url = 'https://www.bilibili.com/v/music/?spm_id_from=333.851.b_7072696d6172794368616e6e656c4d656e75.3'
c = crawl(url,pn=2)
c.crawling()