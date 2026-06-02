#Application factory 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.employees import employees_bp
    from app.routes.payroll import payroll_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(payroll_bp, url_prefix='/payroll')

    # Create tables
    with app.app_context():
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    """Create default admin user if none exists."""
    from app.models.users import User
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@hrpayroll.com',
            role='admin',
            full_name='System Administrator'
        )
        admin.set_password('Admin@1234')
        db.session.add(admin)
        db.session.commit()
    
    
   