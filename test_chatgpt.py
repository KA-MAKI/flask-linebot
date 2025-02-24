import os
from flask import Flask, request, abort
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# ✅ .env を読み込む
load_dotenv()

app = Flask(__name__)

# ✅ 環境変数から LINE API キーを取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("❌ 環境変数が正しく設定されていません！")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/")
def home():
    return "LINE Bot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    """ LINE Webhook エンドポイント """
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    # ✅ 受信したリクエストをログに出力（デバッグ用）
    print(f"📩 受信したリクエスト: {body}")

    if not signature:
        print("❌ エラー: X-Line-Signature ヘッダーがありません")
        return "Bad Request", 400

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ InvalidSignatureError: シークレットキーが間違っている可能性があります。")
        return "Invalid Signature", 400
    except Exception as e:
        print(f"❌ 予期しないエラー: {str(e)}")
        return "Internal Server Error", 500

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ ユーザーからのメッセージを受け取って返信 """
    user_message = event.message.text.strip()
    
    print(f"📨 受信メッセージ: {user_message}")

    if user_message == "こんにちは":
        reply_text = "こんにちは！どのようなご用件でしょうか？"
    else:
        reply_text = "メッセージありがとうございます！"

    print(f"✅ 送信するメッセージ: {reply_text}")
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, threaded=True)
