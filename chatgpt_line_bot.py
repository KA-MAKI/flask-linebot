import os
import openai
from flask import Flask, request, abort
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# ✅ 環境変数をロード
load_dotenv()

# ✅ LINE API の設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ✅ OpenAI API キーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Flask アプリを作成
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    """LINE Bot の Webhook エンドポイント"""
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ユーザーのメッセージを受信し、ChatGPT で処理"""
    user_message = event.message.text

    # ✅ ChatGPT にリクエスト
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "あなたは税理士のアシスタントです。"},
                  {"role": "user", "content": user_message}]
    )

    reply_text = response["choices"][0]["message"]["content"]

    # ✅ ユーザーに返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)

    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=user_message,
    max_tokens=200
)
reply_text = response["choices"][0]["text"].strip()

