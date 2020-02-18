from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
app = Flask(__name__)
#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
def myIndex(l, x):
    if x in l:
        return l.index(x)
    else:
        return -1
hands = ["グー","チョキ","パー"]
def selectHands(input):
    return myIndex(hands, input)
def judgeHands(userHand, cpuHand):
    #0:あいこ　1:cpuの勝ち　2:userの勝ち
    return (selectHands(userHand) - cpuHand + 3) % 3
def createMessage(input):
    if selectHands(input) == -1:
        message = "グー、チョキ、パーをカタカナで入力してね♡"
    else:
        cpuHand = random.randint(0,2)
        status = judgeHands(input, cpuHand)
        message = "botは" + hands[cpuHand] + "だよ\n"
        if status == 0:
            message += "どっちかというと引き分け"
        elif status == 1:
            message += "あなたの負け"
        elif status == 2:
            message += "あなたの勝ち"
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=createMessage(event.message.text)))
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
