DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS comments;

CREATE TABLE user (
    id INTEGER PRIMARY  KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE likes (
    id INTEGER primary key AUTOINCREMENT,
    post_id INTEGER not null,
    created TIMESTAMP not null default CURRENT_TIMESTAMP,
    like INTEGER not null default 0,
    dislike INTEGER not null default 0,
    foreign key (post_id) REFERENCES post(id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    parent_id INTEGER NOT NULL,
    created TIMESTAMP not null default CURRENT_TIMESTAMP,
    user TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    comments TEXT UPDATE NOT NULL,
    FOREIGN KEY (post_id) REFERENCES post(id)
);