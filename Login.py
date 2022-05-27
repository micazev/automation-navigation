import time
from selenium.webdriver.common.by import By
from datetime import datetime
from Log import Log


class Login():

    def __init__(self):
        pass
    
    def LoginUserId(self):
        while len(self.web.find_elements(By.XPATH, '//*[@id="userid"]')) < 1:
            time.sleep(1)

        self.web.find_element(By.XPATH, '//*[@id="userid"]').send_keys("integration.evope")

        while len(self.web.find_elements(By.XPATH, "/html/body/div[5]/form/div[2]/input[2]")) < 1 :
            time.sleep(1)

        self.web.find_element(By.XPATH, "/html/body/div[5]/form/div[2]/input[2]").send_keys("Oracle123")

        while len(self.web.find_elements(By.XPATH, '//*[@id="btnActive"]')) < 1:
            time.sleep(1)
        self.web.find_element(By.XPATH, '//*[@id="btnActive"]').click()
        time.sleep(2)


        Log.add("Login realizado")