from asyncio.windows_events import NULL
from calendar import c
from cmath import nan
from operator import le
import time
from tracemalloc import start
from numpy import NaN
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import Select #dropdown
from selenium.webdriver.common.keys import Keys
from Log import Log
import re
from Try import Try
from selenium.common.exceptions import StaleElementReferenceException


class ListIssues():

    def __init__(self):
        self.keepGoing = True
        self.check = False
        self.menssagem = 'ok'

    def GetCreateIssueDetail(self):
            quantidadeDeTasks = len(self.dt_create_issue['Issue Name'])
            i = 0
            lista = []
            for c in range(0, quantidadeDeTasks, 1): 
                lista = []
                name = self.dt_create_issue['Issue Name'][c]
                if self.dt_create_issue['Insert 1'][c] == "ok":
                    Log.add(f"Já cadastrado: {name}")
                elif self.dt_create_issue['Insert 1'][c] == "":
                    description = self.dt_create_issue['Description'][c]
                    issue_type = self.dt_create_issue['Type'][c]
                    severity = self.dt_create_issue['Severity'][c]
                    issue_status = self.dt_create_issue['Status'][c]
                    comment = self.dt_create_issue['Comment'][c]
                    context_segment = self.dt_create_issue['Context Segment'][c]
                    wls_u = self.dt_create_issue['WLS_U'][c]
                    object_type = self.dt_create_issue['Object Type'][c]
                    related_object = self.dt_create_issue['Related Object for Issue'][c]
                    self.firstInsertion(name, description, issue_type, severity, issue_status, comment, object_type, related_object, wls_u)
                    # Inserir 
                    self.dt_create_issue.at[c, "Insert 1"] = self.menssagem
                    self.dt_create_issue.to_excel('4_Input_CreateIssue.xlsx', index = False)
                else:
                    Log.add(f"Verificar caso: {name}")    

                # SEGUNDA INSERCAO
                self.menssagem = "ok"
                if self.dt_create_issue['Insert 2'][c] == "ok":
                    Log.add(f"Já cadastrado completamente: {name}")
                elif self.keepGoing == False:
                    self.dt_create_issue.at[c, "Insert 2"] = "error"
                elif self.keepGoing:
                    requires_remediation = self.dt_create_issue['Requires Remediation'][c]
                    impact_cost = self.dt_create_issue['Impact Cost'][c]
                    recurrence = self.dt_create_issue['Likelyhood of Recurrence'][c]
                    remediation_cost = self.dt_create_issue['Remediation Cost'][c]
                    source = self.dt_create_issue['Source'][c]
                    remediation_plan = self.dt_create_issue['Remediation Plan'][c]
                    user_name = self.dt_create_issue['User Name (Security assignment)'][c]
                    self.secondInsertion(name, remediation_plan, user_name, requires_remediation)
                    #inserir ok
                    self.dt_create_issue.at[c, "Insert 2"] = self.menssagem
                else:
                    Log.add(f"Verificar caso: {name}")
                self.dt_create_issue.to_excel('4_Input_CreateIssue.xlsx', index = False)
                self.keepGoing = True
                self.menssagem = "ok"
                i += 1
            return

    def firstInsertion(self, name, description, issue_type, severity, issue_status, comment, object_type, related_object, wls_u):
        self.ClickIconCreate()
        time.sleep(3)
        # Dados básicos
        for p in range (0,5):
            try:
                Log.add(f"CRIAR {name}")
                self.Name(name)
                self.Description(description)
                self.IssueType(self.WichType(issue_type))
                self.Severity(self.WichSeverity(severity))
                self.IssueStatus(self.WichStatus(issue_status))
                self.Comment(comment)
                self.Checkerror()
            except StaleElementReferenceException:
                time.sleep(2)
                print('erro ao achar o elemento')
                self.menssagem = 'erro de cadastro'
                continue
            break

        # Dados related object
        if self.keepGoing == True:
            self.ObjectType(object_type, related_object)
            if self.keepGoing == True:
                Try.catch(self.IssueOpeningReason(wls_u), "issue opening reason")
                Try.catch(self.Save(), "save")
                print("finish")
                Log.add(f"SALVO {name}")
            else: 
                print("error")
                Log.add(f"ERROR {name}")
                self.menssagem = 'erro de related object'
                # cancel
                self.web.execute_script('document.querySelectorAll(".xrb")[1].click()')
                time.sleep(3)
        else:
            Log.add(f"Já havia cadastro: {name}")
            self.menssagem = 'já cadastrado'
            self.keepGoing = True
            # cancel
            self.web.execute_script('document.querySelectorAll(".xrb")[1].click()')
            time.sleep(3)

    def secondInsertion(self, name, remediation_plan, user_name, requires_remediation):
        Log.add(f"Busca por {name}")
        if requires_remediation == "Sim":
            print('Busca')
            self.Buscar(name)
            self.ClickCase(name)
            if self.keepGoing:
                Try.catch(self.Actions(), "actions")
                Try.catch(self.ClickEditar(), "editar")
                # Checar se esta checado
                self.CheckBox()
                print('Remediation Plan')
                Try.catch(self.ClickPlus(), "click plus")
                self.RemediationPlan(remediation_plan)
                print('submit')
                Try.catch(self.IssueSubmit(), "submit")
        Log.add("Tarefa finalizada")

    def ClickIconCreate(self):
        ## Clicar no mais +
        time.sleep(2)
        self.web.execute_script("document.querySelectorAll('.x1k6')[0].click()")
        time.sleep(2)

    def Name(self, name):
        print(f"Name {name}")
        self.web.execute_script(f'document.querySelectorAll(".x25")[0].value = "{name}"')  
        # while len(self.web.find_elements(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:pb1:it1::content"]')) < 1:
        #     time.sleep(1)
        # self.web.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:pb1:it1::content"]').send_keys(name)

    def Description(self, description):
        print(f"Description {description}")
        self.web.execute_script(f'document.querySelectorAll(".x25")[1].value = "{description}"')  
        # while len(self.web.find_elements(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:pb1:it2::content"]')) < 1:
        #     time.sleep(1)
        # self.web.find_element(By.XPATH, '//*[@id="btnActive"]').send_keys(description)

    def IssueType(self, issue_type):
        print(f"Issue Type {issue_type}")
        self.web.execute_script(f'document.querySelectorAll(".x2h")[0].value = "{issue_type}"')       

    def Severity(self, severity):
        print(f"Severity {severity}")
        self.web.execute_script(f'document.querySelectorAll(".x2h")[1].value = "{severity}"')  

    def IssueStatus(self, issue_status):
        print(f"Issue Status {issue_status}")
        self.web.execute_script(f'document.querySelectorAll(".x2h")[2].value = "{issue_status}"')  

    def Comment(self, comment):
        print(f"Comment {comment}")
        self.web.execute_script(f'document.querySelectorAll(".x25")[2].value = "{comment}"')  
        # while len(self.web.find_elements(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:pb1:it3::content"]')) < 1:
        #     time.sleep(1)
        # self.web.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:pb1:it3::content"]').send_keys(comment)
          
    def WichType(self, type):
        if type == "Financial":
            return 1
        if type == "Operational":
            return 2
 
    def WichSeverity(self, severity):
        if severity == "Control Implementation":
            return 1
        if severity == "Medium Deficiency":
            return 2
        if severity == "Minor Deficiency":
            return 3
        if severity == "Significant Deficiency":
            return 4

    def WichStatus(self, issue_status):
        if issue_status == "In Remediation":
            return 0
        if issue_status == "On Hold":
            return 1
        if issue_status == "Open":
            return 2
    
    def WichObject(self, object_type):
        if object_type == "Process":
            return 0
        if object_type == "Risk":
            return 1
        if object_type == "Control":
            return 2


# ADITIONAL INFORMATION
    def ContextSegment(self, context_segment):
        print(f"Context Segment {context_segment}")
        while len(self.web.find_elements(By.XPATH, '//*[@id="_FOpt1:_FOr1:0:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:sdh2:df1_IssueDFFIterator__FLEX_Context__FLEX_EMPTY::content"]')) < 1:
            time.sleep(1)
        dropDownSelect = Select(self.web.find_element(By.XPATH, '//*[@id="_FOpt1:_FOr1:0:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:sdh2:df1_IssueDFFIterator__FLEX_Context__FLEX_EMPTY::content"]')) 
        time.sleep(1)
        dropDownSelect.select_by_visible_text(context_segment)

        time.sleep(2)

    def IssueOpeningReason(self, wls_u):
        print(f"Issue Opening Reasonn {wls_u}")
        ## Clique para abrir
        while len(self.web.find_elements(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:sdh2:df1_IssueDFFIteratorissueOpeningReason__FLEX_EMPTY::lovIconId"]')) < 1:
            time.sleep(1)
        self.web.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:sdh2:df1_IssueDFFIteratorissueOpeningReason__FLEX_EMPTY::lovIconId"]').click()
        time.sleep(3)

        ## Clique para procurar
        while len(self.web.find_elements(By.LINK_TEXT, 'Search...')) < 1:
            time.sleep(1)
        self.web.find_element(By.LINK_TEXT, 'Search...').click()
        time.sleep(1)
        
        ## Procurar
        while len(self.web.find_elements(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:sdh2:df1_IssueDFFIteratorissueOpeningReason__FLEX_EMPTY::_afrLovInternalQueryId:value00::content"]')) < 1:
            time.sleep(1)
        element = self.web.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:sdh2:df1_IssueDFFIteratorissueOpeningReason__FLEX_EMPTY::_afrLovInternalQueryId:value00::content"]')
        element.send_keys(wls_u)
        element.send_keys(Keys.RETURN)
        time.sleep(1)

        ## Selecionar
        while len(self.web.find_elements(By.XPATH, '/html/body/div[1]/form/div[2]/div[2]/div[1]/div[1]/table/tbody/tr/td/div/div/table/tbody/tr[2]/td[2]/div/div[2]/div/div/div/div/div[2]/table/tbody/tr/td[2]')) < 1:
            time.sleep(1)
        self.web.find_element(By.XPATH, '/html/body/div[1]/form/div[2]/div[2]/div[1]/div[1]/table/tbody/tr/td/div/div/table/tbody/tr[2]/td[2]/div/div[2]/div/div/div/div/div[2]/table/tbody/tr/td[2]').click()

        ## Confirmar
        while len(self.web.find_elements(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:sdh2:df1_IssueDFFIteratorissueOpeningReason__FLEX_EMPTY::lovDialogId::ok"]')) < 1:
            time.sleep(1)
        self.web.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:sdh2:df1_IssueDFFIteratorissueOpeningReason__FLEX_EMPTY::lovDialogId::ok"]').click()
        time.sleep(3)

    def Checkerror(self):
        self.web.execute_script('document.querySelectorAll(".xrb")[4].click()')
        time.sleep(3)
        if len(self.web.find_elements(By.CLASS_NAME, 'x34p')) > 4:
            time.sleep(1)
        else: 
            self.keepGoing = False
            self.menssagem = 'mensagem de erro ao cadastrar'
            # cancel
            self.web.execute_script('document.querySelectorAll(".xrb")[1].click()')
            time.sleep(3)
        return self.keepGoing



    def ObjectType(self, object_type, related_object):
        object_type += " (0)"
        print(f"Object Type {object_type}")
        dropDownSelect = Select(self.web.find_element(By.ID, 'pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:pb3:soc11::content')) 
        dropDownSelect.select_by_visible_text(object_type)
        time.sleep(2)
        # elemento = self.web.execute_script(f'document.querySelectorAll(".x2h")[4]')
        # self.web.execute_script(f'document.querySelectorAll(".x2h")[4].value = "{object_type}"')    
        # elemento.send_keys(Keys.RETURN)      
        time.sleep(2)
        # click +
        self.web.execute_script('document.querySelectorAll(".x1k6")[3].click()')
        time.sleep(2)
        # type to search
        while len(self.web.find_elements(By.CLASS_NAME, 'x25')) < 1:
            time.sleep(1)
        elemento = self.web.find_element(By.CLASS_NAME, 'x25')
        elemento.clear()
        elemento.send_keys(related_object)
        elemento.send_keys(Keys.RETURN)
        time.sleep(3)
        try:
            self.web.find_element(By.CLASS_NAME, 'xem').click()
        except:
            self.keepGoing = False
            Log.add(f"ITEM {related_object} NAO ENCONTRADO")
            print('item não encontrado')
        time.sleep(3)

        ## voltar
        self.web.execute_script('document.querySelectorAll(".xkn")[11].click()')
        time.sleep(2)
        return self.keepGoing

    def Save(self):
        ## submit
        print('salvar')
        time.sleep(2)
        while len(self.web.find_elements(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:cmi3"]/a')) < 1:
            time.sleep(1)
        self.web.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:1:up1:UPsp1:cmi3"]/a').click()

    # SEGUNDA INSERCAO
    
    def Buscar(self, name):
        # Buscar o nome
        while len(self.web.find_elements(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:_FOTr1:1:up1:UPsp1:ls1:_LSSF::content"]')) < 1:
            time.sleep(1)
        elemento = self.web.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:_FOTr1:1:up1:UPsp1:ls1:_LSSF::content"]')
        elemento.clear()
        time.sleep(1)
        elemento.send_keys(name)
        elemento.send_keys(Keys.RETURN)
        time.sleep(2)

    def ClickCase(self, name):
        try:
            time.sleep(2)
            self.web.find_element(By.LINK_TEXT, name).click()
            time.sleep(2)
        except:
            self.keepGoing = False
            Log.add(f"ITEM {name} NAO ENCONTRADO")
            print('item não encontrado')
            self.menssagem = 'item não encontrado'
        time.sleep(3)

    def Actions(self):
        # Abrir opcoes
        while len(self.web.find_elements(By.CLASS_NAME, 'xut')) < 1:
            time.sleep(1)
        self.web.find_element(By.CLASS_NAME, 'xut').click()
        time.sleep(2)

    def ClickEditar(self):
        # Issue Details
        while len(self.web.find_elements(By.CLASS_NAME, 'xnx')) < 1:
            time.sleep(1)
        self.web.find_element(By.CLASS_NAME, 'xnx').click()
        time.sleep(2)

    def CheckBox(self):   
        # Clicar em Requer correção
        while len(self.web.find_elements(By.CLASS_NAME, 'x17e')) < 1:
            time.sleep(1)
        # self.web.find_element(By.CLASS_NAME, 'x17e').send_keys(Keys.RETURN)
        self.web.find_element(By.CLASS_NAME, 'x17e').click()
        time.sleep(3)    

    def OutrasInfos(self, recurrence, source,remediation_cost,impact_cost):
        # Probabilidade de recorrência
        # //*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:2:up1:UPsp1:pb1:soc6::content"]
        self.web.execute_script(f'document.querySelectorAll(".x2h")[2].value = "{recurrence}"')

        # Impact Cost
        while len(self.web.find_elements(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:2:up1:UPsp1:pb1:it4::content"]')) < 1:
            time.sleep(1)
        self.web.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:2:up1:UPsp1:pb1:it4::content"]').send_keys(impact_cost)
        time.sleep(2) 

        # Remediation Cost
        while len(self.web.find_elements(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:2:up1:UPsp1:pb1:it55::content"] ')) < 1:
            time.sleep(1)
        self.web.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FOSritemNode_financial_reporting_compliance_issues:0:MAnt2:2:up1:UPsp1:pb1:it55::content"] ').send_keys(remediation_cost)
        time.sleep(2) 
               
        # Source
        self.web.execute_script(f'document.querySelectorAll(".x2h")[2].value = "{source}"')

    def ClickPlus(self):
        # Clicar + em Remediation Plans
        time.sleep(2)
        self.web.execute_script(f'document.querySelectorAll(".xrb")[8].click()')
        time.sleep(3)

    def RemediationPlan(self, remediation_plan):
        for p in range (0,5):
            try:
                ## type to search
                while len(self.web.find_elements(By.CLASS_NAME, 'x25')) < 1:
                    time.sleep(1)
                elemento = self.web.find_element(By.CLASS_NAME, 'x25')
                elemento.clear()
                elemento.send_keys(remediation_plan)
                elemento.send_keys(Keys.RETURN)
                time.sleep(5)
                try:
                    self.web.find_element(By.CLASS_NAME, 'xem').click()
                except:
                    self.keepGoing = False
                    Log.add(f"ITEM {related_object} NAO ENCONTRADO")
                    print('item não encontrado')
                    time.sleep(3)
                ## voltar
                Try.catch(self.RemediationVoltar(), "voltar") 
            except StaleElementReferenceException:
                time.sleep(2)
                print('erro ao achar o elemento')
                continue
            break

    def RemediationVoltar(self):
        self.web.execute_script('document.querySelectorAll(".xkn")[11].click()')
        time.sleep(2)   

    def SecurityAssignment(self, user_name):
        # ADD
        time.sleep(3)
        self.web.execute_script(f'document.querySelectorAll(".xeq")[0].click()')
        time.sleep(2)

        # Checar se já esta atribuido
        amountUsers = self.web.execute_script('return document.querySelectorAll(".x2zj").length')
        listaUsers = []
        for i in range(0, amountUsers, 1): 
            nome = self.web.execute_script(f'return document.querySelectorAll(".x2zj")[{i}].outerText')
            nome = re.sub('[^A-Za-z0-9]+', '', nome)
            listaUsers.append(nome)
        print(listaUsers)
        stripAssignament = re.sub('[^A-Za-z0-9]+', '', user_name).upper()
        if stripAssignament == "EMILIOBRUN":
            stripAssignament = "EMILIOJUNIOR"
            
        if stripAssignament in listaUsers:
            Log.add(f"Usuário {user_name} já atribuido")
            print('usário já atribuído')
        else: 
            self.web.execute_script('document.querySelectorAll(".xeq")[1].click()')
            time.sleep(2)
            self.web.find_element(By.CLASS_NAME, 'xpe').click()
            time.sleep(2)
            self.web.find_element(By.CLASS_NAME, 'xpe').send_keys(f"{user_name}")
            time.sleep(2)
            self.web.find_element(By.CLASS_NAME, 'xpe').send_keys(Keys.ARROW_DOWN)
            time.sleep(2)
            self.web.find_element(By.CLASS_NAME, 'xpe').send_keys(Keys.RETURN)
            time.sleep(2)
            # self.web.execute_script(f'document.querySelectorAll(".x17b")[1].click()')
            self.web.execute_script(f'document.querySelectorAll(".xeq.p_AFTextOnly")[1].click()')
            Log.add(f"Usuário {user_name} atribuido")
    
        # Voltar
        self.web.execute_script('document.querySelectorAll(".xkn")[11].click()')

    def IssueSubmit(self):
        self.web.find_element(By.CLASS_NAME, 'x1k4').click()   
        time.sleep(1)
        self.web.execute_script('document.querySelectorAll(".xnx")[19].click()')
        # Voltar
        self.web.execute_script('document.querySelectorAll(".xkn")[11].click()')
