import openai
import os
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

# OpenAI APIキーを取得
openai.api_key = os.getenv("OPENAI_API_KEY")

# ChatGPTのプロンプト（税理士向け）
system_prompt = """
あなたは経験豊富な税理士AIアシスタントです。
以下のルールに従って、ユーザーの質問に答えてください。

1. **税務相談のみ** に回答し、それ以外の質問には「申し訳ありませんが、税務相談以外の質問には対応しておりません。」と返答する。
2. **確定申告・法人税・消費税などの基本的な情報** は簡潔に説明する。
3. **税法に基づいた具体的なアドバイス** を提供する。（例：所得税法第○条）
4. **法律的なアドバイスはしない**（弁護士法に抵触しないため）。
5. **税務署や専門家への相談を推奨する**（個別の税務判断は不可）。
"""

def get_tax_advice(user_message):
    """GPT-3.5を使って税務相談の回答を生成する"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response["choices"][0]["message"]["content"]  # 新バージョンの書き方に修正
        
        # デバッグ用ログ出力
        print(f"✅ ChatGPT API に送信: {user_message}")
        print(f"💬 ChatGPT API の応答: {reply}")
        
        return reply
    except Exception as e:
        print(f"⚠ エラー: {e}")
        return "申し訳ありません。システムエラーが発生しました。"

# テスト用
if __name__ == "__main__":
    test_message = "今年の確定申告の期限はいつですか？"
    print(get_tax_advice(test_message))
