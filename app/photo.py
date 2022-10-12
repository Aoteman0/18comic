# coding=gbk
import json
import re
import threading
import time
from multiprocessing import Queue

from Include.app.option_head import *
from Include.mysql_db.mysql_db import comic_db


class Mhall(threading.Thread):
    def __init__(self, twodict):
        self.twodict = twodict
        self.page = ()
        super().__init__()

    def run(self):
        print('线程%s开始了' % self.getName())
        while not page_empty:
            time.sleep(0.5)
            with webdriver.Chrome(options=option) as driver:
                try:
                    self.page = page_queue.get(timeout=2)
                except Exception as e:
                    pass
                #driver.switch_to.new_window('tab')
                driver.get(self.page[1])
                print(self.page)
                # 最新話ID是0就遍历全部url
                try:
                    driver.implicitly_wait(30)
                    divxpath=driver.find_element(By.XPATH, self.twodict["data_div"])
                    #print("divxpath",divxpath)
                except Exception as e:
                    divxpath=False
                    # pngname = time.strftime("%H.%M.%S")
                    # driver.get_screenshot_as_file("%s.png"%pngname)
                    #print(e.__traceback__.tb_lineno,e)
                try:
                    if divxpath:
                        if comic_db.select("SELECT * FROM `comicone` where albumId=%s and photo_lastid = '0' " % self.page[0]):
                            alist = divxpath.find_elements(By.XPATH, self.twodict["data_a"])
                            print("全部兄弟标签",len(alist))
                            self.parse(alist, driver)
                        else:
                            #print("xpath",self.twodict["data_id"]%self.page[0])
                            alist = divxpath.find_elements(By.XPATH, self.twodict["data_id"]%self.page[2])
                            print("兄弟标签",len(alist))
                            if alist:self.parse(alist, driver)
                            else:
                                upsql = "update comicone set lastdate=CURDATE() where albumId=%s"
                                comic_db.insert(upsql,self.page[0])
                        #print("%d %s" % (len(alist), self.page))

                    else:
                        print("没拿到div标签",self.page)
                        self.parse_lastzero(driver)
                except Exception as e:
                    print(e.__traceback__.tb_lineno,e)

                # driver.delete_cookie()
                # driver.close()
                # driver.switch_to.window((driver.window_handles)[0])  # driver关闭后要马上切换窗口句柄
                print("线程%s执行完了" % self.getName())
    def parse(self, alist, driver):
        if "完結" in driver.find_element(By.XPATH, self.twodict["type"]).text:
            comicone_state = '1'
        else:
            comicone_state = '0'
        for a in alist:
            try:
                #print("开始了")
                driver.implicitly_wait(20)
                photourl = a.get_attribute('href')
                spantextlist = a.find_elements(By.XPATH, 'li/span')
                phontid = a.get_attribute('data-album')
                photoname = a.get_attribute('textContent')
                # print("photonameall",photonameall)
                for spantext in spantextlist:
                    photoname = re.sub(r'%s|\n' % spantext.get_attribute('textContent'), '', photoname)
                photoname = photoname.encode('GBK', 'ignore').decode('GBk')
                #print("photoname%s"%photoname)
                if not comic_db.select('select * from comictwo where photo_id=%s', phontid):
                    sql = "insert into comictwo(photo_id,photo_name,photo_url,albumId) value(%s,%s,%s,%s)"
                    comic_db.insert(sql, phontid, photoname, photourl,self.page[0])
                else:
                    pass
                    # print('%s已存在'%phontid)

                print(phontid, photoname, photourl,self.page[0])
            except Exception as e:
                print(e.__traceback__.tb_lineno,'%s  alist的长度：%d'%(self.page[0],len(alist)), e)
        if alist[-1]:  # 插入最后一话的aid
            phontlast = alist[-1].get_attribute('data-album')
            upsql = "update comicone set state =%s,photo_lastid = %s,lastdate=CURDATE() where albumId=%s"
            comic_db.insert(upsql, comicone_state, phontlast, self.page[0])
    def parse_lastzero(self, driver):
        try:
            if "完結" in driver.find_element(By.XPATH, self.twodict["type"]).text:
                comicone_state = '1'
            else:
                comicone_state = '0'
            phontid =self.page[0]
            # pngname = time.strftime("%H.%M.%S")
            # driver.get_screenshot_as_file("%s.png"%pngname)
            photoname = "第1話"
            photourlxpath = driver.find_element(By.XPATH, self.twodict["startread"])
            photourl  =photourlxpath.get_attribute('href')
            if not comic_db.select('select * from comictwo where photo_id=%s', phontid):
                sql = "insert into comictwo(photo_id,photo_name,photo_url,albumId) value(%s,%s,%s,%s)"
                comic_db.insert(sql, phontid, photoname, photourl,self.page[0])
            else:
                pass

            upsql = "update comicone set photo_lastid=%s,lastdate=CURDATE() where albumId=%s"
            comic_db.insert(upsql, comicone_state,self.page[0])
        except Exception as e:
            print(e.__traceback__.tb_lineno, e)


page_queue = Queue()
page_empty = False
def app(*args):
    global page_queue,page_empty
    if args==():
        sql = "select albumId,albumurl,photo_lastid from comicone"  # 爬取全部

        #查询comictwo和comicone表albumid差异  查询新书更新comictwo
        #sql="SELECT albumId ,albumurl,photo_lastid " \
        "FROM comicone WHERE albumId " \
        "in (SELECT albumId FROM " \
        "(SELECT albumId FROM comictwo GROUP BY albumId  " \
        "UNION all SELECT albumId FROM comicone) t2 G" \
        "ROUP BY albumId HAVING count(*)=1)"
        # 更新comictwo sql语句
        #sql = "SELECT albumId,albumurl,photo_lastid FROM `comicone` where state='0' and DATEDIFF(CURRENT_DATE,lastdate)>=1"
    else:
        args_str=','.join(args)
        sql = "select albumId,albumurl from comicone where albumId in (%s)"%args_str  # 爬取部分
    #print(sql)
    # sql="select albumId,albumurl  FROM comicone where photo_lastid='0'"#查找默认只有一话的漫画
    albumurllist = comic_db.select_2(sql)
    #print(albumurllist)
    if not albumurllist == False:
        for albumurl_trupe in albumurllist:
            page_queue.put(albumurl_trupe)
        print("page_queue:%s" % page_queue.qsize())
        if len(albumurllist) > 5:
            one_list = list(range(4))
        else:
            one_list = list(range(len(albumurllist)))
        with open('xpathjson.json', 'r') as f:
            page_json = json.loads(f.read())
        onethread_list = []
        starttime = time.perf_counter()
        for i in one_list:
            mhall = Mhall(page_json["two"])
            mhall.start()
            onethread_list.append(mhall)
        while not page_queue.empty():
            pass
        page_empty = True
        for i in onethread_list:
            i.join()
            print("%s结束了,时间共%.2f秒" % (i.getName(), time.perf_counter() - starttime))
    else:
        print("获取comicone失败")
if __name__ == '__main__':
    app()

