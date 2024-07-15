import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///bridge.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    DEBUG = os.getenv('FLASK_DEBUG', False)
