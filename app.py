# -*- coding: utf-8 -*-

from flask import Flask, url_for,render_template
app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    # return 'Welcome to My Watchlist!'
    return render_template('index.html',name=name,movies=movies)

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='greyli'))
    print(url_for('user_page', name='peter'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test page'

# 定义虚拟数据
name = 'lihaonihao'
movies = [
    {
        'title': 'My Neighbor Totoro','year':'1988'
    },
    {
        'title': 'Three Colours trilogy','year':'1993'
    },
    {
        'title': 'Forrest Gump','year':'1994'
    },
    {
        'title': 'Memento','year':'2000'
    }
]

if __name__ == '__main__':
    app.run(debug=True)