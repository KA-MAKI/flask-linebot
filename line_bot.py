from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os
import logging
from dotenv import load_dotenv
from chatgpt_api import get_tax_advice

# 環境変数のロード
load_dotenv()

# ログ設定（エラーを確認するため）
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# LINE APIの設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=["POST"])
def webhook():
    """LINEからのメッセージを受け取るエンドポイント"""
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    logging.info(f"📩 受信データ: {body}")  # ログ出力

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logging.error("❌ InvalidSignatureError: LINEのシークレットキーが間違っている可能性があります。")
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ユーザーからのメッセージを処理"""
    user_message = event.message.text
    logging.info(f"📨 ユーザーの入力: {user_message}")

    try:
        chatgpt_response = get_tax_advice(user_message)
        logging.info(f"💬 ChatGPTの返答: {chatgpt_response}")

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=chatgpt_response)
        )
    except Exception as e:
        logging.error(f"⚠ エラー発生: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="申し訳ありません。システムエラーが発生しました。")
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
