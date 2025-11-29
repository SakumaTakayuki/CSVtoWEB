import pandas as pd
from db.session import SessionLocal
from db.model import Run
from datetime import datetime, date


session = SessionLocal()


def save_log(result):
    result["timestamp"] = datetime.now()
    session.add(result)
    session.commit()


def get_logs(filter_option="全て"):
    if filter_option == "成功":
        return session.query(Run).filter(Run.status == "success").all()
    elif filter_option == "失敗":
        return session.query(Run).filter(Run.status != "success").all()
    else:
        return session.query(Run).all()


def get_today_count():
    return session.query(Run).filter(Run.timestamp >= date.today()).count()


def get_latest_log():
    logs = session.query(Run).order_by(Run.id.desc()).first()
    if logs is None:
        return "-"
    return logs.status


def get_success_rate():
    successes = session.query(Run).filter(Run.status == "success").count()
    logsCount = session.query(Run).count()
    if successes == 0 or logsCount == 0:
        return 0
    return int((successes / logsCount) * 100)


def export_logs_csv(list_run):
    data = [r.__dict__ for r in list_run]
    for d in data:
        d.pop("_sa_instance_state", None)
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode("utf-8")
