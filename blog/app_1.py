from flask import Flask, url_for, request
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def api():
    return 'Welcome'


@app.route('/data')
def api_data():
    if 'da' in request.args:
        print(request.args['da'])
        return request.args['da']
    else:
        return 'none'


if __name__ == '__main__':
    # debug=True
    app.run()
