import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "storyDb"
password = 'bara1414'
database_path = "postgres://{}:{}@{}/{}".format('postgres', password, 'localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Author(db.Model):

    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    age = Column(Integer)
    user_id = Column(String)
    stories = db.relationship('Story', backref='author')

    def __init__(self, fname, lname, age, user_id):
        self.fname = fname
        self.lname = lname
        self.age = age
        self.user_id = user_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'first_name': self.fname,
            'last_name': self.lname,
            'age': self.age,
            'user_id': self.user_id
        }


class Story(db.Model):

    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(String)
    category = Column(String)
    content = Column(String)
    author_id = Column(Integer, db.ForeignKey('author.id'))

    def __init__(self, title, type, category, content, author):
        self.title = title
        self.type = type
        self.category = category
        self.content = content
        self.author_id = author

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'category': self.category,
            'content': self.content,
            'author': self.author_id
        }