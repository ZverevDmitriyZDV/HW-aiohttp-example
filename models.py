from datetime import datetime
from gino import Gino
from pydantic import BaseModel, validator
import re

db = Gino()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(), nullable=False)
    user_password = db.Column(db.String(), nullable=False)
    user_email = db.Column(db.String(), nullable=False, unique=True)

    _idx1 = db.Index('user_password_idx', 'user_password', unique=True)


class Adv(db.Model):
    __tablename__ = 'advertisment'

    id = db.Column(db.Integer(), primary_key=True)
    header = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.String(), default=datetime.today().strftime('%Y-%m-%d'))
    owner = db.Column(db.Integer, db.ForeignKey("user.id"))


class UserValidationModel(BaseModel):
    user_name: str
    user_password: str
    user_email: str

    @validator('user_email')
    def password_by_template(cls, v):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, v):
            raise ValueError('Invalid email')
        return v.title()


class AdvValidationModel(BaseModel):
    header: str
    description: str
    owner: int

