from flask import Flask, request, make_response, render_template, url_for
from flask_script import Manager
from api import apiSql as sql
import json
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)
mysql = sql.MYSQL({
    'host': 'localhost',
    'sql_name': 'blog',
    'user': 'blog',
    'password': 'gtian0122'
}, charset='utf8')
navDefaultList = []


# 初始化页面（首页）
@app.route('/')
def index():
    # print('column_name:', column_name)
    # print(type(column_name), isinstance(column_name, str))
    # if isinstance(column_name, str):
    #     get_column_content(column_name)
    # nav()
    return render_template('index.html')


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
    navDefaultList = [
        {'title': '首页 | Home', 'url': '/'},
        {'title': 'Python', 'url': 'javascript:;'},
        {'title': 'JavaScript', 'url': 'javascript:;'},
        {'title': 'Css|Style', 'url': 'javascript:;'},
        {'title': '关于我 | About Me', 'url': '/about'}
    ]
    res = get_nav('gt_metas', 'category', 'type')
    print((res))
    navDefaultList = res
    return json.dumps(res)


@app.route('/<column_name>', methods=['GET'])
def get_column_content(column_name):
    print('get_column_content', column_name)
    print(request.args)
    return column_name


# 获取导航
def get_nav(metas, category, slug):
    '''
    栏目查询
    :param metas: 表名 str
    :param category: 查询类别 str
    :param slug: 查询字段 str
    :return: 返回拼装结果 dict
        [
            {
                "name": "css/html",
                "type": "category",
                "count": 4,
                "order": 1,
                "slug":
                "css-html",
                "description": null,
                "parent": 0, "mid": 1
            }
        ]
    '''
    query_result = mysql.query(metas, category, slug)
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
    print('result', result)
    return result


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
