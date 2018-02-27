from flask import Flask, request, make_response, render_template, url_for
from flask_script import Manager
import json
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)

# 初始化页面（首页）
@app.route('/')
def index():
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
    print('request.method', request.method)
    res = navDefaultList
    print(res)

    return json.dumps(res)

# 以下为测试单元
# 测试方法：ajax接口测试
# 返回传入数据
@app.route('/ajax_return', methods=['GET', 'POST'])
def ajax_return():
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
    app.run(debug=True, host = '0.0.0.0')
