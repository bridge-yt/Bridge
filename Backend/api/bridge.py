from flask import Flask
from .config import Config
from flask_talisman import Talisman
from . import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Talisman(app)
    db.init_app(app)
    Migrate(app, db)

    from .routes import bp as api_bp
    app.register_blueprint(api_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')

git remote set-url origin https://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@github.com/bridge-yt/Bridge.git

git@github.com:bridge-yt/Bridge.git
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