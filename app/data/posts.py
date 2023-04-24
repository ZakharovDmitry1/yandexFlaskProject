import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Posts(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    image = sqlalchemy.Column(sqlalchemy.String, default='images_cats/default_cat.png')
    cost = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    title = sqlalchemy.Column(sqlalchemy.String, default='')
    user = orm.relationship('User')


