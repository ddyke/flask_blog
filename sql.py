# create a database for the blog

import sqlite3

with sqlite3.connect("blog.db") as conn:
    c = conn.cursor()

    # create table "post" which has two fields "title" and "post"
    c.execute("DROP TABLE if exists posts")
    c.execute("CREATE TABLE posts(title TEXT, post TEXT)")

    # insert dummy data into the tabe
    c.execute('INSERT INTO posts VALUES("Good", "I\'m good.")')
    c.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')
    c.execute('INSERT INTO posts VALUES("Excellent", "I\'m excellent.")')
    c.execute('INSERT INTO posts VALUES("Okay", "I\'m Okay.")')





