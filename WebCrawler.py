'''
Created on Dec 15, 2015

@author: itaraday
'''
from SBLocations import SBLocations 
from SBAdmin import SBAdmin 
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.keys import Keys
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup

def getOrgs():
    return ['ps', 'Scotiabank', 'Bluenose', 'SCCO', 'misscharitychallenge']

        
@contextmanager
def wait_for_page_load(self, timeout=60):
    old_page = self.find_element_by_tag_name('html')
    yield
    WebDriverWait(self, timeout).until(staleness_of(old_page))


    
        
class crawler:    
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.SBLocations = SBLocations(self)
        self.SBAdmin = SBAdmin(self)
        
    def inputData(self, mytype, element, text):
        if mytype == 'id':
            elem = self.browser.find_element_by_id(element)
        elif mytype == "name":
            elem = self.browser.find_element_by_name(element)
        else:
            elem = ""
            
        elem.clear()   
        elem.send_keys(text) 
        
    def wait(self, amount):
        self.browser.implicitly_wait(amount)
        
    def Ewait(self, amount, mytype, element):
        if mytype == "xpath":
            WebDriverWait(self.browser,amount).until(EC.presence_of_element_located((By.XPATH,element)))
            
    def select(self, mytype, element, value):
        if mytype == 'id':
            Select(self.browser.find_element_by_id(element)).select_by_visible_text(value)
    
    def makeAdminName(self, loc):
        return self.maindata.makeAdminName(loc)  
        
    def getOldNames(self, table, eq):
        elem = self.browser.find_element_by_id(table)
        soup = BeautifulSoup(elem.get_attribute('innerHTML') )
        locations = []
        for row in soup.find_all('tr'):
            locations.append(row.find_all('td')[eq].get_text())
        for loc in self.maindata.getLocations():
            oldratio = 70
            ratio = 0
            myloc = ""
            for removedloc in locations:
                ratio = fuzz.ratio(loc, removedloc)
                if ratio > oldratio:
                    oldratio = ratio
                    myloc = removedloc
                    self.maindata.setAttribute(loc, "old name", myloc)        

    def quit(self):
        self.browser.close()
   
    def pageClick(self, mytype, clickTo):
        if mytype == "id":
            self.browser.find_element_by_id(clickTo).click()
        elif mytype == "text":
            self.browser.find_element_by_link_text(clickTo).click()

    def pageLoad(self, mytype, clickTo):
        with wait_for_page_load(self.browser):
            self.pageClick(mytype, clickTo)
                                             
    def getLocations(self, mytype="all"):
        return self.maindata.getLocations(mytype)
    
    def getAttributeOne(self, loc, name):
        return self.maindata.getAttributeOne(loc, name)
    
    def setAttribute(self, loc, name, value):
        self.maindata.setAttribute(loc, name, value)

    def setup(self, maindata, username, password, org):
        self.maindata = maindata
        if org == 'Bluenose':
            self.event = '2016 Scotiabank Charity Challenge at the Scotiabank Blue Nose Marathon'
        elif org == 'Scotiabank' or org == 'ps':
            self.event = '2016 Scotiabank Charity Challenge at the Scotiabank Calgary Marathon'
        #logging in
        with wait_for_page_load(self.browser):
            self.browser.get("https://admin.e2rm.com")
        self.inputData("id", "textOrganizationID", org)
        self.inputData("id", "textUsername", username)
        self.inputData("id", "textPassword", password)
        self.browser.find_element_by_id('buttonSubmit').click()
        
    def setupLocations(self):    
        self.SBLocations.setupLocations(self.event)
                      
    def setupAdmin(self):
        self.SBAdmin.setupAdmin()
        
    
