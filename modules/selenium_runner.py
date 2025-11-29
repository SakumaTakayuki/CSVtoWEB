from db.session import SessionLocal
from db.model import Run, RunDetail
from modules.selenium_driver import init_driver
from modules.selenium_actions import register_one


def run_selenium_process(csv_rows, check_only=False):
    session = SessionLocal()
    driver = init_driver(headless=False)

    run = Run()
    session.add(run)
    session.commit()
    session.refresh(run)

    success_count = 0
    fail_count = 0

    for i, row in enumerate(csv_rows, start=1):

        ok, error = register_one(driver, row)

        if ok:
            success_count += 1
        else:
            fail_count += 1

        detail = RunDetail(
            run_id=run.id,
            row_number=i,
            data=row,
            result="success" if ok else "error",
            error_message=error,
        )
        session.add(detail)

    run.total = len(csv_rows)
    run.success = success_count
    run.failed = fail_count
    run.status = "success" if fail_count == 0 else "partial"

    session.commit()
    driver.quit()
