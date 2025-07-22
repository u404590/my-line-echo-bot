# app.py

import os # 引入 os 模組來讀取環境變數
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 從環境變數中讀取密鑰，而不是直接寫死在程式碼中
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', None)

# 檢查密鑰是否存在，如果沒有設定則會報錯
if LINE_CHANNEL_ACCESS_TOKEN is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    exit(1)
if LINE_CHANNEL_SECRET is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    exit(1)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    print(f"Received message from user: {user_message}")

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=user_message)
    )

# 從環境變數中讀取 Port，Replit 會提供一個 Port
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000)) # 預設使用 5000，但 Replit 會設定自己的 Port
    app.run(host='0.0.0.0', port=port) # 監聽所有 IP，讓 Replit 能存取
