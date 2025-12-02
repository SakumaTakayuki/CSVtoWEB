import streamlit as st
import pandas as pd
from db.session import SessionLocal
from db.model import Run, RunDetail
from modules.selenium_driver import init_driver
from modules.selenium_actions import register_one
from modules.validation import validation_check

gender = ["男性", "女性", "その他"]
region = ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州", "日本以外"]


def run_selenium_process(csv_rows, check_only=False):
    total = len(csv_rows)
    progress_bar = st.progress(0)
    status_text = st.empty()

    success_count = 0
    fail_count = 0

    if check_only:
        for i, (index, row) in enumerate(csv_rows.iterrows(), start=1):
            message = validation_check(row)
            if not message is None:
                st.error(f"行 {index + 1}: {message}")
                st.write(f"入力内容: {row.to_dict()}")
                fail_count += 1
            else:
                success_count += 1
            progress_bar.progress(i / total)
            status_text.text(
                f"""
                    処理中 {i} / {total} 件
                    成功 : {success_count}
                    失敗 : {fail_count}
                """
            )
        return
    else:
        session = SessionLocal()
        driver = init_driver(headless=True)

        run = Run()
        session.add(run)
        session.commit()
        session.refresh(run)

        for i, (idx, row) in enumerate(csv_rows.iterrows(), start=1):
            message = validation_check(row)
            if not message is None:
                ok = False
                stage = "validation_check"
                error = message
            else:
                result = register_one(driver, row)
                ok = result["success"]
                stage = result["stage"]
                error = result["message"]

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
                error_stage=stage,
                error_message=error,
            )
            session.add(detail)
            progress_bar.progress(i / total)
            status_text.text(
                f"""
                    処理中 {i} / {total} 件
                    成功 : {success_count}
                    失敗 : {fail_count}
                """
            )

        run.total = len(csv_rows)
        run.success = success_count
        run.failed = fail_count
        run.status = "成功" if fail_count == 0 else "失敗"

        session.commit()
        driver.quit()

        return run
