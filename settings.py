from pathlib import Path

#LINEbot
access_token='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
secret_key='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

#DB
db_info = {
    'user': 'aaaaaaaaaaaaaa',
    'password': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    'host': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    'database': 'aaaaaaaaaaaaaa',
    'charset': 'utf8mb4',
}
db_uri='postgres://{user}:{password}@{host}/{database}'.format(**db_info)  #for psql in heroku
# db_uri='mysql+pymysql://{user}:{password}@{host}/{database}?charset={charset}'.format(**db_info)

#makottyann
time=[2100,1140,1215]

#flask_setting
JSON_AS_ASCII = False
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = True
SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
UPLOADED_CONTENT_DIR = Path("upload")