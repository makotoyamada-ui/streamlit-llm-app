import os
from dotenv import load_dotenv
import openai
import streamlit as st

# envの読み込み
load_dotenv()

# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# LLMからの回答を取得する関数
def get_advice(input_text, category):
    """
    入力テキストとカテゴリを基にLLMからの回答を取得する関数。

    Args:
        input_text (str): ユーザーからの入力テキスト。
        category (str): ラジオボタンで選択されたカテゴリ。

    Returns:
        str: LLMからの回答。
    """
    system_message = ""
    if category == "食事へのアドバイス":
        system_message = "あなたは栄養学に関するアドバイザーです。ユーザーの健康に関する悩みに対して、必要な栄養が取れる具体的な食材を含めてアドバイスを提供してください。"
    elif category == "運動へのアドバイス":
        system_message = "あなたは運動に関するアドバイザーです。ユーザーの健康の悩みに対して、具体的な運動方法を含めてアドバイスを提供してください。"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_text},
        ],
        temperature=0.5
    )
    return response['choices'][0]['message']['content']

# Streamlit アプリのタイトル
st.title("日常の健康に関する悩みに食事面と運動面からアドバイスがもらえるアプリ")

st.write("##### 食事の専門家")
st.write("食事の側面から、健康的なアドバイスを提供します。")

st.write("##### 運動の専門家")
st.write("運動の側面から、健康的なアドバイスを提供します。")

# 動作モードの選択
selected_item = st.radio(
    "## 動作モードを選択してください。",
    ["食事へのアドバイス", "運動へのアドバイス"]
)
st.divider()

# ユーザーの悩みを入力するテキストエリア
user_input = st.text_area("悩みを入力してください。", placeholder="例: 最近疲れやすいのですが、どうすればいいですか？")

# 実行ボタン
if st.button("実行"):
    if not user_input:
        st.warning("悩みを入力してください。")
    else:
        # 選択されたカテゴリに基づいてアドバイスを取得
        advice = get_advice(user_input, selected_item)
        st.success("アドバイスが届きました！")
        st.write(advice)
