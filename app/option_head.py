# coding=gbk
from selenium import webdriver
from Include.useragents.myran import Myran
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

option = webdriver.ChromeOptions()
option.add_argument("--disable-extensions")  # ������չ
# option.add_argument('--incognito')  # ����ģʽ���޺�ģʽ�� ������ץ����
option.add_argument("--disable-software-rasterizer")  # ����3D��դ����
option.add_argument('--no-sandbox')  # ���DevToolsActivePort�ļ������ڵı���
option.add_argument("--disable-gpu")  # �ȸ����GPU����
option.add_experimental_option("excludeSwitches", ["enable-automation"])  # ������վ���selenium ������ģʽ����
option.add_experimental_option('useAutomationExtension', False)  # ȥ����ʾ�Կ�����ģʽ����
option.page_load_strategy = 'none'  # �������������������������ִ��
# prefs = {"profile.managed_default_content_settings.images": 2}
# option.add_experimental_option("prefs", prefs)#������ͼģʽ
option.add_argument('blink-settings=imagesEnabled=false')  # ������ͼƬ, �����ٶ�
option.add_argument("User-Agent=%s" % Myran().agents())  # ��ͷģʽ��Ҫ�������ͷ
option.add_argument("--headless")  # ������ͷģʽ
option.add_argument("--window-size=1920,1050")  # ��ͷģʽ���ô��ڴ�С
# option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome.exe --remote-debugging-port=9222
