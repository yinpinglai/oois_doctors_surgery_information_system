from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from client.service.auth_service import AuthService


def create_blueprint(config):

    auth = Blueprint('auth', __name__)

    @auth.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            auth_service = AuthService(config)
            try:
                email = 'kris.lai@gmail.com'
                password = 'P@ssw0rd'
                is_success, token = auth_service.login(email, password)
                if is_success and token is not None:
                    employee = auth_service.get_user_info(token)
                    if employee:
                        flash('Logged in successfully!', category='success')
                        login_user(employee, remember=True)
                        return redirect(url_for('views.home'))
                    else:
                        flash('Email does not exist.', category='error')
                else:
                    flash('Email does not exist.', category='error')
            except Exception as e:
                print(e)
                flash(f'Login failed: {e}')

        return render_template("login.html", user=current_user)


    @auth.route('/logout')
    @login_required
    def logout():
        if current_user.access_token is not None:
            token = current_user.access_token
            auth_service = AuthService(config)
            try:
                is_success = auth_service.logout(token)
                if is_success:
                    flash('Logged out successfully!', category='success')
                    logout_user()
            except Exception as e:
                print(e)
                flash(f'Logout failed: {e}', category='error')
            finally:
                return redirect(url_for('auth.login'))

        return redirect(url_for('auth.login'))

    return auth

