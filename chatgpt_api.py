import openai
import os
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API の新しいバージョンに対応した呼び出し方法
client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": "あなたは税理士です。"},
              {"role": "user", "content": "今年の確定申告はいつですか？"}]
)

print(response.choices[0].message.content)
