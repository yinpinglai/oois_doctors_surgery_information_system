
import jwt
import datetime
from typing import Union, Dict, Any
from sqlalchemy.sql import func

from .. import db, flask_bcrypt
from ..config import key
from .json_serializable import JSONSerializable
from app.main.util.datetime import DateTimeUtil
from app.main.model.blacklist import BlacklistToken
from app.main.enum.position_type import PositionType


@JSONSerializable.register
class User(db.Model):
    ''' User Model for storing user related details '''
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100))
    name = db.Column(db.String(255), unique=True, nullable=False)
    employee_number = db.Column(db.String(255), unique=True, nullable=False)
    position = db.Column(db.String(1), default=PositionType.staff.value)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    appointments = db.relationship('Appointment')
    registered_on = db.Column(db.DateTime, nullable=False, default=func.now())
    public_id = db.Column(db.String(100), nullable=False, unique=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id: int) -> bytes:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def serialize(self) -> Dict[str, Any]:
        '''
        Serializes the object instance to the JSON standard format

        :return serialized_dictionary - The serialized JSON dictionary
        '''
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'employee_number': self.employee_number,
            'position': self.position,
            'admin': self.admin,
            'appointments': self.appointments,
            'registered_on': DateTimeUtil.serialize_datetime_object(self.registered_on),
            'public_id': self.public_id,
        }

    def __str__(self):
        return f"<User '{self.name}' and user's position is {self.position}>"

    def __repr__(self):
        return f"""
            User: (
				id: {self.id},
                name: {self.name},
                employee_number: {self.employee_number},
                position: {self.position},
                admin: {self.admin},
                appointments: {repr(self.appointments)},
            )
        """
