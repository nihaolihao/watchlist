from flask import render_template
from watchlist import app
from watchlist.models import User

@app.errorhandler(404)  # 定义404错误处理函数
def page_not_found(e):
    user = User.query.first()    # 取出第一个用户
    return render_template('errors/404.html'), 404  # 返回404页面