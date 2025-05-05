# -*- coding: utf-8 -*-
import os
import sys
import click
from flask import Flask, url_for,render_template,redirect,flash,request
from flask_sqlalchemy import SQLAlchemy



WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix ='sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控

db = SQLAlchemy(app) # 实例化数据库对象

@app.cli.command() # 定义命令行命令
@click.option('--drop', is_flag=True, help='Create after drop.') # 定义选项
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

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

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


app.config['SECRET_KEY'] = 'dev'  # 设置密钥

@app.route('/',methods=['GET','POST'])
@app.route('/index')
@app.route('/home')
def index():
    # return 'Welcome to My Watchlist!'
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(title) > 60 or len(year) > 4:
            flash('Invalid input.')  # 显示错误信息
            return redirect(url_for('index'))  # 重定向回首页
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Movie added.')  # 显示成功信息
        return redirect(url_for('index'))  # 重定向回首页
    
    user = User.query.first()    # 取出第一个用户
    movies = Movie.query.all()   # 取出所有电影
    return render_template('index.html',movies=movies)

@app.route('/delete/<int:movie_id>',methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 根据电影ID取出电影，如果不存在则返回404错误
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')  # 显示成功信息
    return redirect(url_for('index'))  # 重定向回首页
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

@app.errorhandler(404)  # 定义404错误处理函数
def page_not_found(e):
    user = User.query.first()    # 取出第一个用户
    return render_template('404.html'), 404  # 返回404页面

# 模板上下文处理函数
@app.context_processor
def inject_user():  # 定义模板上下文处理函数
    user = User.query.first()    # 取出第一个用户
    return dict(user=user)  # 返回字典

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 根据电影ID取出电影，如果不存在则返回404错误
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(title) > 60 or len(year) > 4:
            flash('Invalid input.')  # 显示错误信息
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回编辑页面
        
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')  # 显示成功信息
        return redirect(url_for('index'))  # 重定向回首页
    return render_template('edit.html', movie=movie)  # 编辑电影信息页面
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

class User(db.Model): # 定义User模型
    id = db.Column(db.Integer, primary_key=True) # 主键
    name = db.Column(db.String(50)) # 姓名

class Movie(db.Model): # 定义Movie模型
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影名
    year = db.Column(db.String(4)) # 年份



if __name__ == '__main__':
    app.run(debug=True)