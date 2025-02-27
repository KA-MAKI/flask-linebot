# 必要なライブラリをインポート
import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# .env ファイルを読み込む（APIキーなどの設定）
load_dotenv()

# OpenAI APIキーを環境変数から取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Flask アプリケーションを作成
app = Flask(__name__)

# ルートエンドポイント（動作確認用）
@app.route("/", methods=["GET"])
def home():
    return "✅ サーバーは正常に起動しています！"

# LINE Webhook エンドポイント
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(f"📩 受信データ: {data}")

    # メッセージが含まれていない場合は何もしない
    if "events" not in data or len(data["events"]) == 0:
        return jsonify({"status": "no events"}), 200

    event = data["events"][0]  # 最初のイベントのみ処理
    user_message = event["message"]["text"]
    reply_token = event["replyToken"]

    # ChatGPT で応答を生成
    response_text = get_chatgpt_response(user_message)

    # LINE に返信（関数を呼び出す）
    send_line_reply(reply_token, response_text)

    return jsonify({"status": "success"}), 200

# ChatGPT にメッセージを送信し、回答を取得する関数
def get_chatgpt_response(user_message):
    openai.api_key = OPENAI_API_KEY  # APIキーをセット
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "あなたは税理士のアシスタントです。"},
                  {"role": "user", "content": user_message}]
    )
    return response["choices"][0]["message"]["content"]

# LINE に返信を送る関数
def send_line_reply(reply_token, response_text):
    import requests

    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": response_text}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=payload)

# 環境変数からポートを取得（Railway対応）
port = int(os.getenv("PORT", 8080))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
