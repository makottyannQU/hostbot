from flask import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
import pandas as pd
import psycopg2  # for psql in heroku

import settings
from models import *

db_engine = create_engine(settings.db_uri, pool_pre_ping=True)
Session = sessionmaker(bind=db_engine)
s = Session()


# # print a table
# query = f'''
#         select * from "meal";
#         '''
# df = pd.read_sql(query, db_engine)
# print(df)


# # print a row
# user=s.query(User).filter_by(id == 'U6c8f1bb0cfb39e08bb5052f6d6fb632d').first()
# print(user)


# # add a row
# id=str(uuid4())
# meal = Meal(id=id, name='チキン南蛮',image=f'image/{id}.png',price=300)
# s.add(meal)
# s.commit()


# # delete a row
# s.query(User).filter(User.id == 'U6c8f1bb0cfb39e08bb5052f6d6fb632d').delete()
# s.commit()


# # marge tables user,meal,order
# user_id='U6c8f1bb0cfb39e08bb5052f6d6fb632d'
# ym='201908'
# query = f'''
#         select menu.date, "meal".name  from ( select * from "menu" where date between {ym}00 and {ym}32)
#         as menu inner join "meal" on menu.meal_id = "meal".id;
#         '''
# df = pd.read_sql(query, db_engine)
# print(df)
