from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dash import Dash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask_login import LoginManager
from flask_login import login_required, current_user
from .plotlydash.dashboard import init_dashboard



# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Setup configuration
    app.config['SECRET_KEY'] = 'ten10isp'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Init databaes
    db.init_app(app)

    # Init dashboard
    app = init_dashboard(app)

    #from .celery_utils import make_celery

    #app.config.update(CELERY_BROKER_URL = 'pyamqp://localhost//')
    #app.config.update(CELERY_RESULT_BACKEND = 'pyamqp://localhost//')

    #celery = make_celery(app)

#   @celery.task()
 #   def add_together(a,b):
 #       return a+b


    # Enable session login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app