from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)


def wait(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def wait_all(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((by, value))
    )


def register_one(driver, row):
    try:
        # ===== stage: input =====
        # driver.get("https://testsite-production-df80.up.railway.app/")
        driver.get("http://127.0.0.1:8000/")

        age_input = wait(driver, By.NAME, "age")
        age_input.clear()
        age_input.send_keys(row["age"])

        gender_buttons = wait_all(driver, By.NAME, "gender")
        for radio in gender_buttons:
            if radio.get_attribute("value") == row["gender"]:
                radio.click()
                break

        region_element = wait(driver, By.NAME, "region")
        select = Select(region_element)
        select.select_by_visible_text(row["region"])

        food_input = wait(driver, By.NAME, "food")
        food_input.clear()
        food_input.send_keys(row["food"])

        # ===== stage: submit =====
        submit_btn = wait(driver, By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()

        # ===== stage: confirm =====
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h1[contains(text(), '回答ありがとうございました！')]")
                )
            )
            return {
                "success": True,
                "stage": None,
                "message": None,
            }

        except TimeoutException:
            return {
                "success": False,
                "stage": "confirm",
                "message": "完了ページが表示されません",
            }

    except TimeoutException as e:
        return {
            "success": False,
            "stage": "input",
            "message": f"要素待機 Timeout: {str(e)}",
        }

    except NoSuchElementException as e:
        return {
            "success": False,
            "stage": "input",
            "message": f"要素が見つかりません: {str(e)}",
        }

    except WebDriverException as e:
        return {
            "success": False,
            "stage": "unexpected",
            "message": f"ブラウザエラー: {str(e)}",
        }

    except Exception as e:
        return {
            "success": False,
            "stage": "unexpected",
            "message": f"その他のエラー: {str(e)}",
        }
