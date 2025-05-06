from flask import render_template, flash, redirect, url_for, request
from watchlist.models import User, Movie
from flask_login import login_user, logout_user, login_required, current_user
from watchlist import app,db



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')  # 显示错误信息
            return redirect(url_for('login'))  # 重定向回登录页面
        
        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)  # 登录用户
            flash('Login success.')  # 显示成功信息
            return redirect(url_for('index'))  # 重定向回首页
        
        flash('Invalid username or password.')  # 显示错误信息
        return redirect(url_for('login'))  # 重定向回登录页面
    
    return render_template('login.html')  # 登录页面

@app.route('/logout')
@login_required
def logout():
    logout_user()  # 登出用户
    flash('Logout success.')  # 显示成功信息
    return redirect(url_for('index'))  # 重定向回登录页面


@app.route('/',methods=['GET','POST'])
@app.route('/index')
@app.route('/home')
def index():
    # return 'Welcome to My Watchlist!'
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('login'))  # 未登录则重定向到登录页面
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
    
    user = current_user
    movies = Movie.query.all()   # 取出所有电影
    return render_template('index.html',user=user,movies=movies)

@app.route('/delete/<int:movie_id>',methods=['POST'])
@login_required
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


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
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


@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')  # 显示错误信息
            return redirect(url_for('settings'))  # 重定向回设置页面
        
        current_user.name = name
        db.session.commit()
        flash('Settings updated.')  # 显示成功信息
        return redirect(url_for('index'))  # 重定向回首页
    return render_template('settings.html')  # 设置页面