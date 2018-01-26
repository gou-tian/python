from flask import Flask, request, make_response, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    # return render_template('index.html', browser=user_agent, cookies=response)
    return render_template('index.html')


@app.route('/about')
def about():
    return '<h1>饺子的介绍</h1>'


@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)


if __name__ == '__main__':
    # host='0.0.0.0',
    # manager.run()
    bt = Bootstrap(app)
    app.run(debug=True)
