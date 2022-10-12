
爬取韩漫

album.py 默认爬取韩漫书名 类型 人气 并且保存到comicone数据库

photo.py 爬取每本漫画话数链接 并且保存comictwo数据库 向第一层数据库插入每本漫画的当前最新话aid

imgcomic.py 爬取每话每张图片的名称和url保存到comicthree数据库

down_img:拼凑完整图片的逻辑代码

dowm_one:单独下载每话

download:下载全数据库图片 并且保存本地

option_head: selenium头部导入文件

update：可以更新数据库漫画

xpathjson:存放爬取网址的xpath语句

mysql_db.py 创建mysql数据库comic和三个表 comicone,commictwo,comicthree

myran:随机获取一个user-agent


安装：
python3.7+ 、 mysql

安装pillow 分割拼凑图片用

pip install pillow -i https://pypi.douban.com/simple

安装selenium 自动化测试工具

pip install selenium -i https://pypi.douban.com/simple

安装PyExecJS 在python中执行js

pip install PyExecJS

安装mysql-connector-python来创建mysql连接池

pip install mysql-connector-python

安装requests 获取网页数据

pip install requests

