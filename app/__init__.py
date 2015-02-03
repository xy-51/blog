from flask import Flask, g, request
import MySQLdb

#cofiguration
USENAME = 'root'
PASSWORD = ''
DATABASE = 'blog_information'
DEBUG = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

def connect_db():
    conn = MySQLdb.connect(host='localhost', user=USENAME, passwd=PASSWORD, charset='utf8')
    conn.select_db(DATABASE)
    return conn

@app.before_request
def before_request():
    g.conn = connect_db()
    g.db = g.conn.cursor()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    g.db.close()

from app import views



