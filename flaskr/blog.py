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
    post = get_post(id, check_author=False)
    createlikes(id)  # 显示正文时初始化likes数据
    likes = get_likes(id)
    return render_template('blog/details.html', post=post, likes=likes)


# 获取like数据
def get_likes(id):
    datas = get_db().execute(
        ('select like,dislike from likes '
         'join post on likes.post_id=post.id '
         'where post.id= ?'),
        (id,)
    ).fetchone()
    return datas


# 建立likes数据
def createlikes(id):
    id = id
    db = get_db().execute(
        ('SELECT l.id FROM likes l '
         'JOIN post p ON l.post_id = p.id '
         'WHERE p.id = ?'),
        (id,)
    ).fetchone()
    if not db:
        db = get_db()
        db.execute(
            'INSERT INTO likes (like,dislike,post_id) VALUES ( ?, ?, ?)',
            (0, 0, id)
        )
        db.commit()
    return id


# 更新喜欢帖子数据
@bp.route('/<int:id>/like', methods=('GET',))
def updatelike(id):
    post = get_post(id, check_author=False)
    likes = get_likes(id)
    like = likes['like']
    like += 1
    db = get_db()
    db.execute(
        'UPDATE likes SET like = ? WHERE post_id = ?',
        (like, id)
    )
    db.commit()
    return render_template('blog/details.html', post=post, likes=get_likes(id))


# 更新不喜欢帖子数据
@bp.route('/<int:id>/dislike', methods=('GET',))
def updatedislike(id):
    post = get_post(id, check_author=False)
    likes = get_likes(id)
    dislike = likes['dislike']
    dislike += 1
    db = get_db()
    db.execute(
        'UPDATE likes SET dislike = ? WHERE post_id = ?',
        (dislike, id)
    )
    db.commit()
    return render_template('blog/details.html', post=post, likes=get_likes(id))


# 显示要评论的帖子标题和现有评论数,评论内容
@bp.route('/<int:id>/comments')
def get_comments(id):
    post = get_post(id, check_author=False)
    numcomment = get_db().execute(
        ('select sum(comments.id) as num from comments '
         'join post on comments.post_id=post.id '
         'where post.id= ?'),
        (id,)
    ).fetchone()
    if not numcomment:
        comments = get_db().execute(
        ('select c.id, c.post_id, c.parent_id, c.created, c.user, c.email, c.comments from comments c '
         'join post p on c.post_id=p.id '
         'where post.id= ?'),
        (id,)
    ).fetchone()
        return render_template(
        'blog/comments.html',
        post=post,
        numcomment=numcomment
        )
    return render_template(
        'blog/comments.html',
        post=post,
        numcomment=numcomment,
        comments=comments
        )


# 添加评论
@bp.route('/<int:id>/comments/add', methods=('GET', 'POST'))
def add_comment(id, parent_id=0):
    # post = get_post(id)

    if request.method == 'POST':
        parent_id = parent_id
        user = request.form['user']
        comment = request.form['comment']
        error = None

        if not user:
            error = '名称是必须的'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                ('UPDATE comments SET post_id = ?, parent_id = ? user = ? comments = ? WHERE id = ?'
                ),(id,parent_id,user,comment)
                )
            db.commit()
    return redirect(url_for('blog.details.html'))