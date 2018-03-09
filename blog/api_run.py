#-*-coding:utf-8-*-
from api import apiSql as sql
import json
import markdown
# "localhost", "blog", "gtian0122", "blog", charset='utf8'
mysql = sql.MYSQL({
    'host': 'localhost',
    'sql_name': 'blog',
    'user': 'root',
    'password': 'gtian0122'
}, charset='utf8')


def get_html():
    list = article_column_relation()
    res = {}
    res.update(list)
    for key, val in res.items():
        for mk in val:
            mk['text'] = markdown_conversion_html(mk['text'])
    return res


def markdown_conversion_html(markdown_doc):
    extension_list = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
            'markdown.extensions.toc']
    return markdown.markdown(markdown_doc, extensions=extension_list)


def get_nav():
    query_result = query_nav('gt_metas', 'category', 'type')
    result = []
    print('query_result', query_result)
    for res in query_result:
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

    for rf in relation[:]:
        relation_format.append({
          'cid': rf[0],
          'mid': rf[1]
        })
    for ctf in column_type[:]:
        column_type_format.append({
            'mid': ctf[0],
            'name': ctf[1],
            'slug': ctf[2],
            'type': ctf[3],
            'description': ctf[4],
            'count': ctf[5],
            'order': ctf[6],
            'parent': ctf[7]
        })
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
    return return_results(relation_format[:], column_type_format[:], article_format[:])


# 格式化数据
def return_results(relation, column_type, article):
    '''
    返回栏目对应的文章列表
    :param relation: 对应关系
    :param column_type: 获取栏目mid
    :param article: 获取文章cid
    :return: 返回栏目对应的文章列表
    '''
    res = {}
    for info in article:
        # 获取栏目对于关系表
        for re in relation:
            # 获取栏目名称
            for cy in column_type:
                if re['mid'] == cy['mid']:
                    if re['cid'] == info['cid']:
                        key = cy['slug']
                        if key in res:
                            res[key].append(info)
                        else:
                            res[key] = []
                            res[key].append(info)

    return res


# temp = article_column_relation()
# print('\n', temp, '\n')
# for k, v in temp.items():
#     print('Temp\nkey:', k, 'val:', v)
#     print('key:', k, 'val len', len(v))
#     print('-' * 50)
# get_nav()
index()