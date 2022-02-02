from flask import Flask
from flask_login import LoginManager

from client.service.auth_service import AuthService
from .views import create_blueprint as create_views_blueprint
from .auth import create_blueprint as create_auth_blueprint
from .config import config_by_name


def start_client_app(config_name: str) -> None:
    config = config_by_name[config_name]
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.SECRET_KEY

    app.register_blueprint(create_views_blueprint(config), url_prefix='/')
    app.register_blueprint(create_auth_blueprint(config), url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    auth_service = AuthService(config)

    @login_manager.user_loader
    def load_user(token):
        employee = auth_service.get_user_info(token)
        return employee

    return app

