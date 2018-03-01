#-*-coding:utf-8-*-
from api import api_sql as sql

mysql = sql.Api_mySql()

# mysql.open_sql()
mysql.key_query('gt_metas', 'category', 'type')
