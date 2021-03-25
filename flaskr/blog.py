from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


# 索引视图
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        ('SELECT p.id, title, body, created, author_id, username FROM '
         'post p JOIN user u ON p.author_id = u.id ORDER BY created DESC')
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


# 创建视图
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = '标题是必须的-Title isrequired.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title,body,author_id) VALUES ( ?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


# 取得帖子函数
def get_post(id, check_author=True):
    post = get_db().execute(
        ('SELECT p.id,title,body,created,author_id,username FROM post p '
         'JOIN user u ON p.author_id = u.id WHERE p.id = ?'),
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id{0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


# 更新帖子视图
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = '标题是必须的'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


# 删除帖子
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


# 显示帖子正文
@bp.route('/<int:id>/details')
def details(id):
    # return "test"
    post = get_post(id, check_author=False)
    return render_template('blog/details.html',post=post)


# 显示喜欢或不喜欢帖子
@bp.route('/<int:id>/like')
def likeindex(id):
    # post = get_post(id, check_author=False)
    posts = get_db()
    posts.execute(
        ('select like,dislike from like '
         'join post on like.post_id=post.id '
         'where post.id= ?'),
        (id,)
    ).fetchone()
    return print('print:',posts)
