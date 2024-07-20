import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///Helm-bridge-plugin.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    DEBUG = os.getenv('FLASK_DEBUG', True)
    ENABLE_SSL = os.getenv('ENABLE_SSL', 'False').lower() in ['true', '1', 't']

    @staticmethod
    def validate_ssl_config():
        if Config.ENABLE_SSL:
            if not Config.SQLALCHEMY_DATABASE_URI.startswith('postgresql://'):
                raise ValueError("SSL is enabled, but the database URL is not using SSL.")
