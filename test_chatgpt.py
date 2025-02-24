from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from dotenv import load_dotenv

# ✅ 環境変数の読み込み
load_dotenv()
app = Flask(__name__)

# ✅ 環境変数から LINE の API キーを取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("⚠️ 環境変数が正しく設定されていません！")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    print(f"📩 受信メッセージ: {body}")  # デバッグ用

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ InvalidSignatureError: シークレットキーが間違っている可能性があります。")
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()
    print(f"📩 受信したメッセージ: {user_message}")  # デバッグ用

    if user_message.lower() == "こんにちは":
        reply_text = "こんにちは！どのようなお手伝いができますか？"
    else:
        reply_text = f"「{user_message}」ですね。ご質問ありがとうございます！"

    print(f"✅ 送信するメッセージ: {reply_text}")  # デバッグ用
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # ✅ Railway 用にポートを 8080 に変更
    app.run(host="0.0.0.0", port=port, threaded=True)
