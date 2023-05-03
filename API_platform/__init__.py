import os

from flask import Flask
from flask_qrcode import QRcode

app = Flask(__name__, instance_relative_config=True)
QRcode(app)
app.config.from_mapping(
    SECRET_KEY="dev",
    DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
)

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
