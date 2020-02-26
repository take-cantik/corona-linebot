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
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

#クラス指定
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

# タイムストップの関数
def time_start(stime):
    stime = int(stime)
    time.sleep(3)
    message = "スタート！"
    start = float(time.time())
    print("AHIAHIAHI")
    print(start)
    print("AHIAHIAHI")
    return start, stime, message

def timeresult(stime, start):
    usertime = float(time.time())
    print("AHIAHI")
    print(usertime)
    print("AHIAHI")
    time_2 = start + stime + 1.5

    if usertime > time_2:
        message = "{}秒以上でした。\n残念賞！！！".format(stime)
    elif usertime <= time_2:
        dif_time = abs(time_2 - usertime) #絶対値
        message = "{0}秒との差は{1}秒でした。".format(stime, dif_time)
    return message

# 王様ゲームの関数
def king_game(personnum):
    allusernum = int(personnum)
    numnumnum = []
    numnum = 1
    for i in range(allusernum - 1):
        numnumnum.append(numnum)
        numnum += 1
    #iは人の番号が入ったlist
    designuser = random.sample(numnumnum,2)
    hands = ["に一番気になる子を言う",
             "をデコピン",
             "に真顔で「大好き」と言う",
             "にジュースを買ってあげる",
             "と交際経験を赤裸々に語る",
             "に濃厚接触をする",
             "と初恋を語る",
             "を褒めちぎる",
             "が好きだと叫ぶ",
             "を笑わせる",
             "のものまねをする",
             "と連絡先を交換する",
             "と30秒間見つめ合う",
             "にクサいセリフを言う",]
    user1 = designuser[0]
    user2 = designuser[1]
    message = "{0}番の人は{1}番の人".format(user1, user2) + hands[random.randint(0, len(hands) - 1)]
    return message

# じゃんけんの関数
def zyanken(reply):

    #1:グー 2:チョキ 3:パー
    if reply == "グー":
        userhand = 1

    elif reply =="チョキ":
        userhand = 2

    elif reply == "パー":
        userhand = 3

        #userhand = 4 はグーチョキパー以外が入力されたとき
    else:
        userhand = 4

    cpuhand = random.randint(1,3)


    if cpuhand == 1:
        returnhand = "グー"
    elif cpuhand == 2:
        returnhand = "チョキ"
    elif cpuhand == 3:
        returnhand = "パー"

    status = (userhand - cpuhand + 2) % 3


        #0:負け　1:勝ち　2:あいこ 基準は出した人
    if status == 0:
        say = "あなたの犬です。このバカチンが！"
    elif status == 1:
        say = "ナイスですね！"
    elif status == 2:
        say = "カブトムシ。"


    #userhandが4のときエラー文を出力してそれ以外のときに返答文を返す
    if userhand == 4:
        message = "グー、チョキ、パーをカタカナで入力してね♡"
    else:
        message = "私は"+returnhand+"をだしました"+ say

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
    print("AHI")
    print(num)
    print("AHI")

    if "終了" in event.message.text:
        number = 0
        message = "り"
    # ゲームの説明
    elif "eカード" in event.message.text and "説明" in event.message.text:
        number = 0
        message = ""
    elif "タイムストップ" in event.message.text and "説明" in event.message.text:
        number = 0
        message = ""
    elif "オリジナル王様ゲーム" in event.message.text and "説明" in event.message.text:
        number = 0
        message = ""
    elif "じゃんけん" in event.message.text and "説明" in event.message.text:
        number = 0
        message = ""
    # ゲームの選択
    elif "eカード" in event.message.text: 
        number = 10
        message = "ほいだらスタートや！\nなんかテキトーに送ってや。"
    elif "タイムストップ" in event.message.text:
        number = 20
        message = "ほいだらスタートや！\n何秒にするか数字だけ送ってや！"
    elif "オリジナル王様ゲーム" in event.message.text:
        number = 30
        message = "ほいだらスタートや！\n参加人数の数字だけ送ってや！"
    elif "じゃんけん" in event.message.text:
        number = 40
        message = "ほいだらスタートや！\n最初はグー、じゃんけん…"
    # ゲームの内容
    elif num == 20:
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
        number = 21
    elif num == 21:
        time_contents = db.session.query(Timestop).all()
        st_ti = time_contents[-1].start_time
        se_ti = time_contents[-1].set_time
        message = timeresult(se_ti, st_ti)
        number = 0
    elif num == 30:
        message = king_game(event.message.text)
        number = 0
    elif num == 40:
        message = zyanken(event.message.text)
        number = 0
    else:
        message = "このLINEbotでは以下のゲームを行うことができます。\n・eカード(仮)\n・タイムストップ\n・オリジナル王様ゲーム\nやりたいゲーム名を入力してください。\n遊び方はゲーム名と説明を送ると分かるよ！"
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
    #print("最後のやつ")
    #print(time.time())
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(message)
    )


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
