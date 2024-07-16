from flask import Flask, send_from_directory
from .config import Config
from . import db, init_app
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__, static_folder='../bridgeui/build', static_url_path='/')
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    from .routes import bp as api_bp
    app.register_blueprint(api_bp)

    @app.route('/')
    def serve():
        return send_from_directory(app.static_folder, 'index.html')

    @app.errorhandler(404)
    def not_found(e):
        return send_from_directory(app.static_folder, 'index.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
