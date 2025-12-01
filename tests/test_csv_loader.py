import pandas as pd
from modules.csv_loader import load_csv


def test_load_csv(tmp_path):
    # テスト
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "age,gender,region,food\n0,男性,関東,焼肉\n1,女性,北海道,なし", encoding="utf-8"
    )

    df = load_csv(csv_file)

    # 検証
    assert len(df) == 2
    assert df.loc[0, "age"] == 0
    assert df.loc[1, "food"] == "なし"
