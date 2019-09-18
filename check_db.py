# -*- coding: utf-8 -*-
from flask import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
import pandas as pd
# import psycopg2  # for psql in heroku
import pymysql
import datetime

import settings
from models import *

db_engine = create_engine(settings.db_uri, pool_pre_ping=True)
Session = sessionmaker(bind=db_engine)
s = Session()


def dateseparate(date):  # date=20190911
    yobi = ["月", "火", "水", "木", "金", "土", "日"]
    date = datetime.datetime.strptime(str(date), '%Y%m%d')
    year = date.strftime('%Y')
    month = str(int(date.strftime('%m')))
    day = str(int(date.strftime('%d')))
    week = date.weekday()
    return {'year': year, 'month': month, 'day': day, 'week': yobi[week]}


# # print a table
# query = f'''
#         select * from meal;
#         '''
# df = pd.read_sql(query, db_engine)
# print(df)


# # print a row
# users=s.query(Users).filter_by(id == 'U6c8f1bb0cfb39e08bb5052f6d6fb632d').first()
# print(users)


# # add a row
# id=str(uuid4())
# meal = Meal(id=id, name='チキン南蛮',image=f'image/{id}.png',price=300)
# s.add(meal)
# s.commit()


# # delete a row
# s.query(Users).filter(Users.id == 'U6c8f1bb0cfb39e08bb5052f6d6fb632d').delete()
# s.commit()


# # marge tables users,meal,orders
# user_id='U6c8f1bb0cfb39e08bb5052f6d6fb632d'
# query = f'''
#         select order1.date, users.name, meal.name, meal.price  from ( select * from orders where user_id = '{user_id}' )
#         as order1 inner join meal on order1.meal_id = meal.id inner join users on order1.user_id = users.id ;
#         '''
# df = pd.read_sql(query, db_engine)
# print(df)


########### clientbot #############


# #for order
# url='https://platform.coi.kyushu-u.ac.jp/lineapp/'
# now=datetime.datetime.now()
# date=now #if am
# #date=now+datetime.timedelta(days=1) # if pm
# date=date.strftime('%Y%m%d')
# query = f'''
#         select date from menu where date >= {date} order by date limit 1;
#         '''
# df = pd.read_sql(query, db_engine)
# if len(df)>0:
#     date = df.date[0]
#     query = f'''
#             select menu.date, menu.meal_id, meal.name as meal_name, meal.image as image_path, meal.s_price,
#             meal.m_price, meal.l_price, menu.s_stock, menu.m_stock, menu.l_stock
#             from (select * from menu where date = {date}) as menu inner join meal on menu.meal_id = meal.id;
#             '''
#     df = pd.read_sql(query, db_engine)
#     df['image_path']=url+df['image_path']
#     order_dict=df.to_dict(orient='records')
# else:
#     print('メニューがありません')


# # for cancel
# user_id = 'aaa'
# now = datetime.datetime.now()
# date = now  # if am
# # date=now+datetime.timedelta(days=1) # if pm
# date = date.strftime('%Y%m%d')
# query = f'''
#         select orders.date, orders.meal_id, meal.name as meal_name, orders.size from ( select * from orders
#         where date >= {date} and user_id = '{user_id}' and status = 1 ) as orders inner join meal on orders.meal_id = meal.id;
#         '''
# df = pd.read_sql(query, db_engine)
# if len(df) > 0:
#     cancel_dict=df.iloc[0].to_dict() #for cancel yesno question
# else:
#     status = 'none'


# # for cancel yes
# user_id = 'aaa'
# date = 20190911
# meal_id = '1602e8b9-0ef0-4a4d-964d-42f9108342ed'
# size = 1
# orders = s.query(Orders).filter_by(user_id = user_id, date = int(date), meal_id = meal_id, size = size, status = 1).first()
# if orders:
#     orders.status = -1
#     s.commit()
#     status = 'ok'
# else:
#     status = 'none'


# # for check
# user_id = 'aaa'
# now = datetime.datetime.now()
# date = now  # if am
# # date=now+datetime.timedelta(days=1) # if pm
# date = date.strftime('%Y%m%d')
# query = f'''
#         select orders.date, orders.meal_id, meal.name as meal_name, orders.size from ( select * from orders
#         where date >= {date} and user_id = '{user_id}' and status = 1 ) as orders inner join meal on orders.meal_id = meal.id;
#         '''
# df = pd.read_sql(query, db_engine)
# if len(df) > 0:
#     check_dict=df.iloc[0].to_dict()
# else:
#     status = 'none'


# # for menu
# now=datetime.datetime.now()
# date=now #if am
# #date=now+datetime.timedelta(days=1) # if pm
# date=date.strftime('%Y%m%d')
# query = f'''
#         select menu.date, meal.name as meal_name from ( select * from menu where date >= {date} )
#         as menu inner join meal on menu.meal_id = meal.id order by date;
#         '''
# df = pd.read_sql(query, db_engine)
# grouped = df.groupby('date', sort=False)
# menu_dict=[]
# for date, group in grouped:
#     menu_dict.append({'date':date,'meals':group.meal_name.to_list()})


################ hostbot #######################


# # for member
# query = f'''
#         select orders.date, users.id, users.name, profile.name as fullname, profile.grade, profile.department, profile.course,
#         profile.club from (select user_id, max(date) as date from orders group by user_id ) as orders
#         inner join users on orders.user_id = users.id
#         left outer join profile on orders.user_id = profile.user_id order by date desc;
#         '''
# df = pd.read_sql(query, db_engine)
# member_dict=df.to_dict(orient='records')


# # for ordercheck
# size_list=['小','中','大']
# query = f'''
#         select s1.date, meal.name as meal_name, s1.size, users.name as user_name from orders where status = 1 as s1 inner join
#         ( select max(date) as date from orders ) as s2 on s1.date = s2.date
#         inner join users on s1.user_id = users.id inner join meal on s1.meal_id = meal.id order by s1.timestamp;
#         '''
# df = pd.read_sql(query, db_engine)
# date = df.date[0]
# if len(df)==0:
#     print('注文はありません')
# else:
#     ordercheck_dict=[]
#     meal_grouped = df.groupby('meal_name', sort=False)
#     for meal_name, meal_group in meal_grouped:
#         size_grouped=meal_group.groupby('size', sort=False)
#         tmp=[]
#         for size,size_group in size_grouped:
#             tmp.append({'size':size_list[size],'member':size_group.user_name.to_list()})
#         ordercheck_dict.append({'meal_name':meal_name,'each_size':tmp})


# # check order num
# date = 20190911
# query = f'''
#         select * from menu where date = {date};
#         '''
# menu_df=pd.read_sql(query, db_engine)
# if len(menu_df)>0:
#     query = f'''
#             select orders.meal_id, orders.size, sum(count) as count from ( select meal_id, size, count from orders
#             where date = {date} and status != -1) as orders group by orders.meal_id, orders.size;
#             '''
#     df = pd.read_sql(query, db_engine)
#     ordernum={}
#     for index,row in menu_df.iterrows():
#         id=row.meal_id
#         tmp=df[df['meal_id']==id]
#         if len(tmp)>0:
#             try:
#                 s_count=tmp[tmp['size']==0]['count'].iloc[0]
#             except:
#                 s_count=0
#             try:
#                 m_count = tmp[tmp['size'] == 1]['count'].iloc[0]
#             except:
#                 m_count = 0
#             try:
#                 l_count=tmp[tmp['size']==2]['count'].iloc[0]
#             except:
#                 l_count=0
#         else:
#             s_count=0
#             m_count=0
#             l_count=0
#         ordernum[id]={'s_count':s_count,'m_count':m_count,'l_count':l_count,'s_stock':row.s_stock,'m_stock':row.m_stock,'l_stock':row.l_stock}
# else:
#     print('メニューがありません')