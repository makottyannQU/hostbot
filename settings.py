from pathlib import Path

#LINEbot
access_token='i9NTbMHxmsuaxbDc1wdONh3d4gWmf1n0xOCyWRzBgbxuexfblaycUBfbvnxq/ert8VwFnlpVrCzya56/00iQPpNlF5oNH/ImFgIR25lHDdFj8XV0BeQxesug2+ezYfWisVrCca7iy52IAjN5gYICHgdB04t89/1O/w1cDnyilFU='
secret_key='46a9b4c50c1796fc4a1f7a1b5e43b6c4'

#DB
db_info = {
    'user': 'ebteviguhocrja',
    'password': '79682d065d147ce8b3919fbdd684801ed92074ff8b2a7840d515bb7dfc453fae',
    'host': 'ec2-54-221-215-228.compute-1.amazonaws.com:5432',
    'database': 'd2306btn9crms5',
    'charset': 'utf8mb4',
}
# db_uri = 'postgres://ebteviguhocrja:79682d065d147ce8b3919fbdd684801ed92074ff8b2a7840d515bb7dfc453fae@ec2-54-221-215-228.compute-1.amazonaws.com:5432/d2306btn9crms5'
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