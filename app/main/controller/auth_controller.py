from flask import request
from flask_restx import Resource

from typing import Dict, Tuple
from app.main.dto.auth import AuthDto
from app.main.service.auth_helper import Auth
from app.main.util.decorator import token_required

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self) -> Tuple[Dict[str, str], int]:
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)


@api.route('/user/info')
class UserInfoAPI(Resource):
    """
    User Information Resource
    """
    @token_required
    @api.doc('user info')
    def post(self) -> Tuple[Dict[str, str], int]:
        return Auth.get_logged_in_user(request)

