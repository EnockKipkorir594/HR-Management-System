
'''secret_ key --> generate random hex characters
run --> python3 -c 'import secrets; print(secrets.token_hex())'
'''
class Config(object):
    #for production 
    TESTING = False 
    #Database server for producton
    DB_SERVER = '192.168.1.56'
    #database URI
    def DATADASE_URI(self):
        return f"mysql://user@{self.DB_SERVER}/foo"
    
#Production environment
class Production(Config):
    DEBUG = False
    DB_SERVER = '192.168.1.32'
    
#Development environmet where debugging is true   
class Development(Config):
    DEBUG = True
    DB_SERVER ='localhost'
    
#Testing environment    
class Testing(Config):
    DB_SERVER = 'localhost'
    DATABASE_URI = 'sqlite:///:memory:'
    
    
    
config = {
    "development": Development,
    "testing": Testing,
    "production": Production,
    "default": Development
    
}