from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app():
    from .bridge import create_app
    return create_app()