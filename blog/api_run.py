#-*-coding:utf-8-*-
from api import apiSql as sql
# "localhost", "blog", "gtian0122", "blog", charset='utf8'
mysql = sql.MYSQL({
    'host': 'localhost',
    'sql_name': 'blog',
    'user': 'blog',
    'password': 'gtian0122'
}, charset='utf8')

# mysql.open_sql()
# mysql.query('gt_metas', 'category', 'type')
def get_nav():
    query_result = query_nav('gt_metas', 'category', 'type')
    result = []
    print('query_result', query_result)
    for res in query_result:
        # print(res)
        # print('-'*50)
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
    print(result)


def query_nav(tab_name, column_val, column_name):
    '''
        导航数据查询
        :param tab_name: 表名 str
        :param column_val: 查询类别 str
        :param column_name: 查询字段 str
        :return: 返回查询结果 tuple
    '''
    sql = "SELECT * FROM blog." + tab_name + " where " + column_name + "='" + column_val + "'"
    # print(sql)
    return mysql.query(sql)

# 插入/更新栏目数据
def add_update_nav(gt_metas, data):
    sql = 'INSERT INTO ' + gt_metas + \
          '(name,slug,type,description,count,`order`,parent) values("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
          (data['name'], data['slug'], data['type'], data['description'],
           data['count'], data['order'], data['parent']) + \
          ' on duplicate key update slug=VALUES(slug),name=VALUES(name)'
    mysql.add_update(sql, 'update')
    get_nav()


# 查询文章对应关系并归类
def article_column_relation():
    '''查询文章对应关系并归类'''
    # 查询对应CID和MID关系
    relation = mysql.query('SELECT * FROM blog.gt_relationships')
    relation_format = []
    # 查询栏目类别
    column_type = mysql.query("SELECT * FROM blog.gt_metas where type='category'")
    column_type_format = []
    # 查询文章对应列表
    article = mysql.query('SELECT * FROM blog.gt_contents where slug!="start-page"')
    article_format = []
    # print(relation[0], '\n', column_type[0], '\n', article[0])
    for rf in relation[:]:
        relation_format.append({
          'cid': rf[0],
          'mid': rf[1]
        })
    # print(relation_format[0])
    for ctf in column_type[:]:
        column_type_format.append({
            'min': ctf[0],
            'name': ctf[1],
            'slug': ctf[2],
            'type': ctf[3],
            'description': ctf[4],
            'count': ctf[5],
            'order': ctf[6],
            'parent': ctf[7]
        })
    # print(column_type_format[0])
    for af in article[:]:
        article_format.append({
        'cid': af[0],
        'title': af[1],
        'slug': af[2],
        'created': af[3],
        'modified': af[4],
        'text': af[5],
        'order': af[6],
        'authorId': af[7],
        'template': af[8],
        'type': af[9],
        'status': af[10],
        'password': af[11],
        'commentsNum': af[12],
        'allowComment': af[13],
        'allowPing': af[14],
        'allowFeed': af[15],
        'parent': af[16]
    })
    # print(article_format[0])
    return_results(relation_format[:], column_type_format[:], article_format[:])


def return_results(relation, column_type, article):
    '''
    返回栏目对应的文章列表
    :param relation: 对应关系
    :param column_type: 获取栏目mid
    :param article: 获取文章cid
    :return: 返回栏目对应的文章列表
    '''
    count = 0
    num = 0
    print('\n', 'relation len:', len(relation), '\n', 'column_type len:',
          len(column_type), '\n', 'article len:', len(article), '\n')
    # print(relation)
    article_temp = []
    # while count < len(relation):
    #     try:
    #         while num < len(article):
    #             # print(relation[count]['cid'] == article[num]['cid'])
    #             if relation[count]['cid'] == article[num]['cid']:
    #                 article_temp.append({
    #                     'cid': article[num]['cid'],
    #                     'body': article[num]
    #                 })
    #                 # print(relation[count]['cid'], article[num]['cid'])
    #                 print("article_temp[num]['cid']", article_temp[num]['cid'])
    #                 # if article_temp[num]['cid'] != None:
    #                 #     if article_temp[num]['cid'] != article[num]['cid']:
    #                 #         print(article_temp)
    #                 #         article_temp.append({
    #                 #             'cid': article[num]['cid'],
    #                 #             'body': article[num]
    #                 #         })
    #                 # else:
    #                 #     article_temp.append({
    #                 #         'cid': article[num]['cid'],
    #                 #         'body': article[num]
    #                 #     })
    #             print('count', count, 'num', num)
    #             num+=1
    #
    #     except:
    #         pass
    #
    #     count += 1
    #     # try:
    #     #     if relation[count]['cid']:
    #     #         print('???', relation[count]['cid'] in article[count])
    #     #         print('????', relation[count]['cid'], article[count]['cid'])
    #     #         # if article[count]['cid'] == relation[count]['cid']:
    #     #         #     print(article[count])
    #     #     count += 1
    #     # except:
    #     #     return None

    for k in relation:
        # print(k)
        for j in article:
            if k['cid'] == j['cid']:
                # pass
                # print(k['cid'], j['cid'], k, j)
                # print(j['cid'], article_temp)
                print(j['cid'] in article_temp)
                print('article_temp:', article_temp)
                if len(article_temp) > 0:
                    for v in article_temp:
                        if j['cid'] in v:
                            pass
                        else:
                            article_temp.append({
                                'cid': j['cid'],
                                'body': j
                            })
                else:
                    article_temp.append({
                        'cid': j['cid'],
                        'body': j
                    })
    # print(article_temp)
    for a in article_temp:
        print(a)
# -------------------------------------
# get_nav()
# add_update_nav('gt_metas',{
#             'name': 'TRE',
#             'slug': 'php',
#             'type': 'category',
#             'description': '',
#             'count': 0,
#             'order': 0,
#             'parent': 0
#         })
article_column_relation()