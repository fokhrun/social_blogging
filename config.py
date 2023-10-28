import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "passcode"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")


def get_config(default_choice="development"):
    return {
        "development": DevelopmentConfig,
    }
