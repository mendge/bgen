'''获取某个区下按热度视频视频urls'''
import datetime
import json
import re
from lxml import etree
import requests

class zone():
    def __init__(self, url):
        self.html = requests.get(url).text
        self.tree = etree.HTML(self.html)
        self.baseurl = 'https://s.search.bilibili.com/cate/search?'
        self.parmas = {
            'main_ver': 'v3',
            'search_type': 'video',
            'view_type': 'hot_rank',
            'order': 'click',
            'copy_right': -1,
            'cate_id': 86,
            'page': 1,
            'pagesize': 20,
            'jsonp': 'jsonp',
            'time_from': 20211204,
            'time_to': 20211211
        }

    def geturls(self,pn=2):
        '''从视频分区中按照在分类返回urls，返回的是字典列表，字典键是分类值是该类下url列表， pn是爬取最大页码，按热度排序'''
        urls = []
        #配置时间
        today = datetime.date.today()
        before = today + datetime.timedelta(days=-7)#需要七天前
        time_from = before.year*10000 + before.month*100 + before.day
        time_to = today.year*10000 + today.month*100 + today.day
        #print(time_from,time_to)
        self.parmas['time_from'] = time_from
        self.parmas['time_to'] = time_to

        #按照不同cate_id，获取该区不同分类视频
        infos = re.findall('"name":"(.*?)",.*?,"tid":(\d*),"ps":', self.html)
        for info in infos:
            class_ = {info[0]:[]}
            self.parmas['cate_id'] = int(info[1])
            #翻页获取多页
            for p in range(1,pn+1):
                self.parmas['page'] = p
                nowhtml = requests.get(self.baseurl,params=self.parmas).text
                js = json.loads(nowhtml)['result']
                for i in js:
                    #class_[info[0]].append(i['title'])  #不需要视频title
                    class_[info[0]].append(i['arcurl'])
            urls.append(class_)
        return urls

# # url = 'https://www.bilibili.com/v/cinephile/?spm_id_from=333.5.b_7072696d6172794368616e6e656c4d656e75.57'
# url1 = 'https://www.bilibili.com/v/knowledge/?spm_id_from=333.851.b_7072696d6172794368616e6e656c4d656e75.45'
# s = zone(url1)
# urls = s.geturls(pn=2)
# print(len(urls))
# for i in urls:
#     for k,v in i.items():
#         print(k,v)


