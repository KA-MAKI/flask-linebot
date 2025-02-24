import os
import logging
from flask import Flask, request, abort

from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# ✅ ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ 環境変数をロード
load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("⚠ 環境変数が正しく設定されていません！")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    # ✅ 受信データをログに記録
    logger.info(f"📩 受信データ: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ InvalidSignatureError: シークレットキーが間違っている可能性があります。")
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()
    logger.info(f"✅ 受信メッセージ: {user_message}")

    if user_message == "こんにちは":
        reply_text = "こんにちは！どのようなお手伝いができますか？"
    else:
        reply_text = "メッセージありがとうございます！"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    logger.info(f"✅ 送信メッセージ: {reply_text}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, threaded=True)
