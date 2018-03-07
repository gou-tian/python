#-*-coding:utf-8-*-
import pymysql
'''
    MySql数据库操作类
'''

class MYSQL:
    '''My sql 操作'''

    def __init__(self, config, charset='utf8'):
        '''
        初始化配置
        :param config: 数据配置参数
            {
                host: 数据地址 str
                user: 数据库用户名 str
                password: 用户密码 str
                sql_name: 链接数据库 str
            }
        :param charset: 字符编码格式默认utf-8 str
        '''
        self.db_host = config['host']
        self.db_user = config['user']
        self.db_password = config['password']
        self.db_sql_name = config['sql_name']
        self.db_charset = charset

    def open_sql(self, sql_statements="SELECT VERSION()", type=None):
        '''打开数据库'''
        self.db = pymysql.connect(self.db_host, self.db_user, self.db_password,
                                  self.db_sql_name, charset=self.db_charset)
        result = None
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()
        try:
            # 使用 execute()  方法执行 SQL 查询
            self.cursor.execute(sql_statements)
            # 使用 fetchall() 接收全部的返回结果行.
            result = self.cursor.fetchall()
        except:
            print('open_sql', 'Error')
            # 如果发生错误则回滚
            self.db.rollback()
        self.db.close()
        if type == 'update':
            return 'update done.'
        return result

    def query(self, sql):
        '''数据查询'''
        return self.open_sql(sql)

    def add_update(self, sql, type=None):
        '''插入/更新数据'''
        return self.open_sql(sql, type)

    def remove(self):
        '''数据修改'''
        pass