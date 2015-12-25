'''
Created on Dec 15, 2015

@author: itaraday
'''
from SBLocations import SBLocations 
from SBAdmin import SBAdmin 
from SBTax import SBTax 
from SBPledge import SBPledge 
from SBPages import SBPages 
from SBEmail import SBEmail
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
import urllib
from urlparse import urlparse, parse_qs
	
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
		self.SBPages = SBPages(self)
		self.SBEmail = SBEmail(self)
		self.SBPledge = SBPledge(self)
		with open('eventData.json') as data_file:
			self.eventData = json.load(data_file) 
	
	def getOrgs(self):
		return self.eventData.keys()

	#Helper functions
	def inputData(self, mytype, element, text, clear=True):
		if mytype == 'id':
			elem = self.browser.find_element_by_id(element)
		elif mytype == "name":
			elem = self.browser.find_element_by_name(element)
		elif mytype == "tag":
			elem = self.browser.find_element_by_tag_name(element)
		else:
			return			
		if clear:
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
			WebDriverWait(self.browser,amount).until(EC.visibility_of_element_located((By.XPATH,element)))
		elif mytype == "id":
			WebDriverWait(self.browser,amount).until(EC.visibility_of_element_located((By.ID,element)))
			
	def select(self, mytype, element, value):
		if mytype == 'id':
			Select(self.browser.find_element_by_id(element)).select_by_visible_text(value)
	
	def selectLast(self, mytype, element):
		if mytype == 'id':
			elem = Select(self.browser.find_element_by_id(element))
		else:
			return
		selectLen = len(elem.options)
		elem.select_by_index(selectLen-1)
	
	def fineElement(self, mytype, element):
		found = True
		try:
			if mytype == 'id':
				self.browser.find_element_by_id(element)
			elif mytype == 'xpath':
				self.browser.find_element_by_xpath(element)
			elif mytype == 'partial':
				self.browser.find_element_by_partial_link_text(element)
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
		
	
	def stealImage(self, mytype, element, name):
		src = self.getElemAttribute(mytype, element, 'src')
		saveas = self.filepath + "/" + name
		urllib.urlretrieve(src, saveas)
		
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
	
	def newTab(self):
		self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') 
		
	def closeTab(self):
		self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w') 
	
	
	def pageClick(self, mytype, clickTo):
		if mytype == "id":
			self.browser.find_element_by_id(clickTo).click()
		elif mytype == "text":
			self.browser.find_element_by_link_text(clickTo).click()
		elif mytype == 'xpath':
			self.browser.find_element_by_xpath(clickTo).click()
		elif mytype == 'partial':
				self.browser.find_element_by_partial_link_text(clickTo).click()

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
			if (box.get_attribute("checked") != check) and (box.is_displayed()):
				box.click()
	
	def goToUrl(self, url):
		self.browser.get(url)
		
	def writeInIFrame(self, mytypeFrame, frameElement, mytype, element, text):
		if mytypeFrame == 'xpath':
			driver = self.browser.find_element_by_xpath(frameElement)
		self.browser.switch_to_frame(driver)
		self.inputData(mytype, element, text)
		self.browser.switch_to_default_content()
		
	def getUrl(self):
		return self.browser.current_url
	
	def cleanURL(self, url):
		parse = urlparse(url)
		query = parse_qs(parse.query)
		url = parse.scheme +"://" + parse.netloc + parse.path +"?"
		for key in query:
			if not key == "Referrer":
				url = url + key +"=" + query[key][0] + "&"
		return url[:-1]
		
	def getIDs(self):
		myIDS = {
				"Location Page": "locationID",
				"Personal Page": "registrationID",
				"Donation Page": "SPID"
				}
		for loc in self.getLocations():
			for key in myIDS:
				URL = self.getAttributeOne(loc, key)
				parse = urlparse(URL)
				qs = parse_qs(parse.query)
				self.setAttribute(loc, myIDS[key], qs[myIDS[key]])
			
		
	#SBLocation main functions
	def setup(self, maindata, username, password, org, filepath):
		self.maindata = maindata
		self.event = self.eventData[org]
		self.filepath = filepath
		self.username = username
		#logging in
		with wait_for_page_load(self.browser):
			self.goToUrl("https://admin.e2rm.com")
		self.inputData("id", "textOrganizationID", org)
		self.inputData("id", "textUsername", username)
		self.inputData("id", "textPassword", password)
		self.browser.find_element_by_id('buttonSubmit').click()
		
	def setupLocations(self):	 
		self.SBLocations.setupLocations(self.event)
					
	def execute_script(self, script):
		self.browser.execute_script(script)
		
	def setupAdmin(self):
		self.SBAdmin.setupAdmin(self.event)
	
	def setupTR(self):
		self.SBTax.setupTR()
		self.SBLocations.enableTR(self.event)
		
	def setupPages(self):
		self.SBLocations.getLocURL(self.event)
		self.SBPages.findLogin()
		self.SBPages.setuppages()
		self.getIDs()
		self.SBLocations.finishDesc(self.event)
		self.SBPages.setCharityUDF(self.event)
	
	def setupPledge(self):
		self.SBLocations.goToEvent(self.event)
		self.SBPledge.setupPledge()
		
	def setupEmail(self):
		self.SBLocations.goToEvent(self.event)
		self.SBEmail.setupEmail()
	
	def Done(self):
		self.maindata.done(self.username)