from flask import Flask 
from app.extensions import db
from config import config

def create_app(config_class=None):
    
    app = Flask(__name__ , instance_relative_config=True)
    #Load settings from config class
    app.config.from_object(config)
    #loading database configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
    #connecting database object to the app settings
    db.init_app(app)
    
    return app 
    
    
   