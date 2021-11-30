import urllib.parse
root = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus('Nipun@2003')
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{root}:{password}@localhost/examhelper'
SECRET_KEY = "NIPUN"


USER_CREATED_SUCCESSFULLY = 0
USER_CREATE_FAILED = 1
USER_ALREADY_EXISTED = 2