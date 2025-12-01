import streamlit as st
from db.init_db import init_db
from modules.log_manager import (
    get_session,
    get_latest_log,
    get_today_count,
    get_success_rate,
)

init_db()

session = get_session()

st.set_page_config(page_title="CSV → Web登録 自動化ツール", layout="wide")

st.title("CSV → Web登録 自動化ツール")

col1, col2, col3 = st.columns(3)

try:
    with col1:
        st.metric("今日の実行数", get_today_count(session))

    with col2:
        st.metric("最新ステータス", get_latest_log(session))

    with col3:
        st.metric("成功率", f"{get_success_rate(session)}%")
except Exception as e:
    st.error(f"ログ取得中にエラーが発生しました: {e}")
finally:
    session.close()

st.write("---")
st.subheader("メニュー")

st.page_link("pages/Upload.py", label="CSVアップロード")
st.page_link("pages/Logs.py", label="実行ログ")


with st.sidebar:
    st.page_link("app.py", label="ダッシュボード")
    st.page_link("pages/Upload.py", label="CSVアップロード")
    st.page_link("pages/Logs.py", label="実行ログ")
