from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

class Variable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usernum = db.Column(db.Integer, unique=False)

    def __init__(self, usernum):
        self.usernum = usernum

class Timestop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set_time = db.Column(db.Integer, unique=False)
    start_time = db.Column(db.Integer, unique=False)

    def __init__(self, set_time, start_time):
        self.set_time = set_time
        self.start_time = start_time

def time_start(stime):
    stime = int(stime)
    time.sleep(3)
    message = "スタート！"
    start = int(time.time())
    print("AHIAHIAHI")
    print(start)
    print("AHIAHIAHI")
    return start, stime, message

def timeresult(stime, start):
    usertime = int(time.time())
    print("AHIAHI")
    print(usertime)
    print("AHIAHI")
    start /= 1000
    time_2 = start + stime
    usertime /= 1000

    if usertime > time_2:
        message = "{}秒以上でした。\n残念賞！！！".format(stime)
    elif usertime <= time_2:
        dif_time = stime - abs(time_2 - usertime) #絶対値
        message = "{0}秒との差は{1}秒でした。".format(stime, dif_time)
    return message


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ここに色々書き込むよ
    contents = db.session.query(Variable).all()
    num = contents[-1].usernum
    print("AHIAHIAHI")
    print(num)
    print("AHIAHIAHI")

    if "終了" in event.message.text:
        number = 0
        message = "り"
    elif "eカード" in event.message.text and "説明" in event.message.text:
        number = 0
        message = ""
    elif "タイムストップ" in event.message.text and "説明" in event.message.text:
        number = 0
        message = ""
    elif "eカード" in event.message.text: 
        number = 1
        message = "ほいだらスタートや！\nなんかテキトーに送ってや。"
    elif "タイムストップ" in event.message.text:
        number = 2
        message = "ほいだらスタートや！\n何秒にするか数字だけ送ってや！"
    elif num == 2:
        result = time_start(event.message.text)
        start = result[0]
        stime = result[1]
        message = result[2]
        timestop = Timestop(stime, start)
        print("AHIAHI")
        print(timestop)
        print("AHIAHI")
        db.session.add(timestop)
        db.session.commit()
        number = 3
    elif num == 3:
        time_contents = db.session.query(Timestop).all()
        st_ti = time_contents[-1].start_time
        se_ti = time_contents[-1].set_time
        message = timeresult(se_ti, st_ti)
        number = 0
    else:
        message = "このLINEbotでは以下のゲームを行うことができます。\n・eカード(仮)\n・タイムストップ\nやりたいゲーム名を入力してください。\n遊び方はゲーム名と説明を送ると分かるよ！"
        number = 0   


    num = number
    variable = Variable(num)
    db.session.add(variable)
    db.session.commit()
    #contents = db.session.query(Variable).all()

    #print(contents)
    
    #messages = []

    #for content in contents:
    #    messages.append(TextSendMessage(content.usernum))


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(message)
    )


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
