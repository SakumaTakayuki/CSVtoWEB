from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.model import Base, Run
from modules.log_manager import get_session, save_log, get_logs
from datetime import datetime
from zoneinfo import ZoneInfo


def get_obj_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    obj_sessionmaker = sessionmaker(bind=engine)
    return obj_sessionmaker()


def test_get_session():
    # テスト
    result_session = get_session()

    # 検証
    assert isinstance(result_session, Session)
    result_session.close()


def test_save_log():
    # テスト
    obj_session = get_obj_session()
    run = Run()
    save_log(obj_session, run)

    # 検証
    result = obj_session.query(Run).first()
    assert result is not None
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    result.timestamp = result.timestamp.replace(tzinfo=ZoneInfo("Asia/Tokyo"))
    delta = abs((now - result.timestamp).total_seconds())
    assert delta < 5
    obj_session.close()


def test_get_logs():
    # テスト
    obj_session = get_obj_session()
    run1 = Run(status="成功", timestamp=datetime(2025, 12, 1, 10, 0, 0))
    run2 = Run(status="失敗", timestamp=datetime(2025, 12, 1, 9, 0, 0))
    run3 = Run(status="成功", timestamp=datetime(2025, 12, 1, 8, 0, 0))
    run4 = Run(status="失敗", timestamp=datetime(2025, 12, 1, 7, 0, 0))
    run5 = Run(status="成功", timestamp=datetime(2025, 12, 1, 6, 0, 0))
    save_log(obj_session, run1)
    save_log(obj_session, run2)
    save_log(obj_session, run3)
    save_log(obj_session, run4)
    save_log(obj_session, run5)

    # 検証
    result_all = get_logs(obj_session, "全て")
    result_success = get_logs(obj_session, "成功")
    result_failure = get_logs(obj_session, "失敗")
    assert result_all is not None
    assert len(result_all) == 5
    assert result_success is not None
    assert len(result_success) == 3
    assert result_failure is not None
    assert len(result_failure) == 2
    for row in result_success:
        assert row.status == "成功"
    for row in result_failure:
        assert row.status == "失敗"
    timestamps_all = [row.timestamp for row in result_all]
    sorted_timestamps_all = sorted(timestamps_all, reverse=True)
    assert timestamps_all == sorted_timestamps_all
    timestamps_success = [row.timestamp for row in result_success]
    sorted_timestamps_success = sorted(timestamps_success, reverse=True)
    assert timestamps_success == sorted_timestamps_success
    timestamps_failure = [row.timestamp for row in result_failure]
    sorted_timestamps_failure = sorted(timestamps_failure, reverse=True)
    assert timestamps_failure == sorted_timestamps_failure
    obj_session.close()
