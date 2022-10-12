#coding=gbk
import threading
from queue import Queue
import time,os,re
import random
import requests
from Include.useragents.myran import Myran
from Include.mysql_db.mysql_db import comic_db
from Include.app.down_img import saveimg
from threading import Lock

class Data(threading.Thread):
    def __init__(self):
        super().__init__()
        self.comicmk_dir()
    def run(self):
        print('�߳�%s��ʼ��' % self.getName())
        while not data_empty:
            try:
                time.sleep(0.5)
                data_trupe=data_queue.get(False)
                img_name=(data_trupe[4].split('.'))[0]
                photo_name=re.search(r"(��\d+Ԓ)",data_trupe[3]).group(1)
                path_album="G:\\comic\\%s"%data_trupe[0]
                path_photo="G:\\comic\\%s\\%s"%(data_trupe[0],photo_name)
                path_img="G:\\comic\\%s\\%s\\%s.jpg"%(data_trupe[0],photo_name,img_name)
                with lock:#�ж��ļ����Ƿ����Ҫ����
                    if not os.path.exists(path_album):os.mkdir(path_album)
                    if not os.path.exists(path_photo):os.mkdir(path_photo)
                if not os.path.exists(path_img):
                    print(data_trupe)
                    #scramble_id=220980 ��ҳ�̶�ֵ
                    if data_trupe[2]>220980:#albumid>aid��ʹ��ƴ�Ӻ��� ����ֱ������
                        print("ƴ��ͼƬ")
                        saveimg.app(data_trupe[-1],data_trupe[2],path_img)
                    else:
                        print("ֱ������ͼƬ")
                        self.dowm_img(data_trupe[-1],path_img)
                #print("·�������ɹ�")
                # down_img.app(data_trupe)
            except Exception as e:
                print(e.__traceback__.tb_lineno,e)
    def comicmk_dir(self):
        with lock:
            if not os.path.exists("G:\\comic"):
                os.mkdir("G:\\comic")
    def dowm_img(self,url,path_img):
        header={
            "User-Agent":Myran().agents()
        }
        proxy={
            "http":"127.0.0.1:10809",
            "https":"127.0.0.1:10809"
        }
        try:
            s=random.choice(list(range(3)))+1+random.random()
            time.sleep(s)
            print("time.sleep=%d"%s)
            response = requests.get(url,headers=header,proxies=proxy)
            if response.status_code == 200:
                with open(path_img,"wb") as f:
                    f.write(response.content)
            else:print("ͼƬrequestʧ��")
        except Exception as e:
            print(e.__traceback__.tb_lineno,e)


data_queue = Queue()
data_empty = False
lock=Lock()
def app():
    global data_queue,data_empty
    sql = "SELECT a.albumId,a.albumname,b.photo_id,b.photo_name,c.img_name,c.img_url FROM (comicone a INNER JOIN comictwo b on a.albumId=b.albumId) INNER JOIN comicthree c on b.photo_id=c.photo_id order by b.photo_id DESC"
    datalist = comic_db.select_2(sql)
    if not datalist == False:
        for data_trupe in datalist:
            print(data_trupe)
            # down_img.app(data_trupe)
            data_queue.put(data_trupe)
    data_max = data_queue.qsize()
    print("data_queue��С:%s" % data_max)
    data_list = list(range(5))
    datathread_list = []
    for i in data_list:
        data = Data()
        data.start()
        datathread_list.append(data)

    while not data_queue.empty():
        pass
    page_empty = True
    for i in datathread_list:
        i.join()
        print("%s������" % i.getName())
if __name__ == '__main__':
    app()