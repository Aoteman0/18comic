import webbrowser

from Include.app.option_head import *
import threading
import time
from  Include.mysql_db.mysql_db import comic_db
from queue import Queue
import json

class Data(threading.Thread):
    def __init__(self,updatexpath):
        super().__init__()
        self.update_dict=updatexpath
    def run(self):
        print("线程%s启动了"%self.getName())
        try:
            driver=webdriver.Chrome(options=option)
            while not data_empty:
                time.sleep(0.5)
                try:
                    data_tuple = data_queue.get(block=False)
                except:
                    pass
                print(data_queue.qsize())
                #with webdriver.Chrome(options=option) as driver:
                driver.switch_to.new_window('tab')#先打开
                driver.get(data_tuple[1])
                #关闭标签或者窗口需要转换句柄
                driver.close()
                driver.switch_to.window((driver.window_handles)[0])
            driver.quit()
        except Exception as e:
            print(e.__traceback__.tb_lineno,e)

def app():
    global data_queue,data_empty
    sql="SELECT albumId,albumurl FROM comicone " \
        "where state='0' " \
        "and DATEDIFF(CURRENT_DATE,lastdate)>7"
    with open('xpathjson.json', 'r') as f:
        page_json = json.loads(f.read())
    albumlist = comic_db.select_2(sql)
    data_list=[]
    data_treadlist=[]
    if albumlist:
        for album in albumlist:
            data_queue.put(album)
        data_list=list(range(3))if len(albumlist)>5 else list(range(len(albumlist)))
    for i in data_list:
        data = Data(page_json['updatexpath'])
        data.start()
        data_treadlist.append(data)

    while not data_queue.empty():
         pass
    data_empty=True
    for thread in data_treadlist:
        thread.join()
        print("线程%s结束了"%thread.getName())
data_queue=Queue()
data_empty=False
if __name__ == '__main__':
    app()