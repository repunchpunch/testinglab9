import pytest
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from pages.contact_page import ContactPage


@pytest.fixture(scope="session")
def driver():
    service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def contact_page(driver):
    page = ContactPage(driver)
    file_path = os.path.join(os.path.dirname(__file__), "..", "contact_form.html")
    driver.get(f"file://{os.path.abspath(file_path)}")
    return page


def test_positive_submission(contact_page):
    contact_page.fill_form(
        name="Иванов Иван Иванович",
        email="ivan@example.com",
        phone="+7 (999) 123-45-67",
        subject="Техническая поддержка"
    )
    contact_page.submit_form()

    assert contact_page.is_success_visible()
    assert "Форма успешно отправлена!" in contact_page.get_result_text()


def test_negative_submission_invalid_phone(contact_page):
    contact_page.fill_form(
        name="Петров Пётр Петрович",
        email="petr@mail.ru",
        phone="8-999-123-45-67",
        subject="Вопрос по оплате"
    )
    contact_page.submit_form()

    assert not contact_page.is_success_visible()
    result_text = contact_page.get_result_text()
    assert result_text == "" or "успешно" not in result_text.lower()