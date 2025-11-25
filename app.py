import os
import streamlit as st
from openai import OpenAI

from dotenv import load_dotenv
import os

# .envファイルを読み込む
load_dotenv()

# 環境変数の取得
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")

def get_llm_response(user_input, expert_type):
    """
    入力テキストと専門家タイプを基にLLMからの回答を取得する関数。
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    # 専門家タイプに応じたシステムメッセージを設定
    if expert_type == "A":
        system_message = "あなたは日本食に関する専門家です。日本食に関する質問に答えてください。"
    elif expert_type == "B":
        system_message = "あなたはアジア料理に関する専門家です。アジア料理に関する質問に答えてください。"
    else:
        system_message = ""

    # LLMへのプロンプトを作成
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content

# Streamlitアプリの構築
st.title("LLMを活用した専門家アプリ")

# アプリの概要を表示
st.write("""
このアプリでは、以下の操作が可能です：
1. 入力フォームに質問を入力してください。
2. 日本食の専門家またはアジア料理の専門家を選択してください。
3. 送信すると、選択した専門家が質問に回答します。
""")

# ラジオボタンで専門家タイプを選択
expert_type = st.radio(
    "専門家の種類を選択してください：",
    ("A", "B"),
    format_func=lambda x: "日本食の専門家" if x == "A" else "アジア料理の専門家"
)

# 入力フォームを作成
user_input = st.text_input("質問を入力してください：")

# 送信ボタン
if st.button("送信"):
    if user_input:
        # LLMからの回答を取得
        response = get_llm_response(user_input, expert_type)
        # 回答を表示
        st.write("### 回答：")
        st.write(response)
    else:
        st.warning("質問を入力してください！")