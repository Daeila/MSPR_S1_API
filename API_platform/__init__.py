import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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

    import API_platform.api_get as api_get

    app.register_blueprint(api_get.bp)
    #
    # import API_platform.api_post as api_post
    #
    # app.register_blueprint(api_post.bp)
    #
    # import API_platform.api_update as api_update
    #
    # app.register_blueprint(api_update.bp)
    #
    # import API_platform.api_delete as api_delete
    #
    # app.register_blueprint(api_delete.bp)

    return app
