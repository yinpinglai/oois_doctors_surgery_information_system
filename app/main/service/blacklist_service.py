from app.main import db

from app.main.model.blacklist import BlacklistToken
from app.main.util.response import produce_common_response_dict
from typing import Dict, Tuple


def save_token(token: str) -> Tuple[Dict[str, str], int]:
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = produce_common_response_dict(
            is_success=True,
            message='Successfully logged out.',
        )
        return response_object, 200
    except Exception as e:
        response_object = produce_common_response_dict(
            is_success=False,
            message=e,
        )
        return response_object, 200
