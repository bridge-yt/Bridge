from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///Helm-bridge-plugin.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    DEBUG = os.getenv('FLASK_DEBUG', True)
    ENABLE_SSL = os.getenv('ENABLE_SSL', 'False').lower() in ['true', '1', 't']

    # Paths to SSL certificate and key (loaded from .env)
    SSL_CERT_FILE = os.getenv('SSL_CERT_FILE', './Certs/default-cert.pem')
    SSL_KEY_FILE = os.getenv('SSL_KEY_FILE', './Certs/default-key.pem')
