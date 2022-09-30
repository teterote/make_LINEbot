from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os

app=Flask(__name__)
#環境変数の取得
YOUR_CHANNEL_ACCESS_TOKEN="D68eLCf3AQY4Iwbjt7lJcrmDQn7+Rp46Q9aFgDOsCcliyZcmJ6bGyZBQDWaueu70EO98Za5pkSQ0nNC3hh/ipGJnkM/ijmtYtnjaFguleS7rDob7LGZ3tVhnerikNp/HsyAOraa58jnWyiYCCgwhBwdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET="51bbc6616ac8c0a19f7b6b48abfc1325"
line_bot_api=LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)
