#from WebCrawler import crawler
import pandas as pd
import time

class SBPages():

	def __init__(self, crawler):
		self.crawler = crawler
	
	def GoToRelationships(self):
		self.crawler.pageLoad("id", "ucBodyHead_hyperlinkRelationshipsTab")
		
	def findLogin(self):
		self.GoToRelationships()
		for loc in self.crawler.getLocations():
			regID = self.crawler.getAttributeOne(loc, "oldRegID")
			if not pd.isnull(regID):
				#regID = 2494748
				regID = int(regID)
				self.crawler.inputData("id", "textRegistrationId", regID)
				self.crawler.pageLoad("id", "buttonRegistrationSearch")
				self.crawler.pageLoad("xpath", '//table[@id="datagridRegistrantsResults"]//a')
				username = self.crawler.getText('xpath', '''//td[contains(text(), "Username")]
															/following-sibling::td''')
				self.crawler.inputData("id", "textPassword", username)
				self.crawler.inputData("id", "textPasswordConfirm", username)
				self.crawler.setAttribute(loc, "Direct Donation Admin Username", username)
				self.crawler.setAttribute(loc, "Direct Donation Admin Password", username)
				self.crawler.pageLoad("id", "buttonSubmitPwd")
				self.GoToRelationships()
				
	def setCharityUDF(self, event):
		self.GoToRelationships()
		for loc in self.crawler.getLocations():
			regID = int(self.crawler.getAttributeOne(loc, "registrationID"))
			self.crawler.inputData("id", "textRegistrationId", regID)
			self.crawler.pageLoad("id", "buttonRegistrationSearch")
			self.crawler.pageLoad("xpath", '//table[@id="datagridRegistrantsResults"]//a')
			self.crawler.pageLoad("xpath", '''//td[contains(text(), "'''+event+'''")]
															/following-sibling::td[4]
															//input[@type="image"]''')
			self.crawler.pageLoad("id", "hyperlinkEditRegistrantEventSurveyQuestions")
			self.crawler.clickCheckboxes("xpath", '''//div[contains(text(), "(Admin only)")]
													/following-sibling::table
													//input[@type="checkbox"]''', 'true')
			self.crawler.pageLoad("id", "buttonSubmit")
			self.GoToRelationships()
			
				
	def RegV2(self, loc, username, newUser):
		self.crawler.Ewait(20, "id", "registrationTypeForm")
		self.crawler.pageClick("id", "individualParticipantTypeButton")
		
		self.crawler.Ewait(20, "id", "contactForm")
		try:
			self.crawler.inputData("id", "BusinessTitle", "charity")
		except:
			pass
		self.crawler.inputData("id", "FirstName", loc)
		self.crawler.inputData("id", "LastName", "Donations")
		self.crawler.inputData("id", "AddressLine1", self.crawler.getAttributeOne(loc, "address"))
		self.crawler.inputData("id", "City", self.crawler.getAttributeOne(loc, "city"))
		self.crawler.select("id", "CAProvince", self.crawler.getAttributeOne(loc, "province"))
		self.crawler.inputData( "id", "PostalCode", self.crawler.getAttributeOne(loc, "postal code"))
		self.crawler.inputData("id", "EmailAddress", "scotiabankgroupcharitychallenge@artez.com")
		self.crawler.inputData("id", "EmailAddressConfirm", "scotiabankgroupcharitychallenge@artez.com")	 
		if newUser:
			self.crawler.inputData("id", "LoginName", username)
			self.crawler.inputData("id", "Password", username)
			self.crawler.inputData("id", "PasswordConfirm", username)
		self.crawler.pageClick("id", "contactNextButton2")
		
		self.crawler.Ewait(20, "id", "additionalInfo")
		self.crawler.inputData("id", "FundraisingGoal", "")
		self.crawler.clickCheckboxes("xpath", '//fieldset[@id="fsPermissions"]//input[@type="checkbox"]', None)
		self.crawler.pageClick("id", "SearchPermission")
		self.crawler.execute_script("$('#registrationUDFFieldset').hide(); $('#additionalInfoNextButton2').click();")
		
		self.crawler.pageLoad("id", "registerNoPay2")
		self.crawler.setAttribute(loc, "canLogin", True)
		
	def FundraisingHub(self, loc):
		self.crawler.pageLoad("xpath", '//div[@id="ctl00_ctl00_mainContent_fundraisingNavContainer"]/a')
		personalPageURL = self.crawler.getElemAttribute("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_ucPerformanceParticipant_textboxPersonalPageLink", 'value')
		self.crawler.setAttribute(loc, "Personal Page", personalPageURL)
		self.crawler.writeInIFrame("xpath", '//div[@id="cke_1_contents"]/iframe', 'tag', 'body', self.crawler.getAttributeOne(loc, "Description Personal"))
		print("You have 30secs to add image saved, please don't leave this page")
		time.sleep(30)	 
		self.crawler.pageClick("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_ucPersonalization_buttonSavePersonalization")
		self.crawler.goToUrl(personalPageURL)
		
		self.crawler.pageLoad("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_buttonDonate")
		donationPageUrl = self.crawler.cleanURL(self.crawler.getUrl())
		self.crawler.setAttribute(loc, "Donation Page", donationPageUrl)		
	
	def setuppages(self):
		self.crawler.newTab()
		for loc in self.crawler.getLocations():
			myUrl = self.crawler.getAttributeOne(loc, "Location Page")
			self.crawler.goToUrl(myUrl)
			
			self.crawler.stealImage("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_locationImage", loc +".png")
			username = self.crawler.getAttributeOne(loc, "Direct Donation Admin Username")
			newUser = False
			if pd.isnull(username):
				newUser = True
				username = self.crawler.makeAdminName(loc, "Charity")
				self.crawler.pageLoad("id", "ctl00_ctl00_mainContent_cphLoginRegister_btnRegister")
				self.crawler.pageLoad("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_buttonCreateNewAccount")		
			else:
				self.crawler.inputData("id", "ctl00_ctl00_mainContent_cphLoginRegister_ucLogin_txtUserID", username)
				self.crawler.inputData("id", "ctl00_ctl00_mainContent_cphLoginRegister_ucLogin_txtPassword", username)
				self.crawler.pageLoad("id", "ctl00_ctl00_mainContent_cphLoginRegister_ucLogin_btnLogin")
				if self.crawler.getAttributeOne(loc, "canLogin") != True:
					self.crawler.pageLoad("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_btnSubmit")

			if self.crawler.getAttributeOne(loc, "canLogin") != True:		
				self.RegV2(loc, username, newUser)
			self.FundraisingHub(loc)				   
		self.crawler.closeTab()