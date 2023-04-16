import os

from flask import Flask
from flask_qrcode import QRcode


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    QRcode(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    import API_platform.db as db

    db.init_app(app)

    import API_platform.api_get as api_get

    app.register_blueprint(api_get.bp)

    import API_platform.authenticator as auth

    app.register_blueprint(auth.bp)

    return app
