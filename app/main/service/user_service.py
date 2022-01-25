import uuid
import datetime

from app.main import db
from app.main.model.user import User
from app.main.util.response import produce_common_response_dict
from typing import Dict, Tuple


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            name=data['name'],
            employee_number=data['employee_number'],
            position=data['position'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow(),
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = produce_common_response_dict(
            is_success=False,
            message='User already exists. Please Log in.',
        )
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def generate_token(user: User) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = produce_common_response_dict(
            is_success=True,
            message='Successfully registered.',
            payload={
                'id': user.public_id,
                'Authorization': auth_token.decode(),
            },
        )
        return response_object, 201
    except Exception as e:
        print(e)
        response_object = produce_common_response_dict(
            is_success=False,
            message='Some error occurred. Please try again.',
        )
        return response_object, 401


def save_changes(data: User) -> None:
    db.session.add(data)
    db.session.commit()

