from flask import Flask
from src.constants.const import *
from src.authentication.auth import auth
from src.video.video import video

def create_app(test_config = None):
    app = Flask(__name__,instance_relative_config=True)
    if(test_config is None):
        app.config.from_mapping(
            SECRET_KEY = SECRET_KEY
        )

    else :
        app.config.from_mapping(test_config)

    app.register_blueprint(auth)
    app.register_blueprint(video)

    @app.get('/')
    def index():
        return "Hello world!"

    return app