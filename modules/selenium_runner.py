import streamlit as st
import pandas as pd
from db.session import SessionLocal
from db.model import Run, RunDetail
from modules.selenium_driver import init_driver
from modules.selenium_actions import register_one

gender = ["男性", "女性", "その他"]
region = ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州", "日本以外"]


def run_selenium_process(csv_rows, check_only=False):
    total = len(csv_rows)
    progress_bar = st.progress(0)
    status_text = st.empty()

    if check_only:
        for i, (index, row) in enumerate(csv_rows.iterrows(), start=1):
            message = "チェック完了"
            if isinstance(row["age"], (str)):
                if not row["age"].isdigit():
                    message = "ageが正しくありません"
            else:
                if pd.isna(row["age"]):
                    message = "ageが正しくありません"
                elif row["age"] < 0:
                    message = "ageが正しくありません"
            if pd.isna(row["gender"]) or not row["gender"] in gender:
                message = "genderが正しくありません"
            if pd.isna(row["region"]) or not row["region"] in region:
                message = "regionが正しくありません"
            if pd.isna(row["food"]):
                message = "foodが不足しています"
            if len(row) != 4:
                message = "列数が正しくありません"
            if message != "チェック完了":
                st.error(f"行 {index + 1}: {message}")
                st.write(f"入力内容: {row.to_dict()}")
            progress_bar.progress(i / total)
            status_text.text(f"処理中 {i} / {total} 件")
        return
    else:
        session = SessionLocal()
        driver = init_driver(headless=True)

        run = Run()
        session.add(run)
        session.commit()
        session.refresh(run)

        success_count = 0
        fail_count = 0

        for i, (idx, row) in enumerate(csv_rows.iterrows(), start=1):
            ok, error = register_one(driver, row)
            if ok:
                success_count += 1
            else:
                fail_count += 1

            data_to_save = {
                key: (None if pd.isna(val) else val)
                for key, val in row.to_dict().items()
            }
            detail = RunDetail(
                run_id=run.id,
                row_number=i,
                data=data_to_save,
                result="成功" if ok else "エラー",
                error_message=error,
            )
            session.add(detail)
            progress_bar.progress(i / total)
            status_text.text(f"処理中 {i} / {total} 件")

        run.total = len(csv_rows)
        run.success = success_count
        run.failed = fail_count
        run.status = "成功" if fail_count == 0 else "失敗"

        session.commit()
        driver.quit()

        return run
