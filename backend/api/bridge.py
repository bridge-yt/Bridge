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

# Enforce HTTPS if SSL is enabled
if app.config.get('ENABLE_SSL'):
    Talisman(app, force_https=True)

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
    cert_file = 'backend/api/Certs/localhost.pem'
    key_file = 'backend/api/Certs/localhost-key.pem'
    app.run(host='0.0.0.0', port=5000, ssl_context=(cert_file, key_file))
