import pymysql
# from twisted.enterprise import adbapi
import time

dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'root',
    'db' : 'test'
}

sqls = ['select 1', 'select VERSION()']

result = []

class DBHelper():
    def __init__(self, dbInfo, sqls):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        # self.sqls = dbInfo['sqls']


    def insert(self, item):
        # sqls = "insert into movie_info(movie_name,actor,time) values(%s,%s,%s,%s)"
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db
        )
        # 游标建立的时候就开启了一个隐形的事务
        cur = conn.cursor()
        try:
            for command in self.sqls:
                cur.execute(command)
                result.append(cur.fetchone())
            # 关闭游标
            cur.close()
            conn.commit()
        except:
            conn.rollback()
        # 关闭数据库连接
        conn.close()

        return item