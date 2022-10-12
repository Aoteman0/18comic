# coding=gbk
from mysql.connector.pooling import MySQLConnectionPool


class Comic:
    def __init__(self):
        self.createdata_comic()
        self.comicone_table()
        self.comictwo_table()
        self.comicthree_table()

    def createdata_comic(self):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            cursor.execute('create database comic')
        except Exception as e:
            print('数据库comic存在')
            # print(e.__traceback__.tb_lineno,e)
        finally:
            pool.set_config(database='comic')
            # print("comic关闭游标和连接con")
            cursor.close()
            con.close()

    def comicone_table(self):
        comicone_table = (
            "create table comicone("
            "id int unsigned auto_increment primary key, "
            "albumId int unsigned not null ,"
            "albumname varchar(70) not null,"
            "albumurl varchar(70) not null,"  # 图书链接 直到简介
            "state enum('2','1','0') default '0',"  # 状态1为 已完结 0为未完结 2为只有单独一话
            "score int not null ,"  # 人气
            "coverurl varchar(70) not null,"  # 封面url
            "photo_lastid SMALLINT default 0,"  # 最后一话的ID 
            "lastdate date not null,"  # 本地最后更新时间
            "index (state),"
            "index (lastdate),"
            "UNIQUE index(albumname),"
            "UNIQUE index(albumId))")
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            cursor.execute(comicone_table)
        except Exception as e:
            print("comicone表已存在")
            # print(e.__traceback__.tb_lineno,e)
        finally:
            if 'con' in dir():
                # print("comic关闭游标和连接con")
                cursor.close()
                con.close()

    def comictwo_table(self):
        comictwo_table = (
            "create table comictwo("
            "id int unsigned auto_increment primary key,"
            "photo_id int unsigned not null,"
            "photo_name varchar(70) not null,"
            "photo_url varchar (70) not null,"
            "albumId int unsigned not null,"
            "UNIQUE (photo_id),"
            "index (albumId))")
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            cursor.execute(comictwo_table)
        except Exception as e:
            print("comictwo表已存在")
            # print(e.__traceback__.tb_lineno,e)
        finally:
            if 'con' in dir():
                # print("comic关闭游标和连接con")
                cursor.close()
                con.close()

    def comicthree_table(self):
        comicthree_table = (
            "create table comicthree("
            "id int unsigned auto_increment primary key,"
            "img_name varchar(10) not null,"
            "img_url varchar(70) not null,"
            "photo_id int unsigned not null,"
            "UNIQUE (photo_id,img_name))")
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            cursor.execute(comicthree_table)
        except Exception as e:
            print("comicthree表已存在")
            # print(e.__traceback__.tb_lineno,e)
        finally:
            if 'con' in dir():
                # print("comic关闭游标和连接con")
                cursor.close()
                con.close()

    def insert(self, sql, *var):  # comic表数据插入  更新也可以使用
        # print("var:",type(var[0]))
        try:
            # var = (146417,'秘密教学 / 秘密の授業','https:/um/146417/','0',468800,'https://cdn-63344851')
            con = pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, var)
            con.commit()
            #print("插入成功", var)
        except Exception as e:
            print("已存在", var, e.__traceback__.tb_lineno, e)
        finally:
            if 'con' in dir():
                # print("关闭游标和连接con")
                cursor.close()
                con.close()
            # print(e.__traceback__.tb_lineno, e)
    def insertmany(self, sql, var):  # comic表数据插入  更新也可以使用
        #print("var:",var)
        try:
            # var = (146417,'秘密教学 / 秘密の授業','https:/um/146417/','0',468800,'https://cdn-63344851')
            con = pool.get_connection()
            cursor = con.cursor()
            cursor.executemany(sql, var)
            con.commit()
            #print("插入成功", var)
        except Exception as e:
            print("已存在", var, e.__traceback__.tb_lineno, e)
        finally:
            if 'con' in dir():
                # print("关闭游标和连接con")
                cursor.close()
                con.close()
            # print(e.__traceback__.tb_lineno, e)

    def select(self, sql, *albumId):  # 带参select
        try:
            # print("albumId%s"%albumId)
            # sql = "select * from comicone where albumId=%s"
            con = pool.get_connection()
            cursor = con.cursor()
            #print(sql, albumId)
            cursor.execute(sql, albumId)
            if cursor.fetchall() == []:
                return False
            else:
                return True
        except Exception as e:
            print(albumId, e.__traceback__.tb_lineno, e)
        finally:
            if 'con' in dir():
                # print("关闭游标和连接con")
                cursor.close()
                con.close()

    def select_2(self, sql):  # 不带参select
        try:
            #print(sql)
            # print("albumId%s"%albumId)
            #sql = "select albumId,albumurl from comicone"
            con = pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            if result == []:
                return False
            else:
                return result
        except Exception as e:
            print(e.__traceback__.tb_lineno, e)
        finally:
            if 'con' in dir():
                # print("关闭游标和连接con")
                cursor.close()
                con.close()


config = {
    "host": "127.0.0.1",
    "port": "3306",
    "user": "root",
    "password": "12345678"
}
try:
    pool = MySQLConnectionPool(
        **config,
        pool_size=10
    )
except Exception as e:
    print("mysql数据库连接池创建失败",e.__traceback__.tb_lineno,e)
comic_db = Comic()
# sql2="insert into comicone value(null,%s,%s,%s,%s,%s,%s,0,CURDATE())"
# sql2="select * from comicone where albumId=%s"
# sql = "insert into comictwo(photo_id,photo_name,photo_url,albumId) value(%s,%s,%s,%s)"
# comic_db.insert(sql, '2545', '第44話50的靜恩', 'http1758', '180459')
# print(comic_db.select(sql2,179377))
# sql = "select albumId,albumurl from comicone"
# print(comic_db.select_2(sql)[0])
# a=[[1,'322','2134',2525],[134,'3224','21344',25425]]
# comic_db.insertmany("insert into comicthree values (%s,%s,%s,%s)",a)
