#coding=gbk
from Include.useragents.myran import Myran
import requests
import io
import re
import functools
from PIL import Image
from Include.mysql_db.mysql_db import comic_db
from Include.app import photo
from Include.app import imgcomic

#输入名称或者简介网址进行搜索
def select_album(albumname):
    sql_albumname='on a.albumId=b.albumId and albumname like "%%%s%%"'
    sql_albumurl='on a.albumId=%s and a.albumId=b.albumId'
    sql_album ='SELECT a.albumId,a.albumname,b.photo_id,b.photo_name,date_format(a.lastdate,"%%Y-%%m-%%d") ' \
        'FROM comicone a INNER JOIN comictwo b '

    sql_albumid1 = 'select albumId from comicone where albumname like "%%%s%%"'
    albumid=[]
    if albumname:
        tmp=re.findall(r'https://18comic.vip/album/(\d+)',albumname)
        if re.findall(r'[\u4E00-\u9FA5\s]+', albumname)!=[]:
            list_all = comic_db.select_2((sql_album+sql_albumname%albumname))
            albumid=list(map(lambda k:k[0],comic_db.select_2((sql_albumid1%albumname))))
        elif tmp!=[]:
            list_all = comic_db.select_2(sql_album+sql_albumurl%tmp[0])
            albumid=tmp

    if list_all:
        list_all.sort(key=functools.cmp_to_key(dataaaa))#先根据albumid排序 再根据話数更新
        for i  in list_all:
            print(i)
    return tuple(albumid)
def dataaaa(x1,x2):
    x1_name=re.findall(r'第(\d+)話',x1[3])[0]
    x2_name=re.findall(r'第(\d+)話',x2[3])[0]
    if x1[0]!=x2[0]:
        return x1[0]-x2[0]
    else:
        return int(x1_name)-int(x2_name)
if __name__ == '__main__':
    s = "Run away/離開"
    s2="https://18comic.vip/album/229077"
    res = re.findall(r'[\u4E00-\u9FA5\\s]+',s)
    http = re.findall(r'https://18comic.vip/album/(\d+)',s2)
    print(http)
    print(select_album(s2))
    #imgcomic.app('146417','196319')