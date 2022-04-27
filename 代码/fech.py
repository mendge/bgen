import json
from seleniumtest import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import re


class fetch():
    def __init__(self):
        self.url = 'https://www.bilibili.com/'
        self.loginurl = 'https://passport.bilibili.com/login'
        # 需要自己初始化
        self.username = ''
        self.password = ''
        self.browser = self.buildbrowser()

    def buildbrowser(self):
        '''需要配置Chromedriver，可网上学着配'''
        try:
            chrome_options = Options()
            # 启动无头模式，实际上是用命令行来对Google浏览器进行限制
            chrome_options.add_argument('--headless')
            # 加上这个东东用来防止bug
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            #chromedriver.exe 位置
            #你需要配置自己chromedriver.exe的路径
            s = Service(r'C:\Users\TTTime\AppData\Local\Microsoft\WindowsApps\chromedriver.exe')
            return webdriver.Chrome(options=chrome_options, service=s)
        except:
            return None

    def login(self):
        '''模拟登录，由于图灵测试，并未成功'''
        self.browser.get(self.loginurl)
        wait = WebDriverWait(self.browser, 10)
        #等待到某个点加载出来
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login-username')))
        username = self.browser.find_elements(by=By.XPATH, value='// *[ @ id = "login-username"]')[0]
        username.send_keys(self.username)
        password = self.browser.find_elements(by=By.XPATH, value='// *[ @ id = "login-passwd"]')[0]
        password.send_keys(self.password)
        self.browser.close()

    def updatecookies(self):
        '''更新cookies到txt文件，可以加载来使用，但我没用到'''
        self.browser.get(self.url)
        wait = WebDriverWait(self.browser, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nav_searchform > input')))
        dictCookies = self.browser.get_cookies()  # 获取list的cookies
        jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存
        print(jsonCookies)
        with open(settings.cookiespath, 'w') as f:
            f.write(jsonCookies)
            f.close()
        print('Cookies update over')

#
# f = fetch()
# f.updatecookies()
