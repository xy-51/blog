from flask import render_template, redirect, url_for, g, flash, request, session
from app import app
from forms import LoginForm, ArticleForm

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    thenick = None
    thepasswd = None
    session['thenick'] = None
#    cur = g.db.execute('select nickname from users order by id desc')
#    for row in g.db.fetchall():
#        if 'abc' in row:
#            print 'yes' 
#        else:
#            print 'no'
    if form.validate_on_submit():
        thenick = form.nickname.data
        form.nickname.data = ''
        thepasswd = form.password.data
        form.password.data = ''
        cur = g.db.execute('select password from users where nickname=\'%s\''%thenick)
        password = g.db.fetchone()
        if password:
            print 'password', password
            if thepasswd in password:
                session['thenick'] = thenick
                return redirect(url_for('home'))
            else:
                flash('Invalid password')
        else:
            flash('Invalid nickname')
    return render_template('index.html',
                           form=form)

@app.route('/blog-home')
def home():
    if session['thenick']:
        cur = g.db.execute('select title from articles where username=\'%s\''%(session['thenick']))
        articles = g.db.fetchall()
        return render_template('home.html',
                                nickname = session.get('thenick'),
                                articles = articles)
    else:
        flash('You were not logged in. Please sign in first.')
        return redirect(url_for('index'))
        
@app.route('/logout')
def logout():
    if session['thenick']:
        flash('You were logged out.')
        print 'yes'
        return redirect(url_for('index'))
    else:
        flash('You were not logged in. Please sign in first.')
        return redirect(url_for('index'))
        
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        session['thenick'] = request.form['nickname']
        cur = g.db.execute('insert into users (nickname, password) values(\'%s\', \'%s\')'%(request.form['nickname'],request.form['password']))
        g.conn.commit()
        return redirect(url_for('home'))
        #thenick = form.nickname.data
        #thepasswd = form.nickname.data
    return render_template('register.html', form=form)

@app.route('/add', methods = ['POST', 'GET'])
def add():
    if session['thenick']:
        Aform = ArticleForm()
        if Aform.validate_on_submit:
            if Aform.title.data and Aform.text.data:
                cur = g.db.execute('insert into articles (title, text, username) values(\'%s\', \'%s\', \'%s\')'%(Aform.title.data, Aform.text.data, session.get('thenick')))
                g.conn.commit()
                flash('New article is created.')
            else:
                flash('Title and text should not be empty.')
        return render_template('add.html',
                            nickname = session['thenick'],
                            Aform = Aform)
    else:
        flash('You were not logged in. Please sign in first.')
        return redirect(url_for('index'))

@app.route('/article', methods = ['POST', 'GET'])
def article():
    return render_template('article.html')
