import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    DISCOVER_SHARED_FOLDERS_THREADS = 10
    SCAN_FILES_THREADS = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') \
                              or 'sqlite:///' + os.path.join(os.pardir, 'data/data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') \
                              or 'sqlite:///' + os.path.join(os.pardir, 'data/data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') \
                              or 'sqlite:///' + os.path.join(os.pardir, 'data/data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}