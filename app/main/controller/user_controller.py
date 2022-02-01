from flask import request
from flask_restx import Resource, reqparse

from app.main.dto.user import UserDto
from app.main.util.decorator import token_required, admin_token_required
from ..service.user_service import save_new_user, get_all_users, get_a_user
from typing import Dict, Tuple

api = UserDto.api
_user = UserDto.user
_user_list_api = UserDto.user_list_api
_user_details_api = UserDto.user_details_api
_user_changed_response = UserDto.user_changed_response


@api.route('/')
class UserList(Resource):

    @admin_token_required
    @api.doc('Gets the list of user')
    @api.marshal_list_with(_user_list_api)
    def get(self):
        """List all registered users"""
        parser = reqparse.RequestParser()
        parser.add_argument('position', action='append', help='User\'s position.')
        params = parser.parse_args()
        return get_all_users(params)

    @admin_token_required
    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.', _user_changed_response)
    @api.doc(
        'Creates a new user',
        responses={
            401: 'Some error occurred. Please try again.',
            409: 'User already exists. Please Log in.',
        },
    )
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):

    @token_required
    @api.doc('Gets an user')
    @api.marshal_with(_user_details_api)
    def get(self, public_id):
        """Gets a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user

