from unittest.mock import MagicMock, patch
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import modules.selenium_actions as sa


# ============================================================
# 1. 正常系テスト（success=True）
# ============================================================
def test_register_one_success():
    driver = MagicMock()
    driver.get.return_value = None

    fake_element = MagicMock()
    fake_element.tag_name = "select"
    driver.find_element.return_value = fake_element
    driver.find_elements.return_value = [fake_element]

    with patch(
        "selenium.webdriver.support.ui.WebDriverWait.until", return_value=fake_element
    ), patch("modules.selenium_actions.Select") as MockSelect:

        MockSelect.return_value = MagicMock()

        result = sa.register_one(
            driver, {"age": 20, "gender": "男性", "region": "関東", "food": "寿司"}
        )

    assert result["success"] is True
    assert result["stage"] is None
    assert result["message"] is None


# ============================================================
# 2. input Timeout 発生（stage="input"）
# ============================================================
def test_register_one_timeout_input():

    driver = MagicMock()

    # age_input などで timeout を発生させる
    with patch.object(sa, "wait", side_effect=TimeoutException("Timeout!!")):
        result = sa.register_one(
            driver, {"age": 20, "gender": "男性", "region": "関東", "food": "寿司"}
        )

    assert result["success"] is False
    assert result["stage"] == "input"
    assert "Timeout" in result["message"]


# ============================================================
# 3. confirm Timeout（stage="confirm"）
# ============================================================
def test_register_one_confirm_timeout():
    driver = MagicMock()

    fake_element = MagicMock()
    fake_element.tag_name = "select"
    driver.find_element.return_value = fake_element
    driver.find_elements.return_value = [fake_element]

    # confirm のみ timeout させる
    def fake_wait(driver, by, value, timeout=10):
        if by == By.XPATH and "回答ありがとうございました" in value:
            raise TimeoutException("confirm timeout")
        return fake_element

    with patch("modules.selenium_actions.wait", side_effect=fake_wait), patch(
        "modules.selenium_actions.Select"
    ) as MockSelect:

        MockSelect.return_value = MagicMock()

        result = sa.register_one(
            driver,
            {"age": 20, "gender": "男性", "region": "関東", "food": "寿司"},
        )

    assert result["success"] is False
    assert result["stage"] == "confirm"
    assert "完了ページが表示されません" in result["message"]


# ============================================================
# 4. unexpected error（その他の例外）
# ============================================================
def test_register_one_unexpected_error():

    driver = MagicMock()

    # region 取得時に unknown error 発生
    def fake_wait(driver, by, value, timeout=10):
        if value == "region":
            raise Exception("Unknown error")
        return MagicMock()

    with patch.object(sa, "wait", side_effect=fake_wait):

        result = sa.register_one(
            driver, {"age": 20, "gender": "男性", "region": "関東", "food": "寿司"}
        )

    assert result["success"] is False
    assert result["stage"] == "unexpected"
