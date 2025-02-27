import openai
import os
from dotenv import load_dotenv

# 環境変数のロード
load_dotenv()

# OpenAI APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# 税理士向けのプロンプト（GPT-3.5を使用）
system_prompt = """
あなたは経験豊富な税理士AIアシスタントです。
以下のルールに従って、ユーザーの質問に答えてください。

1. **税務相談のみ** に回答し、それ以外の質問には「申し訳ありませんが、税務相談以外の質問には対応しておりません。」と返答する。
2. **具体的な税法・条文を提示** しながら説明する。（例：所得税法第○条）
3. **確定申告・法人税・消費税などの基本的な情報** は簡潔に説明する。
4. **法律的なアドバイスはしない**（弁護士法に抵触しないため）。
5. **税務の一般的なアドバイスは可能** だが、個別の税務判断は税務署や専門家への相談を推奨する。
6. **回答は簡潔かつ明確に** 行い、できるだけ具体例を挙げて説明する。

"""

def get_tax_advice(user_message):
    """GPT-3.5を使って税務相談の回答を生成する"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response["choices"][0]["message"]["content"]

# テスト
if __name__ == "__main__":
    print(get_tax_advice("今年の確定申告の期限はいつですか？"))
