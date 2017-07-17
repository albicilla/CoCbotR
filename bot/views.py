# -*- encoding: utf-8 -*-
import json
import random
import requests

from django.shortcuts import render
from django.http import HttpResponse

import sys
path="/Users/albicilla/programming/osoBOT/osomatsu_bot/bot/"
sys.path.append(path)

import load_serif

from load_serif import osomatsu_serif  # 先ほどのおそ松のセリフ一覧をimport
import re #正規表現

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'cf6MkYQIETJ7+jKqHJxVXDqOjHAGrTNfALgyds2qfY3HIslXGQ7GSAGJpALAa2TAZnLNT6u885N6P6w2BB2Qj1EQpdoiQjut0IVAWBlTOikyJwBbnYeAnRj9po9bwmCTJKH/ciE0bAJ+8PbtAOtERAdB04t89/1O/w1cDnyilFU='
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def index(request):
    return HttpResponse("This is bot api.")

def reply_text(reply_token, text):
    reply = random.choice(osomatsu_serif)

    r = re.compile("^[a-z0-9]")
    m = r.search(text)
    if m == "None":
        print ("N")
    else:
        reply  = str([random.randint(1,100)])
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": reply
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return reply

def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
    return HttpResponse(reply)  # テスト用
