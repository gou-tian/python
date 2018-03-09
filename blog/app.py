from flask import Flask, request, make_response, render_template, url_for
from flask_script import Manager
from api import apiSql as sql
import json
import markdown
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)
mysql = sql.MYSQL({
    'host': 'localhost',
    'sql_name': 'blog',
    'user': 'root',
    'password': 'gtian0122'
}, charset='utf8')
navDefaultList = []


# 初始化页面（首页）
@app.route('/')
def index():
    list = json.loads(article_column_relation())
    print(list)
    return render_template('index.html', name='饺子博', nav=json.loads(nav()), list=get_html())


# 自我简介
@app.route('/about')
def about():
    return '<h1>饺子的介绍</h1>'


# 获取导航数据
@app.route('/nav', methods=['GET'])
def nav():
    '''
        数据查询对应导航列表，并返回查询结果
        :return [{'title': '首页 | Home', 'url': '/'}]
    '''
    res = get_nav()
    return json.dumps(res)


@app.route('/<column_name>', methods=['GET'])
def get_column_content(column_name):
    return column_name


# 查询文章对应关系并归类
@app.route('/list',  methods=['GET'])
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
    return_res = {}
    key = 'data'
    return_res[key] = return_results(relation_format[:], column_type_format[:], article_format[:])
    return json.dumps(return_res)


# 获取导航
def get_nav():
    query_result = query_nav('gt_metas', 'category', 'type')
    result = []
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
    return result


# 获取导航栏目信息
def query_nav(tab_name, column_val, column_name):
    '''
        导航数据查询
        :param tab_name: 表名 str
        :param column_val: 查询类别 str
        :param column_name: 查询字段 str
        :return: 返回查询结果 tuple
    '''
    sql = "SELECT * FROM blog." + tab_name + " where " + column_name + "='" + column_val + "'"
    return mysql.query(sql)


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


# markdown转换html
def markdown_conversion_html(markdown_doc):
    extension_list = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
            'markdown.extensions.toc', 'markdown.extensions.codehilite']
    return markdown.markdown(markdown_doc, extensions=extension_list)


def get_html():
    page_list = json.loads(article_column_relation())['data']
    print(type(page_list), page_list)
    for key, val in page_list.items():
        for mk in val:
            mk['text'] = markdown_conversion_html(mk['text'])
    print(page_list)
    return page_list



# 以下为测试单元
# 测试方法：ajax接口测试
# 返回传入数据
@app.route('/ajax_return', methods=['GET', 'POST'])
def ajax_return(name):
    '''借口请求测试函数，返回传入参数'''
    res = []
    print('request.method', request.method)
    if request.method == 'POST':
        print('request.form', request.form)
        if 'name' in request.form:
            res = loop(request.form.items(), request.method)
    else:
        if len(request.args) < 1:
            return '参数列表为空。'
        if 'name' in request.args:
            print('request.args', request.args)
            res = loop(request.args.items(), request.method)
        else:
            res = None
    return json.dumps(res) if res != None else None


def loop(data, methods):
    '''获取对应数据'''
    res = {}
    for k, v in data:
        res['methods'] = methods
        res[k] = v
    return res


if __name__ == '__main__':
    # host = '0.0.0.0'
    # manager.run()
    # bt = Bootstrap(app)
    app.run(debug=True, host='0.0.0.0')
