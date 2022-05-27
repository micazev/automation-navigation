import os
from Login import Login
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from Log import Log
import pandas as pd
from Try import Try


from NavigateIssues import NavigateIss
from TableIssuesDetails import ListIssues

from selenium.common.exceptions import StaleElementReferenceException

class Main(ListIssues, Login, NavigateIss):

    def __init__(self):
        Log.add("Iniciando automação")
        super().__init__()
        dir = os.getcwd()
        self.web = webdriver.Chrome(executable_path=dir + "\chromedriver.exe") 
        self.dt_create_issue = pd.read_excel('4_Input_CreateIssue.xlsx')
        self.SetSheet()
        self.Connect()
        

    def Connect(self):           
        self.web.get("https://fa-eueu-saasfaprod1.fa.ocs.oraclecloud.com")        
        self.web.maximize_window()
        Log.add("Página aberta")

    def SetSheet(self):
        # Verificar se colunas existem
        # Senão criar
        if 'Insert 1' not in self.dt_create_issue.columns:
            self.dt_create_issue.insert(0, "Insert 1", "", allow_duplicates = False)
        if 'Insert 2' not in self.dt_create_issue.columns:
            self.dt_create_issue.insert(1, "Insert 2", "", allow_duplicates = False)
        self.dt_create_issue.to_excel('4_Input_CreateIssue.xlsx', index = False)
    

if __name__ == "__main__":
    teste = Main()
    # LOGIN
    Try.catch(teste.LoginUserId())
    
    # NAVIGATION
    Try.catch(teste.ClickIssues())

    # FIRST INSERTION
    Try.catch(teste.GetCreateIssueDetail())

    time.sleep(10)