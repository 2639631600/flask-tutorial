import functools
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

bp = Blueprint('auth', __name__, url_prefix='/auth')

# 注册用户视图


class RegisterForm(FlaskForm):
    username_msg = '用户名是必须的-Username isrequired.'
    password_msg = '密码是必须的-Password is required.'
    username = StringField('Username', validators=[DataRequired(username_msg)])
    password = PasswordField('Password', validators=[
                             DataRequired(password_msg), Length(8, 128)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username_msg = '用户名是必须的-Username isrequired.'
    password_msg = '密码是必须的-Password is required.'
    username = StringField('Username', validators=[DataRequired(username_msg)])
    password = PasswordField('Password', validators=[
                             DataRequired(password_msg), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     db = get_db()
    #     error = None

    #     if not username:
    #         error = '用户名是必须的-Username isrequired.'
    #     elif not password:
    #         error = '密码是必须的-Password is required.'
    #     elif db.execute(
    #         'SELECT id FROM user WHERE username = ?', (username,)
    #     ).fetchone() is not None:
    #         error = '用户 {} 已经注册-already registered'.format(username)

    #     if error is None:
    #         db.execute(
    #             'INSERT INTO user (username,password) VALUES (?,?)',
    #             (username, generate_password_hash(password))
    #         )
    #         db.commit()
    #         return redirect(url_for('auth.login'))

    #     flash(error)
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        error = None
        db = get_db()
        if db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = '用户 {} 已经注册-already registered'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username,password) VALUES (?,?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html', form=form,)


# 登录视图
@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            error = '用户名错误-Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = '密码错误-Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     db = get_db()
    #     error = None
    #     user = db.execute(
    #         'SELECT * FROM user WHERE username = ?', (username,)
    #     ).fetchone()

    #     if user is None:
    #         error = '用户名错误-Incorrect username.'
    #     elif not check_password_hash(user['password'], password):
    #         error = '密码错误-Incorrect password.'

    #     if error is None:
    #         session.clear()
    #         session['user_id'] = user['id']
    #         return redirect(url_for('index'))

    #     flash(error)

    return render_template('auth/login.html', form=form)


# 在视图函数之前运行此函数，将登录的user 数据 保存到 g.user
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# 注销视图
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 在其他视图中验证用户是否已登录，这是一个装饰器
# 函数名是wrapped_view，不使用functools.wraps装饰器，_name__就会是这个名字。
def login_required(view):  # login_required 翻译意思是必须登录
    @functools.wraps(view)  # functools.warps 函数是为了在装饰器拷贝被装饰函数的__name__。
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
