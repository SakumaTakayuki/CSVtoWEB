from db.session import SessionLocal
from db.model import Run, RunDetail
from datetime import datetime, date
from zoneinfo import ZoneInfo


session = SessionLocal()


def save_log(result):
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    str_now = now.strftime("%Y/%m/%d %H:%M:%S")
    result.timestamp = datetime.strptime(str_now, "%Y/%m/%d %H:%M:%S").replace(
        tzinfo=ZoneInfo("Asia/Tokyo")
    )
    session.add(result)
    session.commit()


def get_logs(filter_option="全て"):
    if filter_option == "成功":
        return (
            session.query(Run)
            .filter(Run.status == "成功")
            .order_by(Run.timestamp.desc())
            .all()
        )
    elif filter_option == "失敗":
        return (
            session.query(Run)
            .filter(Run.status != "成功")
            .order_by(Run.timestamp.desc())
            .all()
        )
    else:
        return session.query(Run).order_by(Run.timestamp.desc()).all()


def get_run_details(run_id: int):
    return (
        session.query(RunDetail)
        .filter(RunDetail.run_id == run_id)
        .order_by(RunDetail.row_number)
        .all()
    )


def get_run_details_error(run_id: int):
    return (
        session.query(RunDetail)
        .filter(RunDetail.run_id == run_id, RunDetail.result == "エラー")
        .order_by(RunDetail.row_number)
        .all()
    )


def get_today_count():
    return session.query(Run).filter(Run.timestamp >= date.today()).count()


def get_latest_log():
    logs = session.query(Run).order_by(Run.id.desc()).first()
    if logs is None:
        return "-"
    return logs.status


def get_success_rate():
    successes = session.query(Run).filter(Run.status == "成功").count()
    logsCount = session.query(Run).count()
    if successes == 0 or logsCount == 0:
        return 0
    return int((successes / logsCount) * 100)


def csv_encode(list):
    return list.to_csv(index=False, quoting=2).encode("utf-8")
