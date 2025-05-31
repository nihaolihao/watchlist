from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    # return 'Welcome to My Watchlist!'

    return render_template('index.html',name=name,movies=movies)
# 定义虚拟数据

name = 'Li Hao'
movies = [
    {'title': 'The Shawshank Redemption', 'year': 1994},
    {'title': 'The Godfather', 'year': 1972},
    {'title': 'The Dark Knight', 'year': 2008},
    {'title': '12 Angry Men', 'year': 1957},
    {'title': 'Schindler\'s List', 'year': 1993},
    {'title': 'The Lord of the Rings: The Return of the King', 'year': 2003},
    {'title': 'Pulp Fiction', 'year': 1994},
    {'title': 'The Lord of the Rings: The Fellowship of the Ring', 'year': 2001},
    {'title': 'The Good, the Bad and the Ugly', 'year': 1966},
    {'title': 'Fight Club', 'year': 1999}
]