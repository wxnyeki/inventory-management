import os
from datetime import timedelta

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    JSON_FILE = os.path.join(os.path.dirname(__file__), 'data', 'inventory.json')
    OPENFOODFACTS_API_URL = 'https://world.openfoodfacts.org/api/v0/product'
    OPENFOODFACTS_SEARCH_URL = 'https://world.openfoodfacts.org/cgi/search.pl'
    REQUEST_TIMEOUT = 10
    ITEMS_PER_PAGE = 50
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    JSON_FILE = os.path.join(os.path.dirname(__file__), 'data', 'test_inventory.json')

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
