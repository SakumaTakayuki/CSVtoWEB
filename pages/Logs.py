import streamlit as st
import pandas as pd
from modules.log_manager import get_session, get_logs, csv_encode, get_run_details
import json

session = get_session()

st.title("実行ログ")

filter_option = st.radio("表示するログ", ["全て", "成功", "失敗"], horizontal=True)

try:
    logs_result = get_logs(session, filter_option)

    logs = pd.DataFrame(
        [
            {
                "ID": log.id,
                "ファイル名": log.file_name,
                "実行時刻": log.timestamp,
                "取込数": log.total,
                "成功数": log.success,
                "失敗数": log.failed,
                "取込結果": log.status,
            }
            for log in logs_result
        ]
    )

    st.dataframe(logs)

    # ダウンロード
    csv = csv_encode(logs)
    st.download_button("CSVとしてダウンロード", csv, "logs.csv", "text/csv")

    st.write("---")

    st.subheader("詳細ログ")

    for log in logs_result:
        with st.expander(
            f"Run ID: {log.id} [{log.file_name}]（{log.timestamp}）  |  成功 {log.success} / 失敗 {log.failed}）"
        ):
            details = get_run_details(session, log.id)
            if not details:
                st.info("詳細ログはありません")
                continue

            details_df = pd.DataFrame(
                [
                    {
                        "行番号": d.row_number,
                        "データ": json.dumps(d.data, ensure_ascii=False),
                        "結果": d.result,
                        "エラー内容": d.error_message,
                    }
                    for d in details
                ]
            )

            def highlight_row(row):
                if row["結果"] == "エラー":
                    return ["background-color: #ffdddd"] * len(row)
                return [""] * len(row)

            st.dataframe(details_df.style.apply(highlight_row, axis=1))

            csv_detail = csv_encode(details_df)
            st.download_button(
                label="詳細ログをCSVとしてダウンロード",
                data=csv_detail,
                file_name=f"run_{log.id}_details.csv",
                mime="text/csv",
            )
except Exception as e:
    st.error(f"ログ取得中にエラーが発生しました: {e}")
finally:
    session.close()

with st.sidebar:
    st.page_link("app.py", label="ダッシュボード")
    st.page_link("pages/Upload.py", label="CSVアップロード")
    st.page_link("pages/Logs.py", label="実行ログ")
