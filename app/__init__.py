from flask import Flask 
from app.extensions import db

def create_app(test_config=None):
    
    app = Flask(__name__ , instance_relative_config=True)
    
    app.config['SQALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
    
    db.init_app(app)
    
    
   