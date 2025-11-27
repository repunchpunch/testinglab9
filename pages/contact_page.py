from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ContactPage(BasePage):
    FULL_NAME = (By.CSS_SELECTOR, "[data-test='fullName']")
    EMAIL = (By.CSS_SELECTOR, "[data-test='email']")
    PHONE = (By.CSS_SELECTOR, "[data-test='phone']")
    SUBJECT = (By.CSS_SELECTOR, "[data-test='subject']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "[data-test='submitButton']")
    FORM_RESULT = (By.ID, "formResult")
    SUCCESS_MESSAGE = (By.XPATH, "//div[@id='formResult' and contains(@class, 'success')]")

    def fill_form(self, name, email, phone, subject):
        self.type_text(self.FULL_NAME, name)
        self.type_text(self.EMAIL, email)
        self.type_text(self.PHONE, phone)
        self.driver.find_element(*self.SUBJECT).send_keys(subject)
    
    def submit_form(self):
        self.click(self.SUBMIT_BUTTON)

    def get_result_text(self):
        return self.find_element(self.FORM_RESULT).text

    def is_success_visible(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except:
            return False