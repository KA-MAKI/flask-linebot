import openai
import os

# 環境変数からAPIキーを取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ 環境変数 `OPENAI_API_KEY` が設定されていません！")

# ChatGPT APIの呼び出し
def get_chatgpt_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは税理士アシスタントです。"},
            {"role": "user", "content": user_input}
        ],
        api_key=OPENAI_API_KEY
    )
    return response["choices"][0]["message"]["content"]

# 動作確認用
if __name__ == "__main__":
    test_input = "確定申告の期限はいつですか？"
    print(get_chatgpt_response(test_input))
