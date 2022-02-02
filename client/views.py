from typing import Dict
from flask import Blueprint, render_template
from flask_login import login_required, current_user

def create_blueprint(config: Dict[str, str]) -> Blueprint:
    views = Blueprint('views', __name__)

    @views.route('/', methods=['GET'])
    @login_required
    def home():
        return render_template("home.html", user=current_user)

    return views

