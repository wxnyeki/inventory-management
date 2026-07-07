from flask import Flask, jsonify
from flask_cors import CORS
from app.routes import init_routes
import os
import logging

def create_app(config_name=None):
    """Application factory"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config.get(config_name, config['default']))
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Enable CORS
    CORS(app)
    
    # Initialize routes
    init_routes(app)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'status': 'error', 'message': 'Bad request'}), 400
    
    return app
