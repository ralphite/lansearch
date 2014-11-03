import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    DISCOVER_SHARED_FOLDERS_THREADS = 20
    SCAN_FILES_THREADS = 10
    INDEX_NAME = 'file-index'
    INDEX_BODY = \
        {
            "mappings": {
                "_default_": {
                    "_source": {
                        "enabled": True
                    },
                    "_all": {
                        "analyzer": "default",
                        "enabled": True
                    },
                    "properties": {
                        "file": {
                            "dynamic": False,
                            "properties": {
                                "machine": {
                                    "type": "multi_field",
                                    "fields": {
                                        "machine": {"type": "string", "index": "analyzed"},
                                        "untouched": {"type": "string", "index": "not_analyzed"}
                                    }
                                },
                                "path": {
                                    "type": "multi_field",
                                    "fields": {
                                        "path": {"type": "string", "index": "analyzed"},
                                        "untouched": {"type": "string", "index": "not_analyzed"}
                                    }
                                },
                                "name": {
                                    "type": "multi_field",
                                    "fields": {
                                        "name": {"type": "string", "index": "analyzed"},
                                        "untouched": {"type": "string", "index": "not_analyzed"}
                                    }
                                },
                                "size": {
                                    "type": "multi_field",
                                    "fields": {
                                        "size": {"type": "string", "index": "analyzed"},
                                        "untouched": {"type": "string", "index": "not_analyzed"}
                                    }
                                },
                                "mtime": {
                                    "type": "multi_field",
                                    "fields": {
                                        "mtime": {"type": "string", "index": "analyzed"},
                                        "untouched": {"type": "string", "index": "not_analyzed"}
                                    }
                                },
                                "full": {
                                    "type": "multi_field",
                                    "fields": {
                                        "full": {"type": "string", "index": "analyzed"},
                                        "untouched": {"type": "string", "index": "not_analyzed"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

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