from flask import Flask, send_from_directory
from flask_talisman import Talisman
import os
from .config import Config
from . import db
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='../../frontend/bridge-ui/build', static_url_path='/static')
app.config.from_object(Config)

db.init_app(app)
Migrate(app, db)

csp = {
    'default-src': [
        "'self'",
        'https://fonts.googleapis.com',  # Allow Google Fonts
        'https://fonts.gstatic.com',      # Allow Google Fonts
        'data:'                           # Allow inline images and fonts
    ],
    'script-src': [
        "'self'",
        "'unsafe-inline'",                # Allow inline scripts for development
    ],
    'style-src': [
        "'self'",
        "'unsafe-inline'",                # Allow inline styles (CSS-in-JS)
        'https://fonts.googleapis.com'
    ],
}

# Enforce HTTPS if SSL is enabled
if app.config.get('ENABLE_SSL'):
    Talisman(app, content_security_policy=csp)

# Ensure API routes are handled first
from .routes import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')  # Prefix all API routes with /api

# Serve React app for non-API routes
@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_react_files(path):
    return send_from_directory(app.static_folder, path)

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    if app.config.get('ENABLE_SSL'):
        cert_file = os.getenv('SSL_CERT_FILE', 'backend/api/Certs/localhost.pem')
        key_file = os.getenv('SSL_KEY_FILE', 'backend/api/Certs/localhost-key.pem')
        app.run(host='0.0.0.0', port=5000, ssl_context=(cert_file, key_file))
    else:
        app.run(host='0.0.0.0', port=5000)
