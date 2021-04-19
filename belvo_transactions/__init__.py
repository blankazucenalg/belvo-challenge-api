import os

from flask import Flask

from belvo_transactions import connection
from belvo_transactions.resources import user, transaction


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'belvo_transactions.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def main():
        return 'It works!'

    connection.init_app(app)
    app.register_blueprint(user.bp)
    app.register_blueprint(transaction.bp)

    return app
