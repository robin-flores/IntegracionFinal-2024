class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'

#Nombre y contraseña de la base de datos
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'parkhouse'
    MYSQL_CURSORCLASS = 'DictCursor'

config = {
    'development': DevelopmentConfig
}