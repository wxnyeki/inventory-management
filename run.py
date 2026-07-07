from app import create_app
import os

if __name__ == '__main__':
    # Get environment
    env = os.getenv('FLASK_ENV', 'development')
    
    # Create app
    app = create_app(env)
    
    # Run server
    port = int(os.getenv('PORT', 5000))
    debug = env == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
