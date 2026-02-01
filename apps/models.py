# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Projects(db.Model):

    __tablename__ = 'Projects'

    id = db.Column(db.Integer, primary_key=True)

    #__Projects_FIELDS__
    project_name = db.Column(db.Text, nullable=True)
    gitlab_project_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    gitlab_project_token = db.Column(db.Text, nullable=True)
    custom_value1_name = db.Column(db.Text, nullable=True)
    custom_value2_value = db.Column(db.Text, nullable=True)
    enabled = db.Column(db.Boolean, nullable=True)

    #__Projects_FIELDS__END

    def __init__(self, **kwargs):
        super(Projects, self).__init__(**kwargs)


class Roles(db.Model):

    __tablename__ = 'Roles'

    id = db.Column(db.Integer, primary_key=True)

    #__Roles_FIELDS__
    role_name = db.Column(db.Text, nullable=True)
    role_description = db.Column(db.Text, nullable=True)
    enabled = db.Column(db.Boolean, nullable=True)

    #__Roles_FIELDS__END

    def __init__(self, **kwargs):
        super(Roles, self).__init__(**kwargs)


class Users(db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)

    #__Users_FIELDS__
    username = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=True)
    role_id = db.Column(db.Integer, nullable=True)
    account_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    account_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    enabled = db.Column(db.Boolean, nullable=True)

    #__Users_FIELDS__END

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)


class Engagements(db.Model):

    __tablename__ = 'Engagements'

    id = db.Column(db.Integer, primary_key=True)

    #__Engagements_FIELDS__
    engagement_start = db.Column(db.DateTime, default=db.func.current_timestamp())
    enagagement_end = db.Column(db.DateTime, default=db.func.current_timestamp())
    archived = db.Column(db.Boolean, nullable=True)

    #__Engagements_FIELDS__END

    def __init__(self, **kwargs):
        super(Engagements, self).__init__(**kwargs)



#__MODELS__END
