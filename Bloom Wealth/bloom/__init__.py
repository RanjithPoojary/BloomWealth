from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
scheduler = BackgroundScheduler()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from bloom.routes import auth, portfolio
    app.register_blueprint(auth.bp)
    app.register_blueprint(portfolio.bp)

    scheduler.start()

    return app