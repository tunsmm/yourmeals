# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time, unittest

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login/")
        driver.find_element(By.LINK_TEXT, u"Зарегистрироваться").click()
        driver.get("http://127.0.0.1:8000/signup/")
        driver.find_element(By.ID, "id_email").click()
        driver.find_element(By.ID, "id_email").clear()
        driver.find_element(By.ID, "id_email").send_keys("newmail@mail.ru")
        time.sleep(1)
        driver.find_element(By.ID, "id_name").clear()
        driver.find_element(By.ID, "id_name").send_keys(u"Пример")
        time.sleep(1)
        driver.find_element(By.ID, "id_age").clear()
        driver.find_element(By.ID, "id_age").send_keys("423")
        time.sleep(1)
        driver.find_element(By.ID, "id_weight").clear()
        driver.find_element(By.ID, "id_weight").send_keys("2351")
        time.sleep(1)
        driver.find_element(By.ID, "id_height").clear()
        driver.find_element(By.ID, "id_height").send_keys("1220")
        time.sleep(1)
        driver.find_element(By.ID, "id_strategy").click()
        Select(driver.find_element(By.ID, "id_strategy")).select_by_visible_text(u"Набор веса")
        time.sleep(1)
        # driver.find_element(By.ID, "(.//*[normalize-space(text()) and normalize-space(.)='*'])[7]/following::div[1]").click()
        time.sleep(1)
        Select(driver.find_element(By.ID, "id_gender")).select_by_visible_text(u"Мужчина")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        driver.find_element(By.ID, "id_age").clear()
        driver.find_element(By.ID, "id_age").send_keys("103")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        driver.find_element(By.ID, "id_weight").click()
        driver.find_element(By.ID, "id_weight").clear()
        driver.find_element(By.ID, "id_weight").send_keys("251")
        time.sleep(1)
        driver.find_element(By.ID, "id_age").click()
        driver.find_element(By.ID, "id_age").clear()
        driver.find_element(By.ID, "id_age").send_keys("203")
        time.sleep(1)
        driver.find_element(By.ID, "id_weight").click()
        driver.find_element(By.ID, "id_weight").clear()
        driver.find_element(By.ID, "id_weight").send_keys("151")
        time.sleep(1)
        driver.find_element(By.ID, "id_height").click()
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        driver.find_element(By.ID, "id_age").clear()
        driver.find_element(By.ID, "id_age").send_keys("63")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        driver.find_element(By.ID, "id_height").clear()
        driver.find_element(By.ID, "id_height").send_keys("190")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        driver.get("http://127.0.0.1:8000/login/")
        driver.find_element(By.ID, "id_email").click()
        driver.find_element(By.ID, "id_email").clear()
        driver.find_element(By.ID, "id_email").send_keys("newmail@mail.ru")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        driver.get("http://127.0.0.1:8000/user/")
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
