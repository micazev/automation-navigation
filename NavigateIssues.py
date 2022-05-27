import time
from selenium.webdriver.common.by import By
from datetime import datetime

from Log import Log


class NavigateIss():

    def __init__(self):
        pass

    def ClickIssues(self):
        while len(self.web.find_elements(By.ID, "pt1:_UIShome")) < 1:
            time.sleep(1)
        self.web.find_element(By.ID, "pt1:_UIShome").click()
        
        while len(self.web.find_elements(By.ID, 'groupNode_risk_management')) < 1: 
            time.sleep(1)
        self.web.find_element(By.ID, 'groupNode_risk_management').click()

        while len(self.web.find_elements(By.LINK_TEXT, 'Issues')) < 1:
            time.sleep(1)
        self.web.find_element(By.LINK_TEXT, 'Issues').click()

        while len(self.web.find_elements(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:_FOTsdiIssueManage_itemNode::icon"]')) < 1:
            time.sleep(1)
        self.web.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:_FOTsdiIssueManage_itemNode::icon"]').click()
        time.sleep(2)

        Log.add("Navegação até área issue")