__author__ = 'yawen'

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    domain = db.Column(db.String(64))
    discovered_time = db.Column(db.DateTime(), default=datetime.utcnow)


class SharedFolder(db.Model):
    __tablename__ = 'folders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    machine = db.Column(db.String(64))
    discovered_time = db.Column(db.DateTime(), default=datetime.utcnow)


class SharedFile(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    machine = db.Column(db.String(64))
    path = db.Column(db.Text())
    size = db.Column(db.Integer)
    m_time = db.Column(db.DateTime(), default=datetime.utcnow)
    discovered_time = db.Column(db.DateTime(), default=datetime.utcnow)