# coding=gbk
import json
import threading
import time
from multiprocessing import Queue
from threading import Lock

from Include.app.option_head import *

from Include.mysql_db.mysql_db import comic_db


class Mhall(threading.Thread):
    def __init__(self, threedict):
        self.threedict = threedict
        self.page = ()
        super().__init__()

    def run(self):
        global pausenum, lock
        print('线程%s开始了' % self.getName())
        while not page_empty:
            time.sleep(0.5)
            try:
                try:
                    self.page = page_queue.get(timeout=2)
                    print(page_queue.qsize())
                except Exception as e:
                    pass
                if not comic_db.select("select * from comicthree where photo_id = %s"%self.page[0]):
                    with webdriver.Chrome(options=option) as driver:
                        #print("self.page",self.page[0])
                        driver.switch_to.new_window('tab')
                        driver.get(self.page[1])
                        driver.implicitly_wait(30)
                        img_list = driver.find_elements(By.XPATH, self.threedict["img_all"])
                        result = self.parse(img_list, driver)
                        if result:
                            sql = "insert into comicthree(img_name,img_url,photo_id) values(%s,%s,%s)"
                            comic_db.insertmany(sql,result)
                        # driver.delete_cookie()
                        # driver.close()
                        # driver.switch_to.window((driver.window_handles)[0])  # driver关闭后要马上切换窗口句柄
                        #print("线程%s执行完了,继续循环" % self.getName())
            except Exception as e:
                print(e.__traceback__.tb_lineno,e)

    def parse(self, img_list, driver):
        imglist=[]
        for img_a in img_list:
            try:
                # print("开始了")
                driver.implicitly_wait(20)
                imgname = img_a.get_attribute('id')
                imgurl = img_a.find_element(By.XPATH, 'img').get_attribute('data-original')
                imglist.append([imgname,imgurl,self.page[0]])
                # if not comic_db.select('select * from comicthree where photo_Id=%s', self.page[0]):
                #     sql = "insert into comicthree value(null,%s,%s,%s)"
                #     comic_db.insert(sql, imgname, imgurl, self.page[0])

            except Exception as e:
                print(e.__traceback__.tb_lineno, e)
        return imglist

page_queue = Queue()
page_empty = False
def app(*args):
    global page_queue,page_empty
    if args == ():
        sql="SELECT photo_id,photo_url " \
            "FROM comictwo WHERE photo_id in " \
            "(SELECT photo_id FROM " \
            "(SELECT photo_id FROM comicthree " \
            "GROUP BY photo_id  UNION all SELECT photo_id FROM comictwo) t2 " \
            "GROUP BY photo_id HAVING count(*)=1)"
        #sql = "select photo_id,photo_url from comictwo" # ORDER BY photo_id desc
    else:
        args_str = ','.join(args)
        sql = "select photo_id,photo_url from comictwo where albumId in (%s)" % args_str  # 爬取部分
    photolist = comic_db.select_2(sql)
    if not photolist == False:
        for albumurl_trupe in photolist:
            page_queue.put(albumurl_trupe)
        print("page_queue:%s" % page_queue.qsize())
        if len(photolist) > 4:
            one_list = list(range(8))
        else:
            one_list = list(range(len(photolist)))
        with open('xpathjson.json', 'r') as f:
            page_json = json.loads(f.read())
        onethread_list = []
        starttime = time.perf_counter()
        for i in one_list:
            mhall = Mhall(page_json["three"])
            mhall.start()
            onethread_list.append(mhall)
        while not page_queue.empty():
            pass
        page_empty = True
        for i in onethread_list:
            i.join()
            print("%s结束了,时间共%.2f秒" % (i.getName(), time.perf_counter() - starttime))
    else:
        print("获取comictwo失败")
if __name__ == '__main__':
    app()
