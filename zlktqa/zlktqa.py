from flask import Flask,render_template,request,redirect,url_for,session,g
from exts import db
from models import User,Question,Comment
import config
from decorators import login_required
from sqlalchemy import or_
#过期时间,通过cookie实现的
from datetime import timedelta



app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
app.permanent_session_lifetime = timedelta(days=31)

@app.route('/')
def index():
    context = {
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['userid'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后登录'

@app.route('/loginout/')
def loginout():
    session.pop('userid')
    #del session['userid']
    #session.clear()
    return redirect(url_for('login'))


@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
def detail(question_id):
    question = Question.query.filter(Question.id ==question_id).first()
    return render_template('detail.html',question =question)

@app.route('/add_comment/',methods=['POST'])
@login_required
def add_comment():
    content = request.form.get('content')
    question_id =request.form.get('question_id')
    comment = Comment(content=content)
    comment.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    comment.question = question
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail',question_id = question_id))



@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #手机号验证，如果被注册了，就不能再注册了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return render_template('regist.html',msg = u'该手机号码已被注册，请更换手机号码')
            #return u'该手机号码已被注册，请更换手机号码'
        else:
            if password1!=password2:
                return render_template('regist.html', meg=u'两次密码不相等，请核对后再填写')
                #return  u'两次密码不相等，请核对后再填写'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/search/')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q)))
    return render_template('index.html', questions=questions)

@app.before_request
def my_before_request():
    userid = session.get('userid')
    if userid:
        user = User.query.filter(User.id==userid).first()
        if user:
            g.user = user

@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}


if __name__ == '__main__':
    app.run()










