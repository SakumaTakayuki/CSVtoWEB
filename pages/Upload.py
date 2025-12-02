import streamlit as st
import pandas as pd
from modules.csv_loader import load_csv
from modules.selenium_runner import run_selenium_process
from modules.log_manager import get_session, save_log, get_run_details_error
import json

session = get_session()

st.title("CSVアップロード")

# CSV ファイルアップロード
uploaded_file = st.file_uploader(
    label="CSVファイルをここにドラッグ＆ドロップ、もしくは「Browse filesボタン」から選択してください（1ファイル200MBまで）",
    type=["csv"],
    accept_multiple_files=False,
)

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
        if check_only:
            st.success("動作確認完了！")
        else:
            result.file_name = uploaded_file.name
            session = get_session()
            try:
                save_log(session, result)
                if result.status == "成功":
                    st.success("Selenium実行成功！")
                else:
                    details = get_run_details_error(session, result.id)
                    details_df = pd.DataFrame(
                        [
                            {
                                "行番号": d.row_number,
                                "データ": json.dumps(d.data, ensure_ascii=False),
                                "結果": d.result,
                                "エラー箇所": d.error_stage,
                                "エラー内容": d.error_message,
                            }
                            for d in details
                        ]
                    )
                    st.error("エラーが発生しました")
                    st.dataframe(details_df)
            except Exception as e:
                st.error(f"ログ保存中にエラーが発生しました: {e}")
            finally:
                session.close()

with st.sidebar:
    st.page_link("app.py", label="ダッシュボード")
    st.page_link("pages/Upload.py", label="CSVアップロード")
    st.page_link("pages/Logs.py", label="実行ログ")
