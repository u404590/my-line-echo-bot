# app.py

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# >>> 請將這些值替換成你在 LINE Developers Console 取得的實際資訊 <<<
LINE_CHANNEL_ACCESS_TOKEN = 'YOUR_CHANNEL_ACCESS_TOKEN'
LINE_CHANNEL_SECRET = 'YOUR_CHANNEL_SECRET'
# >>> 替換結束 <<<

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 當 LINE 伺服器有事件發生時，會向這個 /callback 網址發送 POST 請求
@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature 標頭值，用於驗證請求的來源
    signature = request.headers['X-Line-Signature']

    # 取得請求主體作為文字
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # 處理 Webhook 主體
    try:
        # handler 會根據事件類型自動調用對應的處理函數
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 如果簽名無效，表示請求可能不是來自 LINE，拒絕處理
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400) # 返回 HTTP 400 Bad Request 錯誤

    return 'OK' # 成功接收請求，返回 'OK'

# 當收到文字訊息時，這個函數會被調用 (Echo Bot 的核心邏輯)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # event.message.text 包含了用戶傳送的文字訊息
    user_message = event.message.text
    print(f"Received message from user: {user_message}") # 在你的伺服器控制台顯示收到的訊息

    # 回覆用戶相同的文字訊息 (Echo Bot 的核心功能)
    line_bot_api.reply_message(
        event.reply_token, # 用於回覆訊息的一次性令牌
        TextSendMessage(text=user_message) # 建立一個文字訊息物件，內容為用戶傳來的訊息
    )

# 啟動 Flask 應用程式
if __name__ == "__main__":
    # app.run 預設會在 5000 port 運行
    app.run(port=5000, debug=True) # debug=True 會在程式碼修改時自動重啟，方便開發
