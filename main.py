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
class Egame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    king_card = db.Column(db.Integer, unique=False)
    turn = db.Column(db.Integer, unique=False)

    def __init__(self, king_card, turn):
        self.king_card = king_card
        self.turn = turn

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

class Inputstop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Integer, unique=False)
    select_text = db.Column(db.String(80), unique=False)

    def __init__(self, start_time, select_text):
        self.start_time = start_time
        self.select_text = select_text

class Turninputstop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Integer, unique=False)
    select_text = db.Column(db.String(80), unique=False)

    def __init__(self, start_time, select_text):
        self.start_time = start_time
        self.select_text = select_text

class Speedstop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Integer, unique=False)

    def __init__(self, start_time):
        self.start_time = start_time

# eゲームの関数
#"user1は数字を選択してください　\n king:0 \n citizen:1"
def user1_chose1(reply, num):
    if str(0) in reply:
        k = 0
    else:
        k = 1

    num += 1
    return k, num

def user1_chose2(reply):
    if str(0) in reply:
        k = 0
    else:
        k = 1

    return k

#"user2は数字を選択してください　\n slave:0 \n citizen:1"
def user2_chose(reply):
    if str(0) in reply:
        s = 0
    else:
        s = 1
    return s

def judge(k, s, finish):
    if k == 0 and s == 1:
        message = "king selected KING\nslave selected CITIZEN\n\nking win!"
        finish = 1
    elif k == 0 and s == 0:
        message = "king selected KING\nslave selected SLAVE\n\nslave win!"
        finish = 1
    elif k == 1 and s == 0:
        message = "king selected CITIZEN\nslave selected SLAVE\n\nking win!"
        finish = 1
    else:
        message = "king selected CITIZEN\nslave selected CITIZEN\n\n"
        finish = 0

    return message, finish

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
def zyanken(reply, num):

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
        say = "あなたの負けです。このバカチンが！"
    elif status == 1:
        say = "ナイスですね！"
    elif status == 2:
        say = "カブトムシ。"


    #userhandが4のときエラー文を出力してそれ以外のときに返答文を返す
    if userhand == 4:
        message = "グー、チョキ、パーをカタカナで入力してね♡"
        num = 40
    else:
        message = "私は"+returnhand+"をだしました\n"+ say
        num = 0
    return message, num

# 早打ちゲーム関数
def input_start():
    time.sleep(3)
    random_word =[
    "あしこりく",
    "そけるみね",
    "おじほふき",
    "みけとかし",
    "こいえるし",
    "わそくいね",
    "やきふれそ",
    "むねひくそ",
    "おきぬませ",
    "こせいぬき",
    "あえいおう",
    "おめにしき",
    "かせいくぬ",
    "そめかほき",
    "おわゆくね",
    "めかをんき",
    "んこめうぬ",
    "ちたぬきみ",
    ]

    message = random.choice(random_word)
    start = float(time.time())
    return start, message

def inputresult(start, set_message, input_word):
    input_time = float(time.time())
    difdif_time = input_time - start + 1.5

    if  input_word != set_message:
        difdif_time += 2
        message = "{0}を間違えて{1}と入力するのに{2}秒かかりました!\n打ち間違いには注意しよう！".format(set_message,input_word, difdif_time)

    elif input_word == set_message:
        message = "{0}と入力するのに{1}秒かかりました!".format(set_message, difdif_time)

    return message

#反転文字を入力、、　input_start()は流用
def turninputresult(start,set_message,input_word):
    input_time = float(time.time())
    difdif_time = input_time - start + 1.5

    input_word = input_word[::1]
    if  input_word != set_message:
        difdif_time += 2
        message = "{0}を間違えて{1}と入力するのに{2}秒かかりました!\n打ち間違いには注意しよう！".format(set_message,input_word, difdif_time)

    elif input_word == set_message:
        message = "{0}と入力するのに{1}秒かかりました!".format(set_message, difdif_time)

    return message

# 早押しの関数
def speed_start():
    time.sleep(random.randint(2,8))
    message = "スタート"
    start = float(time.time())
    return start

def speed_result(start):
    usertime = float(time.time())
    difdifdif_time = usertime - (start + 1.5)
    message = "あなたの早押し時間は{0}秒でした".format(difdifdif_time)
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
        message = "人数の目安：２\nこれは対戦型ゲームです\nまず、片方が「王」もう片方が「奴隷」となり、\nそれぞれ王ならば[王、市民、市民、市民]、奴隷ならば[奴隷、市民、市民、市民]という４つの手札を持っています\nそれぞれのパワーバランスは、王は市民に強く、市民は奴隷に強く、奴隷は王に強くなっています\n双方が同時に手札を出し合って勝敗を決めます。"
    elif "タイムストップ" in event.message.text and "説明" in event.message.text:
        number = 0
        message = "人数の目安：１〜\nこのゲームはいかにピッタリの秒数を当てられるかを競うゲームです\nまずはじめにピッタリ当てたい秒数を入力してもらいます\nその後しばらくしてLINE側から”スタート”と返答されるのでその時点から測定を開始します\nもし入力した秒数になったと感じたら任意の文字を入力してください\nするとLINE側から当てたい秒数と自分の止めた秒数との差が表示されます\nなお指定した時間を超過した後に止めるとGAMEOVERです\nぴったりをめざして頑張ってください！！"
    elif "オリジナル王様ゲーム" in event.message.text and "説明" in event.message.text:
        number = 0
        message = "人数の目安：３〜\nこのゲームを始める前に参加者それぞれに番号を振ってください\n王様、命令される人、お題をLINE側から提供します！\n完全ランダムのスリルをとくとお試しあれ！"
    elif "じゃんけん" in event.message.text and "説明" in event.message.text:
        number = 0
        message = "vs LINE bot\n「グー」「チョキ」「パー」のいずれかを送ってください\nじゃんけんは実力\nとにかく勝て！！！"
    elif "反転早打ちゲーム" in event.message.text and "説明" in event.message.text:
        number = 0
        message = '人数の目安：１〜\nこのゲームはランダムに生成された５文字を"右から逆に早く"打ってもらいます\n目指せ早打ち王！'
    elif "早打ちゲーム" in event.message.text and "説明" in event.message.text:
        number = 0
        message = "人数の目安：１〜\nこのゲームはランダムに生成された５文字を早く打ってもらいます\n目指せ早打ち王！"
    elif "早押しゲーム" in event.message.text and "説明" in event.message.text:
        number = 0
        message = "人数の目安：１〜\nスタートがLINE側から出された瞬間に任意の文字をできるだけ早く押してください\n目指せ早押し王！"
    # ゲームの選択
    elif "eカード" in event.message.text: 
        number = 10
        message = "ほいだらスタートや！\nPlayer1はカードを選択してくれ\n0が王で1が市民や！"
    elif "タイムストップ" in event.message.text:
        number = 20
        message = "ほいだらスタートや！\n何秒にするか数字だけ送ってや！"
    elif "オリジナル王様ゲーム" in event.message.text:
        number = 30
        message = "ほいだらスタートや！\n参加人数の数字だけ送ってや！"
    elif "じゃんけん" in event.message.text:
        number = 40
        message = "ほいだらスタートや！\n最初はグー、じゃんけん…"
    elif "反転早打ちゲーム" in event.message.text:
        number = 60
        message = "ほいだらスタートや！\nなんか送ったら三秒後にお題が出るで！"
    elif "早打ちゲーム" in event.message.text:
        number = 50
        message = "ほいだらスタートや！\nなんか送ったら三秒後にお題が出るで！"
    elif "早押しゲーム" in event.message.text:
        number = 70
        message = "ほいだらスタートや！\nなんか送ったら始まるで！\n何秒後に出てくるか分からへんから、用心しとき！"
    # ゲームの内容
    elif num == 10:
        turn = 0
        result = user1_chose1(event.message.text, turn)
        k = result[0]
        turn = result[1]
        egame = Egame(k, turn)
        db.session.add(egame)
        db.session.commit()
        message = "Player2はカードを選択してください。\n0が奴隷で1が市民や！"
        number = 11
    elif num == 11:
        fi_num = 0
        s = user2_chose(event.message.text)
        egame_contents = db.session.query(Egame).all()
        ki_ca = egame_contents[-1].king_card
        result = judge(ki_ca, s, fi_num)
        fi_num = result[1]

        if fi_num == 1:
            message = result[0]
            number = 0
        else:
            message = result[0] + "draw\n\nPlayer1はカードを選択してください。\n0が王で1が市民です。"
            number = 12
    elif num == 12:
        k = user1_chose2(event.message.text)
        egame_contents = db.session.query(Egame).all()
        tu = egame_contents[-1].turn
        tu += 1
        egame = Egame(k, tu)
        db.session.add(egame)
        db.session.commit()
        message = "Player2はカードを選択してください。\n0が奴隷で1が市民です。"

        if tu == 3:
            number = 13
        else:
            number = 11
            
    elif num == 13:
        fi_num = 0
        s = user2_chose(event.message.text)
        egame_contents = db.session.query(Egame).all()
        ki_ca = egame_contents[-1].king_card
        result = judge(ki_ca, s, fi_num)
        fi_num = result[1]

        if fi_num == 1:
            message = result[0]
        else:
            message = result[0] + "king win!"
        
        number = 0

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
        zyan_num = 0
        zyan_result = zyanken(event.message.text, zyan_num)
        message = zyan_result[0]
        number = zyan_result[1]
    elif num == 50:
        result = input_start()
        start = result[0]
        message = result[1]
        inputstop = Inputstop(start, message)
        db.session.add(inputstop)
        db.session.commit()
        number = 51
    elif num == 51:
        input_contents = db.session.query(Inputstop).all()
        st_ti = input_contents[-1].start_time
        se_te = input_contents[-1].select_text
        message = inputresult(st_ti, se_te, event.message.text)
        number = 0
    elif num == 60:
        result = input_start()
        start = result[0]
        message = result[1]
        turninputstop = Turninputstop(start, message)
        db.session.add(turninputstop)
        db.session.commit()
        number = 61
    elif num == 61:
        turninput_contents = db.session.query(Turninputstop).all()
        st_ti = turninput_contents[-1].start_time
        se_te = turninput_contents[-1].select_text
        message = turninputresult(st_ti, se_te, event.message.text)
        number = 0
    elif num == 70:
        start = speed_start()
        print("うおおおおおおおおおおおおおおおおおおおおおおおお")
        print(start)
        print("うおおおおおおおおおおおおおおおおおおおおおおおお")
        speedstop = Speedstop(start)
        db.session.add(speedstop)
        db.session.commit()
        number = 71
    elif num == 71:
        speed_contents = db.session.query(Speedstop).all()
        st_ti = speed_contents[-1].start_time
        message = speed_result(st_ti)
        number = 0
    else:
        message = "このLINEbotでは以下のゲームを行うことができます。\n・eカード(仮)\n・タイムストップ\n・オリジナル王様ゲーム\n・じゃんけん\n・早打ちゲーム\n・反転早打ちゲーム\n・早押しゲーム\nやりたいゲーム名を入力してください。\n遊び方はゲーム名と「説明」を送ると分かるよ！"
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
