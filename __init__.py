from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
database = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="Templates", static_folder="static")

    app.config["SECRET_KEY"] = "secret-key-goes-here"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"

    database.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .weather import weather as weather_blueprint

    app.register_blueprint(weather_blueprint)

    return app
