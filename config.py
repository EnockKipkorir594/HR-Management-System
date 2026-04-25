import os
'''secret_ key --> generate random hex characters
run --> python3 -c 'import secrets; print(secrets.token_hex())'
'''
class Config(object):
    #----core flask settings----------------------
    
    #The secret key
    SECRET_KEY = os.getenv("SECRET_KEY","dev_secret_key_change_in_production")
    
    #----database settings------------------------
 
    #database URI
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///hr_system.db")
    #SQLAchemy has a feature that track every modification to a model onject
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #when True Flask-SQALchemy prints every query it generates to the terminal
    SQLALCHEMY_ECHO = False
    
    #--------session setings --------------------------
    
    #When True the session cookie cannot be accessed by Javascript running in the browser
    SESSION_COOKIE_HTTPONLY = True
    #Controls when the browser sends session cookie with cross-site requests.
    #Lax means the cookie is sent on normal navigation but not on cross-site POST requests
    SESSION_COOKIE_SAMESITE = "Lax"
    #How many seconds session stays alive without activity
    PERMANENT_SESSION_LIFETIME = int(os.getenv("SESSION_LIFETIME_SECONDS", 3600))
    
    #--------Security settings------------------------------------
    
    #Enabled CSRF protection if you are using Flask-WTF for form handling
    WTF_CSRF_ENABLED = True
    
    #--------Application settings--------------------------------
    
    #The currency used in payslip generation and reports
    PAYROLL_CURRENCY = os.getenv("PAYROLL_CURRENCY", "KES")
    #Maximum size of HTTP request bodies in bytes: 16 * 1024 * 1024 = 16MB
    #Prevents attackers from sending enormous request bodies that crash the server
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    #Appears on generated payslips and HR reports
    COMPANY_NAME = os.getenv("COMPANY_NAME", "Your-company-name")
    
    
#Production environment
class ProductionConfig(Config):
    DEBUG = False
    DB_SERVER = '192.168.1.32'
    
#Development environmet where debugging is true   
class DevelopmentConfig(Config):
    DEBUG = True
    DB_SERVER ='localhost'
    
#Testing environment    
class TestingConfig(Config):
    DB_SERVER = 'localhost'
    DATABASE_URI = 'sqlite:///:memory:'
    
    
    
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
    
}