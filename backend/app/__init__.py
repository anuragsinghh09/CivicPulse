from flask import Flask

from .config import Config
from .extensions import db, login_manager
from .models import User
from .routes import admin_bp, auth_bp, citizen_bp, public_bp


def create_app(config_overrides=None):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    if config_overrides:
        app.config.from_mapping(config_overrides)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(citizen_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app
