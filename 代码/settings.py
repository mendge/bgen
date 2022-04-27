'''配置路径、密码等'''
# youget前缀，主要是便于修改地址
import pymysql

basevideocmd = 'you-get -o D:\\crawledfile\\video '
# 账号密码，用于模拟登录
# 由于未解决图灵测试，我的登录没有做出来
username = ''
password = ''
# 视频、封面文件的存储路径
abspath = r'D:\crawledfile\dict'
cookiespath = 'D:\\crawledfile\\cookies\\cookie.txt'
#配置数据库连接
db = pymysql.Connect(host='127.0.0.1',
                            port=3306,
                            user='root',
                            passwd='1957452zz',
                            db='bilibilidata',
                            charset='utf8mb4',
                            autocommit=True)



'''
基本信息表
 create table info(
	BV varchar(20) primary key,
	title varchar(100) not null,
    date varchar(30) not null,
    views varchar(20) not null,
    dms varchar(20) not null,
    likes varchar(20) not null,
    coins varchar(20) not null,
    collects varchar(20) not null,
    shares varchar(20) not null
    );
热评表
create table hots(
	bv char(12) not null references info(BV),
	content varchar(500) not null,
    likes char(10),
    primary key(bv,content)
    );
评论表
create table cmts(
	bv char(12) not null references info(BV),
	content varchar(500) not null,
    likes char(10),
    primary key(bv,content)
    );
'''