DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS likes;

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

create table likes (
    id integer primary key AUTOINCREMENT,
    post_id integer not null,
    created timestamp not null default CURRENT_TIMESTAMP,
    like integer not null default 0,
    dislike integer not null default 0,
    foreign key (post_id) REFERENCES post(id)
);