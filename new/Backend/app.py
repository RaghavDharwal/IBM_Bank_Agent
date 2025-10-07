
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
import logging
from logging.handlers import RotatingFileHandler

from models import db
from routes import routes

app = Flask(__name__)

# Environment-based configuration
ENV = os.environ.get('FLASK_ENV', 'development')
DEBUG = ENV == 'development'

# Security Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Database Configuration
if ENV == 'production':
    # Use PostgreSQL in production
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Use SQLite for development
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///bank_loan_portal.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 300,
    'pool_pre_ping': True
}

# CORS Configuration
if ENV == 'production':
    # Allow your frontend domain in production
    frontend_url = os.environ.get('FRONTEND_URL', 'https://your-frontend-domain.onrender.com')
    CORS(app, origins=[frontend_url, "http://localhost:3000", "http://localhost:3001"])
else:
    # Allow localhost in development
    CORS(app, origins=["http://localhost:3000", "http://localhost:3001"])

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Logging Configuration
if ENV == 'production':
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/bank_portal.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Bank Portal startup')

# Health check endpoint
@app.route('/health')
@app.route('/api/health')
def health_check():
    try:
        # Test database connection
        from sqlalchemy import text
        with db.engine.connect() as connection:
            connection.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'environment': ENV,
            'database': 'connected'
        }), 200
    except Exception as e:
        app.logger.error(f'Health check failed: {str(e)}')
        return jsonify({
            'status': 'unhealthy',
            'environment': ENV,
            'database': 'disconnected',
            'error': str(e)
        }), 500

# Register routes blueprint
app.register_blueprint(routes)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server Error: {error}')
    return jsonify({'error': 'Internal server error'}), 500

# Initialize database
def create_tables():
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables created successfully!")
            print("Database tables created successfully!")
        except Exception as e:
            app.logger.error(f"Failed to create database tables: {str(e)}")
            print(f"Failed to create database tables: {str(e)}")

if __name__ == '__main__':
    create_tables()
    print("Starting Bank Loan Portal Backend...")
    print(f"Environment: {ENV}")
    print("API Documentation:")
    print("- POST /api/auth/register - Register new user")
    print("- POST /api/auth/login - User login")
    print("- POST /api/loan-applications - Submit loan application (requires auth)")
    print("- GET /api/loan-applications - Get user's applications (requires auth)")
    print("- GET /api/loan-applications/<id> - Get specific application (requires auth)")
    print("- GET /api/health - Health check")
    
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=DEBUG, host='0.0.0.0', port=port)
else:
    # This is for production deployment (gunicorn)
    create_tables()
