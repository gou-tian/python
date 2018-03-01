#-*-coding:utf-8-*-
import pymysql
import json
'''
数据库操作类
'''


class Api_mySql:
    '''数据库操作'''

    def __init__(self):
        '''初始化'''
        self.result = ''
        self.db = pymysql.connect("localhost", "blog", "gtian0122", "blog", charset='utf8')
        try:
            # 执行sql语句
            self.cursor = self.db.cursor()
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()


    def open_sql(self, conditions="SELECT VERSION()"):
        '''打开数据，并执行参数'''
        # 使用 execute()  方法执行 SQL 查询
        self.cursor.execute(conditions)
        # 使用 fetchall() 接收全部的返回结果行.
        data = self.cursor.fetchall()
        self.result = data

    def close_sql(self):
        # 关闭数据库连接
        self.db.close()

    def add(self):
        '''增加'''
        self.close_sql()

    def key_query(self, tab_name, column_val, column_name='cid',):
        '''查询'''
        sql = "SELECT * FROM `blog`." + tab_name  + " where " + column_name + "='" + column_val + "'"
        self.open_sql(sql)
        result = []
        for res in self.result:
            print(res)
            print('-'*50)
            result.append({
            'mid': res[0],
            'name': res[1],
            'slug': res[2],
            'type': res[3],
            'description': res[4],
            'count': res[5],
            'order': res[6],
            'parent': res[7]
        })
        self.close_sql()
        # print(result)
        return result

    def insert(self):
        '''修改/查询'''
        self.close_sql()

    def remove(self):
        '''删除'''
        self.close_sql()
