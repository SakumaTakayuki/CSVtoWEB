import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model import Base, Run, RunDetail
import modules.selenium_runner as runner


# ============================
# テスト用の in-memory DB を作成
# ============================
def get_obj_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    obj_sessionmaker = sessionmaker(bind=engine)
    return obj_sessionmaker()


# ============================
# run_all のテスト（成功ケース）
# ============================
def test_run_all_success():
    test_session = get_obj_session()
    # SessionLocal が test_session を返すように差し替え
    with patch(
        "modules.selenium_runner.SessionLocal", return_value=test_session
    ), patch("modules.selenium_runner.st", MagicMock()):
        # register_one を常に成功で返す
        fake_result = {"success": True, "stage": None, "message": None}

        with patch("modules.selenium_runner.register_one", return_value=fake_result):

            df = pd.DataFrame(
                [
                    {"age": 20, "gender": "男性", "region": "関東", "food": "寿司"},
                    {
                        "age": 30,
                        "gender": "女性",
                        "region": "北海道",
                        "food": "ラーメン",
                    },
                ]
            )

            results = runner.run_selenium_process(df, False)

    # ===== DB 検証 =====
    logs = test_session.query(Run).all()
    details = test_session.query(RunDetail).all()

    assert len(logs) == 1
    assert len(details) == 2

    assert results.total == 2
    assert results.success == 2
    assert results.failed == 0
    assert results.status == "成功"


# ============================
# run_all のテスト（失敗ケース）
# ============================
def test_run_all_with_failure():
    test_session = get_obj_session()
    # SessionLocal が test_session を返すように差し替え
    with patch(
        "modules.selenium_runner.SessionLocal", return_value=test_session
    ), patch("modules.selenium_runner.st", MagicMock()):

        success = {"success": True, "stage": None, "message": None}
        failure = {"success": False, "stage": "input", "message": "Timeout"}

        # register_one を 1行目成功 → 2行目失敗 にする
        with patch(
            "modules.selenium_runner.register_one", side_effect=[success, failure]
        ):

            df = pd.DataFrame(
                [
                    {"age": 20, "gender": "男性", "region": "関東", "food": "寿司"},
                    {
                        "age": "あ",
                        "gender": "その他",
                        "region": "九州",
                        "food": "リンゴ",
                    },
                ]
            )

            results = runner.run_selenium_process(df, False)

    # ===== DB 検証 =====
    logs = test_session.query(Run).all()
    details = test_session.query(RunDetail).all()

    assert len(logs) == 1
    assert len(details) == 2

    assert results.total == 2
    assert results.success == 1
    assert results.failed == 1
    assert results.status == "失敗"
