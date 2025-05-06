![watch]()
## Installation
[](https://github.com/nihaolihao/watchlist#installation)
clone:

```
$ git clone https://github.com/nihaolihao/watchlist.git
$ cd watchlist
```

create & active virtual enviroment then install dependencies:

```
$ pipenv install      # 安装虚拟环境
$ pipenv shell        # 启动虚拟环境
(env)$ flask initdb   # 生成数据库文件
(env)$ flask admin    # 创建管理员
示例 flask admin --username admin --password admin
```

generate fake data then run:

```
(env) $ flask forge   # 生成测试数据
(env) $ flask run     # 启动flask服务
* Running on http://127.0.0.1:5000/
```

##
