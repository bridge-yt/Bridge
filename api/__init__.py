from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    from flask import Flask
    from flask_talisman import Talisman
    from flask_migrate import Migrate
    from .config import Config

    app = Flask(__name__)
    app.config.from_object(Config)

    Talisman(app)
    db.init_app(app)
    Migrate(app, db)

    from .routes import bp as api_bp
    app.register_blueprint(api_bp)

    return app
