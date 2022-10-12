# coding=gbk
from selenium import webdriver
from Include.useragents.myran import Myran
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

option = webdriver.ChromeOptions()
option.add_argument("--disable-extensions")  # 禁用拓展
# option.add_argument('--incognito')  # 隐身模式（无痕模式） 开启会抓不了
option.add_argument("--disable-software-rasterizer")  # 禁用3D光栅化器
option.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
option.add_argument("--disable-gpu")  # 谷歌禁用GPU加速
option.add_experimental_option("excludeSwitches", ["enable-automation"])  # 避免网站检测selenium 开发者模式调用
option.add_experimental_option('useAutomationExtension', False)  # 去掉提示以开发者模式调用
option.page_load_strategy = 'none'  # 不等它加载完所有组件就往下执行
# prefs = {"profile.managed_default_content_settings.images": 2}
# option.add_experimental_option("prefs", prefs)#设置无图模式
option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
option.add_argument("User-Agent=%s" % Myran().agents())  # 无头模式下要添加请求头
option.add_argument("--headless")  # 设置无头模式
option.add_argument("--window-size=1920,1050")  # 无头模式设置窗口大小
# option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome.exe --remote-debugging-port=9222
