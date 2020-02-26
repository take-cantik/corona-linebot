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
    num = cotents[-1]

    if "終了" in event.message.text:
        number = 0
        message = "り"
    else:
        if "eカード" in event.message.text: 
            number = 1
            message = "ほいだらスタートや！\nなんかテキトーに送ってや。"
        elif "タイムストップ" in event.message.text:
            number = 2
            message = "ほいだらスタートや！\nなんかテキトーに送ってや。"
        else:
            message = "このLINEbotでは以下のゲームを行うことができます。\n・eカード(仮)\n・タイムストップ\nやりたいゲーム名を入力してください。"
        


    number = num
    variable = Variable(num)
    db.session.add(variable)
    db.session.commit()
    contents = db.session.query(Variable).all()

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
