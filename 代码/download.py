import os
import re
import requests
from lxml import etree
from seleniumtest import settings

class download():
    def __init__(self):
        self.abspath = r'C:\Users\TTTime\Desktop\Spider\python爬'

    @classmethod
    def dlvideo(self,url):
        '''处理逻辑，判断传进来的url是但视频还是多视频调用不同下载'''
        req = requests.get(url)
        html = req.text
        tree = etree.HTML(html)

        hasone = True
        # 是否能找到多page
        if len(tree.xpath('//*[@id="multi_page"]/div[1]/div[1]/span/text()'))!=0:
            hasone = False
        # 单个视频下载
        if(hasone):
            download.getvideo(url)
        # 多个视频下载
        else:
            download.getvideos(url)

    @classmethod
    def getvideo(self,url):
        '''创建目录，下载单个视频及对应音频，合并'''
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
            # 必须指明跳转页面才能下载视频url的内容
            'referer': url}
        request = requests.get(url)
        html = request.text
        title = re.findall('"title":"(.*?)"',html)[0]
        title = self.stdtitle(title)
        # 指定工作路径
        file_abs = settings.abspath
        os.chdir(file_abs)
        if not os.path.exists(title):
            os.mkdir(title)
        os.chdir(file_abs + '\\' + title)
        vname = 'v' + title + '.mp4'
        aname = 'a' + title + '.mp4'
        #扒取视频及音频地址
        url_video = re.findall(r'\[{"id":\d*,"baseUrl":"(.*?)","base_url":', html)[0]
        url_audio = re.findall(r'"audio":\[{"id":\d*,"baseUrl":"(.*?)",', html)[0]
        # 下载视频及音频
        with open('%s'%vname,'wb') as f:
            response_video = requests.get(url_video,headers=headers).content
            f.write(response_video)
            print(vname + ' download  over')
            f.close()
        with open('%s'%aname ,'wb') as f:
            responese_audio = requests.get(url_audio,headers=headers).content
            f.write(responese_audio)
            print(aname + " download over")
            f.close()
        # 合并视频和音频
        os.system(f'ffmpeg -i "%s" -i "%s" -c copy "{title}.mp4" -loglevel quiet'%(vname,aname))
        # 移除原来视频和音频
        os.remove('%s'%vname)
        os.remove('%s'%aname)
        print('merge over\n\n')

    @classmethod
    def getvideos(self,url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
            'referer': url
        }
        request = requests.get(url)
        html = request.text
        # 获取标题创建文件路径用
        title = re.findall('"title":"(.*?)"',html)[0]
        title = re.findall('"title":"(.*?)"', html)[0]
        title = self.stdtitle(title)
        tree = etree.HTML(html)
        # 解析视频个数
        pn = tree.xpath('//*[@id="multi_page"]/div[1]/div[1]/span/text()')[0]
        pn = re.findall('/(\d+?)\)',pn)[0]
        pn = int(pn)
        # 指定工作路径
        file_abs = settings.abspath
        os.chdir(file_abs)
        if not os.path.exists(title):
            os.mkdir(title)
        os.chdir(file_abs + '\\' + title)
        # 获取标准无多余参数视频url，方便翻页下载视频
        try:
            stdurl = re.findall('(https://www.bilibili.com/video/.{12})', url)[0]

            for p in range(1,10):

                # 解析当前单个视频
                nowurl = stdurl+'?p='+str(p)
                r = requests.get(nowurl)
                h = r.text

                url_video = re.findall('"video":\[{"id":\d+,"baseUrl":"(.*?)"', h)[0]
                url_audio = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)"', h)[0]

                nowtitle = re.findall('"page":%s,"from":"vupload","part":"(.*?)"'%str(p),html)[0]
                title = self.stdtitle(title)

                vname = 'v'+nowtitle+'.mp4'
                aname = 'a'+nowtitle+'.mp4'

                with open('%s'%vname,'wb') as f:
                    response_video = requests.get(url_video,headers=headers).content
                    f.write(response_video)
                    print(vname + ' download  over')
                    f.close()
                with open('%s'%aname,'wb') as f:
                    responese_audio = requests.get(url_audio,headers=headers).content
                    f.write(responese_audio)
                    print(aname + " download over")
                    f.close()

                os.system(f'ffmpeg -i "%s" -i "%s" -c copy "{nowtitle}.mp4" -loglevel quiet'%(vname,aname))

                os.remove('%s'%vname)
                os.remove('%s'%aname)
                print('merge over\n\n')
        except Exception as e:
            pass

    @classmethod
    def getimg(self,url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
            # 必须指明跳转页面才能下载视频url的内容
            'referer': url
        }
        request = requests.get(url)
        html = request.text
        url_img = re.findall('"thumbnailUrl":\["(.*?)"\]',html)[0]
        title = re.findall('"title":"(.*?)"',html)[0]
        title = self.stdtitle(title)
        # 指定工作路径
        file_abs = settings.abspath
        os.chdir(file_abs)
        if not os.path.exists(title):
            os.mkdir(title)
        os.chdir(file_abs + '\\' + title)



        iname = title+'.jpg'
        with open('%s' % iname, 'wb') as f:
            responese_audio = requests.get(url_img, headers=headers).content
            f.write(responese_audio)
            print(iname + " download over")
            f.close()

    @classmethod
    def stdtitle(cls,title):
        # 合并文件名不能存在特殊字符
        title = title.replace('/', '')
        title = title.replace('\\', '')
        title = title.replace(':', '')
        title = title.replace('*', '')
        title = title.replace('?', '')
        title = title.replace('"', '')
        title = title.replace('<', '')
        title = title.replace('>', '')
        title = title.replace('|', '')
        title = title.replace(' ', '')
        return title



# # 杀死那个石家庄的人
# getvideo.getvideo('https://www.bilibili.com/video/BV1Wy4y1B7f6/')
# # 周杰伦歌曲合集
# getvideo.getvideos('https://www.bilibili.com/video/BV1Dh41167W4?from=search&seid=9257784826128009596&spm_id_from=333.337.0.0')