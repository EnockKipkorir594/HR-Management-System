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
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///hr_system_dev.db")
    #SQLAchemy has a feature that track every modification to a model object
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
    TESTING = False
    #In this case we use os.environ not os.getenv so the application fails if no secret
    #key is provided . Throws a Keyerror message.
    SECRET_KEY = os.environ("SECRET_KEY")
    #At this stage  SQL printing is set to false since attackers can 
    #SQL query to perform attacks like  SQL injection
    SQLALCHEMY_ECHO = False
    #Production uses HTTPS(for any secure applications)
    #Setting this to true means the browser session cokie is sent over encrypted
    #HTTPS connections
    SESSION_COOKIE_SECURE = True
    
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    
    #Validate required environment variables for production
    @classmethod
    def validate(cls):
        required = [
            "SECRET_KEY",
            "DATABASE_URL",
            "COMPANY_NAME"
        ]
        
        missing = [var for var in required if not os.getenv(var)]
        if missing:
            raise EnvironmentError(
                f"Mssing required environment variables {', '.join(missing)}"
            )
    
    
#Development environmet where debugging is true   
class DevelopmentConfig(Config):
    #Debug is set to True in development 
    #Shows detailed errors and tracebcks in the browser
    DEBUG = True
    
    TESTING = False
    #Development uses a separate sqlite database from production
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://hr_system_dev.db")
    #Set to true to prints all the query statements to determine what the ORM is doing
    SQLALCHEMY_ECHO = True
    #Set to False since dev environment uses HTTP not HTTPS so this must be False
    SESSION_COOKIE_SECURE = False 
    
#Testing environment    
class TestingConfig(Config):
    #Tells Flask it is in testing mode. Changes how flask handles errors 
    TESTING = True
    
    DEBUG = False
    #In-memory SQLite database.Create a new database when a new test session starts.
    #Destroyed when the tests are completed
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","sqlite:///:memory:")
    #Disable SQL printing during testing 
    SQLALCHEMY_ECHO = False
    #Tests run in an isolated environment with no real users so it is safe
    WTF_CSRF_ENABLED = False
    #Tests can run using HTTP since it has no real users hence no securit threats
    SESSION_COOKIE_HTTPONLY = False
    #Secret key is set only used for production
    SECRET_KEY = "test-secret-key-not-for-production"
    #Long session lifetime for tests (24hours) so sessions do not expire mid-test
    PERMANENT_SESSION_LIFETIME = os.getenv("SESSION_LIFETIME_SECONDS", 86400)
    
    
#-------configuration registry--------------------

#Maps string names to configuration classes
#The app factory uses this dictionary for configuration
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
    
}