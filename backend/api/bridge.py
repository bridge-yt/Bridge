import os
import ssl

from flask import Flask, send_from_directory, render_template
from .config import Config
from . import db
from flask_migrate import Migrate
from flask_talisman import Talisman
from dotenv import load_dotenv  # Automatically load environment variables

def create_app():
    # Automatically load environment variables from .env file
    load_dotenv()

    # Create the Flask application instance
    app = Flask(__name__, static_folder='../../frontend/bridge-ui/build', static_url_path='/static')
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    # SSL Configuration - Talisman to enforce HTTPS and secure headers
    if app.config.get('ENABLE_SSL'):
        Talisman(app, force_https=True)  # Force HTTPS on all requests

        # Ensure the SSL certificate and key paths are available
        cert_file = app.config.get('SSL_CERT_FILE')
        key_file = app.config.get('SSL_KEY_FILE')

        # Ensure the certificate and key are present
        if not (cert_file and key_file and os.path.exists(cert_file) and os.path.exists(key_file)):
            raise ValueError("SSL is enabled but the certificate or key file is missing or incorrect.")
    else:
        # If SSL is not enabled, raise an error to prevent running without SSL
        raise ValueError("SSL is required but not enabled.")

    # Register blueprints and routes
    from .routes import bp as api_bp
    app.register_blueprint(api_bp)

    @app.route('/')
    def serve():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static_files(path):
        return send_from_directory(app.static_folder, path)

    @app.errorhandler(404)
    def not_found(e):
        return send_from_directory(app.static_folder, 'index.html')

    with app.app_context():
        db.create_all()  # Ensure the database tables are created

    return app

app = create_app()

if __name__ == '__main__':
    # Check if SSL is enabled
    if app.config.get('ENABLE_SSL'):
        cert_file = app.config.get('SSL_CERT_FILE')
        key_file = app.config.get('SSL_KEY_FILE')
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(cert_file, key_file)

        # Run Flask with SSL context
        if cert_file and key_file and os.path.exists(cert_file) and os.path.exists(key_file):
            app.run(host='0.0.0.0', port=5000, ssl_context=(cert_file, key_file))
        else:
            raise RuntimeError("SSL certificates are not found or invalid.")
    else:
        # If SSL is not enabled, raise an error to prevent running without SSL
        raise ValueError("SSL must be enabled to run this application.")
