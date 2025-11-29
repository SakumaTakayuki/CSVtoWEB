import streamlit as st
from modules.log_manager import get_logs, export_logs_csv


st.title("実行ログ")

filter_option = st.radio("表示するログ", ["全て", "成功", "失敗"], horizontal=True)

logs = get_logs(filter_option)

st.dataframe(logs)

# ダウンロード
csv = export_logs_csv(logs)
st.download_button("CSVとしてダウンロード", csv, "logs.csv", "text/csv")

with st.sidebar:
    st.page_link("app.py", label="ダッシュボード")
    st.page_link("pages/Upload.py", label="CSVアップロード")
    st.page_link("pages/Logs.py", label="実行ログ")
