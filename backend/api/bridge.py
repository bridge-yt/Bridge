from flask import Flask, send_from_directory, render_template
from .config import Config
from . import db
from flask_migrate import Migrate
from flask_talisman import Talisman

def create_app():
    app = Flask(__name__, static_folder='../../frontend/bridge-ui/build', static_url_path='/static')
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    if app.config.get('ENABLE_SSL'):
        Talisman(app)

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
    if app.config.get('ENABLE_SSL'):
        app.run(host='0.0.0.0', port=5000, ssl_context=('../Certs/cert.pem', '../Certs/key.pem'))
    else:
        app.run(host='0.0.0.0', port=5000)
