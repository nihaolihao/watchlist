Installation
clone:

$ git clone https://github.com/helloflask/watchlist.git
$ cd watchlist
create & active virtual enviroment then install dependencies:

$ python3 -m venv env  # use `python ...` on Windows
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
(env) $ pip install -r requirements.txt
generate fake data then run:

(env) $ flask forge
(env) $ flask run
* Running on http://127.0.0.1:5000/
