import pandas as pd

gender = ["男性", "女性", "その他"]
region = ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州", "日本以外"]


def validation_check(row):
    message = None
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
    return message
