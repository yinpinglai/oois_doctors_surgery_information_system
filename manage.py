import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db

from client import start_client_app


config_name = os.getenv('APP_ENVIRONMENT') or 'dev'

app = create_app(config_name)
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run_server():
    app.run()


@manager.command
def run_client():
    start_client_app(config_name)


@manager.command
def test_server():
    """Runs the server side's unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def test_client():
    """Runs the client side's unit tests"""
    tests = unittest.TestLoader().discover('client/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
