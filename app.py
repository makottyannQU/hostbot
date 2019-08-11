# -*- coding: utf-8 -*-
from flask import Flask, request, abort
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import datetime
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent
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

line_bot_api = LineBotApi(settings.access_token)
handler = WebhookHandler(settings.secret_key)


# for run check
@app.route('/')
def index():
    return 'Hello World!'


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
