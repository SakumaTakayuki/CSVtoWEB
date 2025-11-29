import streamlit as st
import pandas as pd
from modules.csv_loader import load_csv
from modules.selenium_runner import run_selenium_process
from modules.log_manager import save_log


st.title("CSVアップロード")

# CSV ファイルアップロード
uploaded_file = st.file_uploader("CSVファイルを選択", type=["csv"])

df = None

if uploaded_file:
    df = load_csv(uploaded_file)
    st.subheader("プレビュー")
    st.dataframe(df)
    st.write(f"件数：{len(df)} 件")

st.write("---")
st.subheader("実行オプション")

col1, col2 = st.columns(2)
with col1:
    check_only = st.checkbox("チェックのみ（動作確認）", value=False)
with col2:
    st.write("")

# 実行ボタン
if st.button("▶ Web自動登録スタート"):
    if df is None:
        st.error("CSVファイルを選択してください")
    else:
        st.info("処理を開始します...")

        result = run_selenium_process(df, check_only)
        save_log(result)

        if result["status"] == "success":
            st.success("Selenium実行成功！")
        else:
            st.error("エラーが発生しました")
            st.json(result)

with st.sidebar:
    st.page_link("app.py", label="ダッシュボード")
    st.page_link("pages/Upload.py", label="CSVアップロード")
    st.page_link("pages/Logs.py", label="実行ログ")
