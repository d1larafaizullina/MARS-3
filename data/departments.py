"""
По мере роста поселения колонистов на Марсе возникает необходимость объединить всех специалистов в департаменты
 и хранить информацию о них в отдельной модели.
  Поэтому нам нужно расширить базу данных колонистов еще одной моделью Department с полями:

id
title (String)
chief (Integer)
members (list of id`s)
email (String)
"""
import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):

    __tablename__ = 'departments'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    chief = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey("users.id"))
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relation('User')
