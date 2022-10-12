# coding=gbk
import json
import re
import time
import threading
from multiprocessing import Queue
from Include.app.option_head import *
from Include.mysql_db.mysql_db import comic_db


class Mhall(threading.Thread):
    def __init__(self, onedict):
        self.onedict = onedict
        self.page = ''
        super().__init__()

    def run(self):
        print('�߳�%s��ʼ��' % self.getName())
        while not page_empty:
            time.sleep(0.5)
            with webdriver.Chrome(options=option) as driver:
                try:
                    self.page = page_queue.get(block=False)
                except:
                    pass
                print(self.page)
                driver.get(self.page)
                driver.implicitly_wait(30)
                divlist = driver.find_elements(By.XPATH, self.onedict["xpath_mvtr"])
                if len(divlist) == 0:
                    print("����30��ûץ��a��ǩ��")
                    page_queue.put(self.page)
                    continue
                print("%d %s" % (len(divlist), self.page))
                self.parse(divlist)

    def parse(self, divlist):
        for div in divlist:
            try:
                a_href = div.find_element(By.XPATH, self.onedict["mhurl"]).get_attribute('href')
                albumid = re.findall(r'/(\d+)/', a_href)[0]
                name = div.find_element(By.XPATH, self.onedict["name"]).text
                name = name.encode('GBK', 'ignore').decode('GBk')
                typesstr = div.find_element(By.XPATH, self.onedict["type"]).text
                if '��Y' in typesstr:
                    state = '1'
                else:
                    state = '0'
                scorestr = div.find_element(By.XPATH, self.onedict["renqi"]).text
                if "K" in scorestr:
                    score = int(re.sub(r'[.K]', '', scorestr)) * 100  # �Ѵ�K������ֵתΪ����
                else:
                    score = int(scorestr)
                coverurl = div.find_element(By.XPATH, self.onedict["fmurl"]).get_attribute("src")
                if 'blank' in coverurl: coverurl = div.find_element(By.XPATH, self.onedict["fmurl"]).get_attribute(
                    "data-original")
                if not comic_db.select('select * from comicone where albumId=%s', albumid):
                    sql = "insert into comicone value(null,%s,%s,%s,%s,%s,%s,0,CURDATE())"
                    comic_db.insert(sql, albumid, name, a_href, state, score, coverurl)
                else:
                    print('%s%s�Ѵ���' % (albumid, name))
            except Exception as e:
                print(e.__traceback__.tb_lineno, e)

        # print("�B�d��", '��Y')


def pagenummax(driver, onedict):  # ��ȡ���ҳ��
    try:
        driver.implicitly_wait(20)
        selectlist = driver.find_elements(By.XPATH, onedict["pagemax_select"])  # ͨ��select��ǩ�õ����ҳ��
        selectobj = Select(selectlist[0])
        selectobj_option = selectobj.options
        return selectobj_option
        # print(selectobj_option[0].get_attribute("value"))
    except Exception as e:
        return []
        print(e.__traceback__.tb_lineno, e)


page_queue = Queue()
page_empty = False
def app():
    global page_queue,page_empty
    url = 'https://18comic.vip/albums/hanman'
    with open('xpathjson.json', 'r') as f:
        page_json = json.loads(f.read())
        # print(page_json["one"])
    with webdriver.Chrome(options=option) as driver:
        driver.get(url)
        print(driver.current_window_handle)
        page_optionlist = pagenummax(driver, page_json["one"])
        print("���%dҳ" % len(page_optionlist))
        maxpage = len(page_optionlist)
        for i in page_optionlist:
            page_queue.put(i.get_attribute("value"))
    if maxpage > 5:
        one_list = list(range(5))
    else:
        one_list = list(range(maxpage))
    onethread_list = []
    for i in one_list:
        mhall = Mhall(page_json["one"])
        mhall.start()
        onethread_list.append(mhall)

    while not page_queue.empty():
        pass
    page_empty = True
    for i in onethread_list:
        i.join()
        print("%s������" % i.getName())
if __name__ == '__main__':
    app()
