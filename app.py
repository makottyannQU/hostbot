# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from flask import Flask, request, abort, redirect, render_template, url_for
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import datetime
import json
from uuid import uuid4
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent
import jpholiday
import psycopg2  # for psql in heroku


import settings
from models import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = settings.JSON_AS_ASCII
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.SWAGGER_UI_DOC_EXPANSION
app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
app.config['UPLOADED_CONTENT_DIR'] = settings.UPLOADED_CONTENT_DIR

with app.app_context():
    db.init_app(app)
    # db.drop_all()  # Remove on release
    db.create_all()

db_engine = create_engine(settings.db_uri, pool_pre_ping=True)
defalt_stock = 200

line_bot_api = LineBotApi(settings.access_token)
handler = WebhookHandler(settings.secret_key)


# for run check
@app.route('/')
def index():
    return render_template('index.html', error=0)


@app.route('/menu')
def menu():
    try:
        date = request.args['date']
        query = f'''
                    select menu.date, "meal".name  from ( select * from "menu" where date = {date})
                    as menu inner join "meal" on menu.meal_id = "meal".id;
                    '''
        df = pd.read_sql(query, db_engine)
        menus = df.to_dict(orient='records')
    except:
        return render_template('index.html')

    if len(menus) > 0:
        return render_template('editmenu.html', menus=menus, date=date)
    else:
        return render_template('addmenu.html', date=date)


@app.route('/addmenu', methods=['GET', 'POST'])
def addmenu():
    if request.method == 'POST':
        print('DB登録開始')
        try:
            date = request.form['date']
            meals = request.form.getlist('meal')
            select = request.form.getlist('check_meal')
        except:
            return redirect(url_for('index', error=1, date=date))
            # return render_template('index.html', error=1, date=date)
        if len(set(meals)) != len(meals):
            return redirect(url_for('index', error=1, date=date))
            # return render_template('index.html', error=1, date=date)
        menus = []
        for i in range(len(meals)):
            print(meals)
            print(select)

            if len(meals[i]) > 0:
                tmp = []
                for s in select:
                    if str(i+1) == s[-1]:
                        tmp.append(s[0])
                if 's' in tmp:
                    s_stock = defalt_stock
                else:
                    s_stock = 0
                if 'm' in tmp:
                    m_stock = defalt_stock
                else:
                    m_stock = 0
                if 'l' in tmp:
                    l_stock = defalt_stock
                else:
                    l_stock = 0
                if s_stock+m_stock+l_stock > 0:
                    menus.append(Menu(date=int(
                        date), meal_id=meals[i], s_stock=s_stock, m_stock=m_stock, l_stock=l_stock))
        db.session.add_all(menus)
        db.session.commit()
        return redirect(url_for('index', error=0))
    else:
        return render_template('addmenu.html')


@app.route('/editmenu', methods=['GET', 'POST'])
def editmenu():
    if request.method == 'POST':
        print('DB登録開始(メニュー変更開始)))')

        date = request.form['date']
        menu_count = int(request.form['menu_count'])
        data_for_DB = []
        temp_list = []
        temp_stock_list = []
        print(request.form)
        print(date)

        # 変更のため元のデータを削除する
        selected_records = db.session.query(Menu).filter(
            Menu.date == int(date))  # .all() は省略可
        for x in selected_records:
            db.session.delete(x)
            db.session.commit()

        for i in range(menu_count):
            # temp_stock_list.clear()
            # temp_list.clear()
            # temp_stock_list.append(request.form['S_stock'+str(i+1)])
            # temp_stock_list.append(request.form['M_stock'+str(i+1)])
            # temp_stock_list.append(request.form['L_stock' + str(i + 1)])
            # temp_list.append(request.form['edit_meal'+str(i+1)])
            # temp_list.append(temp_stock_list)
            MEAL_ID = request.form['edit_meal' + str(i + 1)]
            S_STOCK = request.form['S_stock' + str(i + 1)]
            M_STOCK = request.form['M_stock' + str(i + 1)]
            L_STOCK = request.form['L_stock' + str(i + 1)]

            data_for_DB.append(Menu(date=int(
                date), meal_id=MEAL_ID, s_stock=S_STOCK,m_stock = M_STOCK,l_stock =L_STOCK))
        db.session.add_all(data_for_DB)
        db.session.commit()
        print(data_for_DB)

        return redirect(url_for('index'))
    else:
        return render_template('edit.html')


@app.route('/member')
def member():
    query = f'select * from "profile";'
    df = pd.read_sql(query, db_engine)
    profile = df.to_dict(orient='records')
    return render_template('member.html', profile=profile)


@app.route('/meal')
def meal():
    query = f'select * from "meal";'
    df = pd.read_sql(query, db_engine)
    data = df.to_dict(orient='records')
    return render_template('meal.html', data=data)


@app.route('/editmeal', methods=['GET', 'POST'])
def editmeal():
    if request.method == 'POST':
        print('DB登録開始(弁当編集)))')
        id_of_meal = request.form['id']
        name = request.form['name']
        s_price = int(request.form['s_price'])
        m_price = int(request.form['m_price'])
        l_price = int(request.form['l_price'])
        print(id_of_meal)
        print(name)
        print(s_price)
        print(m_price)
        print(l_price)

         # 変更のためセレクトされたmealレコードを抽出する
        selected_meal_record = db.session.query(Meal).filter(
            Meal.id == id_of_meal).first()
        # 更新  
        selected_meal_record.name = name
        selected_meal_record.s_price = s_price
        selected_meal_record.m_price = m_price
        selected_meal_record.l_price = l_price
        db.session.commit()

        return redirect(url_for('meal'))
    else:
        print('弁当編集ページ')
        meal_data = []
        print(request.args.get("id"))
        meal_id = request.args.get("id")
        selected_meal = db.session.query(
            Meal).filter(Meal.id == meal_id).all()
        # print(selected_meal[0].name)
        # for x in selected_meal:
        #     print(x.name)
        return render_template('editmeal.html', selected_meal=selected_meal[0])

@app.route('/look_in_DB')
def look_in_DB():
    query = f'select * from "meal";'
    df = pd.read_sql(query, db_engine)
    meals = df.to_dict(orient='records')
    query = f'select * from "menu";'
    df = pd.read_sql(query, db_engine)
    menu = df.to_dict(orient='records')
    query = f'select * from "orders";'
    df = pd.read_sql(query, db_engine)
    orders = df.to_dict(orient='records')

    return render_template('look_in_DB.html', meals=meals, menu=menu, orders=orders)


@app.route('/addmeal', methods=['GET', 'POST'])
def addmeal():
    if request.method == 'POST':
        try:
            name = request.form['name']
            s_price = int(request.form['s_price'])
            m_price = int(request.form['m_price'])
            l_price = int(request.form['l_price'])
            image = request.files['image']
        except:
            return render_template('addmeal.html', error='正しく入力してください')
        id = str(uuid4())
        path = f'upload/{id}.png'
        image.save(path)
        meal = Meal(id=id, name=name, image=path, s_price=s_price,
                    m_price=m_price, l_price=l_price)
        db.session.add(meal)
        db.session.commit()
        return redirect(url_for('meal'))
    else:
        return render_template('addmeal.html')


@app.route('/ordercheck')
def ordercheck():
    return render_template('ordercheck.html')


@app.route('/update_calendar', methods=['POST'])
def update_calendar():
    year = int(request.form['year'])
    month = int(request.form['month'])
    holiday = [str(x[0].day) for x in jpholiday.month_holidays(year, month)]
    ym = f'{year:04d}{month:02d}'
    query = f'''
            select menu.date, "meal".name, "menu".s_stock,"menu".m_stock ,"menu".l_stock from ( select * from "menu" where date between {ym}00 and {ym}32)
            as menu inner join "meal" on menu.meal_id = "meal".id;
            '''
    df = pd.read_sql(query, db_engine)
    menus = []
    for index, row in df.iterrows():
        day = str(int(str(row['date'])[-2:]))
        menu = row['name']
        if '丼' in menu:
            type = 'green'
        else:
            type = 'red'
        menus.append({"day": day, "title": menu,
                      "s_stock": row["s_stock"], "m_stock": row["m_stock"], "l_stock": row["l_stock"], "type": type})

    dict = {
        "year": year,
        "month": month,
        "event": menus,
        "holiday": holiday
    }

    #　orderテーブル
    order_check_list = []
    temp = 0
    query = f'''
            select * from orders where date between {ym}00 and {ym}32 ORDER BY date ASC
            '''
    df = pd.read_sql(query, db_engine)
    print(df)
    for index, row in df.iterrows():
        day = int(str(row['date'])[-2:])
        if temp != day:
            order_check_list.append(day)
        temp = day
    
    dict['order_check_list'] = order_check_list
    print(order_check_list)
    return json.dumps(dict, ensure_ascii=False)


@app.route('/get_meals', methods=['GET'])
def get_meals():
    query = f'select * from "meal";'
    df = pd.read_sql(query, db_engine)
    meals = df.to_dict(orient='records')
    return json.dumps(meals, ensure_ascii=False)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    profile = line_bot_api.get_profile(event.source.user_id)

    user = User(id=profile.user_id, name=profile.display_name)
    db.session.add(user)
    db.session.commit()
    # print(profile.user_id, profile.display_name, profile.picture_url, profile.status_message)
    app.logger.info(f'User add {profile.user_id}.')

    text = f'初めまして{profile.display_name}さん\nまこっちゃん弁当です'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text)
    )


@handler.add(UnfollowEvent)
def handle_follow(event):
    Session = sessionmaker(bind=db_engine)
    s = Session()
    s.query(User).filter(User.id == event.source.user_id).delete()
    s.commit()
    app.logger.info(f'User delete {event.source.user_id}.')


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
