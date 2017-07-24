# -*- encoding: utf-8 -*-
import json
import random
import requests

from django.shortcuts import render
from django.http import HttpResponse

# localで実行するときは以下三行のコメントアウトをはずす
import sys
path="/Users/albicilla/programming/osoBOT/osomatsu_bot/bot/"
sys.path.append(path)


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

    # dice 正規表現
    r = re.compile("\dd\d+")
    m = re.match(r,text)
    split_text=text.split("d")

    # 説明　正規表現
    explain = re.compile("explain*")

    # 狂気　正規表現
    sanc_s = re.compile("^scs$")
    sanc_l = re.compile("^scl$")

    #雑談　正規表現
    zatu = re.compile("huzioka")
    # 狂気の一覧
    scs_type = [
        'null',
        '気絶あるいは金切声',
        'パニックになって逃走',
        '感情の噴出（大泣きや大笑いなど）',
        '多弁症、一貫した会話の奔流',
        '釘付けになるほどの恐怖',
        '殺人癖、自殺癖',
        '幻覚/妄想',
        '周りの者の動作/発言を反復する'
        '異常食',
        '昏迷/緊張症'
    ]

    scl_type= [
        'null',
        '健忘症/昏迷/緊張症',
        '激しい恐怖症（逃走可能）',
        '幻覚',
        '奇妙な性的嗜好（露出狂、奇形愛好症など）',
        'フェティッシュ、異常な執着',
        '制御不能のチック、震え、失語',
        '心因性視覚障害、心因性難聴、四肢の機能障害',
        '心因反応（支離滅裂、妄想、常軌を逸したふるまい、幻覚など）',
        '一時的偏執症',
        '強迫観念に取りつかれた行動'
    ]

    reply = ""
    if re.match(explain,text):
        reply = "【コマンド一覧】\n[数値1]d[数値2]：[数値2]面ダイスを[数値1]回振る\nscs：短期の一時的狂気選択\nscl：長期の一時的狂気選択\n僕は藤岡だ。力になれたら嬉しい。"
    elif m:
        for i in range(int(split_text[0])):
            reply  += str([random.randint(1,int(split_text[1]))])
    elif re.match(sanc_s, text):
        rnum = str(random.randint(1,10))
        type = scs_type[int(rnum)]
        round = str(random.randint(4,14))
        reply = "結果：" + rnum + "\n" + type + "\nラウンド：" + round
    elif re.match(sanc_l, text):
        rnum = str(random.randint(1,10))
        type = scl_type[int(rnum)]
        time_list = range(10, 110, 10)
        time_select = random.randint(0,9)
        reply = "結果：" + rnum + "\n" + type + "\n時間：" + str(time_list[time_select])
    elif re.match(zatu,text):
        reply = random.choice(osomatsu_serif)



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
