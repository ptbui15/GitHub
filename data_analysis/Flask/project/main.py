from flask import Blueprint, render_template
from . import db
from .models import Scores
#import celery
from flask_login import login_required, current_user
from flask import current_app

main = Blueprint('main', __name__)

   

@main.route('/')
def index():
    return render_template('index.html')

"""
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
    """


# test dashboard
@main.route('/profile')
@login_required
def profile():
    return render_template(
        "index.jinja2",
        title="Plotly Dash Flask Tutorial",
        description="Embed Plotly Dash into your Flask applications.",
        template="home-template",
        body="This is a homepage served with Flask.",
    )
