'''
Created on Dec 15, 2015

@author: itaraday
'''
from SBLocations import SBLocations 
from SBAdmin import SBAdmin 
from SBTax import SBTax 
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.keys import Keys
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup
import json

	
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
		self.SBTax = SBTax(self)
		with open('eventData.json') as data_file:
			self.eventData = json.load(data_file) 
	
	def getOrgs(self):
		return self.eventData.keys()

	#Helper functions
	def inputData(self, mytype, element, text):
		if mytype == 'id':
			elem = self.browser.find_element_by_id(element)
		elif mytype == "name":
			elem = self.browser.find_element_by_name(element)
		else:
			elem = ""			
		elem.clear()   
		elem.send_keys(text) 
	
	def clear(self, mytype, element):
		if mytype == 'id':
			elem = self.browser.find_element_by_id(element)
		elif mytype == "name":
			elem = self.browser.find_element_by_name(element)	
		elem.clear()	
		
	def wait(self, amount):
		self.browser.implicitly_wait(amount)
		
	def Ewait(self, amount, mytype, element):
		if mytype == "xpath":
			WebDriverWait(self.browser,amount).until(EC.presence_of_element_located((By.XPATH,element)))
			
	def select(self, mytype, element, value):
		if mytype == 'id':
			Select(self.browser.find_element_by_id(element)).select_by_visible_text(value)
	
	def fineElement(self, mytype, element):
		found = True
		try:
			if mytype == 'id':
				self.browser.find_element_by_id(element)
			if mytype == 'xpath':
				self.browser.find_element_by_xpath(element)
		except:
			found = False
		return found
		
	def makeAdminName(self, loc, prefix):
		return self.maindata.makeAdminName(loc, prefix)	 
		
	def getElemAttribute(self, mytype, element, attr):
		if mytype == 'xpath':
			return self.browser.find_element_by_xpath(element).get_attribute(attr)	
		elif mytype == 'id':
			return self.browser.find_element_by_id(element).get_attribute(attr)
			
	def getTRBlocks(self, table):
		TRows = self.browser.find_elements_by_xpath(table)
		values = []
		for tr in TRows[1:]:
			low = int(tr.find_elements(By.TAG_NAME, "td")[0].text)
			high = int(tr.find_elements(By.TAG_NAME, "td")[1].text)
			status = tr.find_elements(By.TAG_NAME, "td")[3].text
			values.append([low, high, status])
		return values
		
	
	def getOldNames(self, table, eq, myName = "Charity's Name"):
		self.maindata.resetOld()
		elem = self.getElemAttribute("id", table, 'innerHTML')
		soup = BeautifulSoup(elem, "lxml")
		locations = []
		for row in soup.find_all('tr'):
			locations.append(row.find_all('td')[eq].get_text())
		for loc in self.maindata.getLocations(myName = myName):
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
		elif mytype == 'xpath':
			self.browser.find_element_by_xpath(clickTo).click()

	def pageLoad(self, mytype, clickTo):
		with wait_for_page_load(self.browser):
			self.pageClick(mytype, clickTo)
											 
	def getLocations(self, mytype="all"):
		return self.maindata.getLocations(mytype)
	
	def getAttributeOne(self, loc, name):
		return self.maindata.getAttributeOne(loc, name)
	
	def setAttribute(self, loc, name, value):
		self.maindata.setAttribute(loc, name, value)

	def getText(self, mytype, element):
		if mytype == 'xpath':
			return self.browser.find_element_by_xpath(element).text
		
	def clickCheckboxes(self, mytype, element, check):
		if mytype == 'xpath':
			checkboxes = self.browser.find_elements_by_xpath(element)
		#go through all checkboxes on the page and make sure clicked or unclicked
		#check = NONE to unclick them 
		for box in checkboxes:
			if box.get_attribute("checked") != check:
				box.click()
	
	#SBLocation main functions
	def setup(self, maindata, username, password, org):
		self.maindata = maindata
		self.event = self.eventData[org]["new"]
		self.eventOld = self.eventData[org]["old"]
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
		self.SBAdmin.setupAdmin(self.event)
	
	def setupTR(self):
		self.SBTax.setupTR()
		self.SBLocations.enableTR(self.event)
		
	
