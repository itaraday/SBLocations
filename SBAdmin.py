#from WebCrawler import crawler


class SBAdmin():

	def __init__(self, crawler):
		self.crawler = crawler
		self.tempPassword = "Password1!"

		
	def rightLocations(self, loc, event):
		self.crawler.pageLoad("xpath",'//a[@eventname="'+event+'"]')
		xpath = '//td[contains(text(),"'+loc+'")]/following-sibling::td[2]//input[@type="checkbox"]'
		if self.crawler.getElemAttribute("xpath", xpath, "checked") == None:
			self.crawler.pageClick("xpath", xpath)
			
	def rightLocationsNew(self, loc, event):
		self.crawler.pageLoad('id', 'checkboxAccessAllEvents')
		self.rightLocations(loc, event)
		
	def cleanPermission(self):
		self.crawler.clickCheckboxes("xpath", '//input[@type="checkbox"]', None)
		self.crawler.pageClick("xpath", '//span[@accesscontrolledunitid="RelationshipSearch"]/input')
		self.crawler.pageClick("xpath", '//span[@accesscontrolledunitid="GenerateReports"]/input')
		self.crawler.pageClick("xpath", '//span[@accesscontrolledunitid="ReportCustom"]/input')
		self.crawler.pageLoad('id', 'buttonSubmit')
				
	def adminSummary(self, loc):
		self.crawler.inputData("id", 'textFirstName', self.crawler.getAttributeOne(loc, "First Name Administrator"))
		self.crawler.inputData("id", 'textLastName', self.crawler.getAttributeOne(loc, "Last Name Administrator"))
		self.crawler.inputData("id", 'textRegion', loc)
		self.crawler.inputData("id", 'contactInfoControl_txtEmailAddress', self.crawler.getAttributeOne(loc, "Email Administrator"))		
	
	def newAdmin(self, loc, event):
		self.crawler.pageLoad("id","linkCreateAdministrator" )
		username = self.crawler.makeAdminName(loc, "Admin")
		self.crawler.inputData("id", 'textUsername', username)
		self.crawler.inputData("id", 'textPassword', self.tempPassword)
		self.crawler.inputData("id", 'textConfirmPassword', self.tempPassword)
		self.adminSummary(loc)
		
		self.crawler.pageLoad("id","buttonContinue" )
		self.crawler.pageLoad("id","linkbuttonTabs" )
		self.cleanPermission()
		self.crawler.pageLoad("id","linkbuttonEvents" )
		self.rightLocationsNew(loc, event)	
		self.crawler.pageLoad("id","buttonSubmit")
		self.crawler.pageLoad("id","buttonSubmit")
		self.crawler.pageLoad("id","buttonSubmit")
		self.crawler.setAttribute(loc, "Artez Admin Username", username)
		self.crawler.setAttribute(loc, "Artez Password", self.tempPassword)
	
	def oldAdmin(self, loc, event):
		self.crawler.inputData("id", 'textUpdatePassword', self.tempPassword)
		self.crawler.inputData("id", 'textConfirmUpdatePassword', self.tempPassword)
		self.crawler.pageLoad("id","btnUpdatePassword")
		self.crawler.pageLoad("xpath",'//li[@id="ucMenu_LiteralLiOpen_ConfigAdminsAccessSummary"]/a')
		
		self.crawler.pageLoad("id","linkbuttonTabs" )
		self.cleanPermission()
		self.crawler.pageLoad("id","linkbuttonEvents" )
		self.rightLocations(loc, event)	
		self.crawler.pageLoad("id","buttonSubmit")
		self.crawler.pageLoad("id","buttonSubmit")

	def setupAdmin(self, event):
		self.crawler.pageLoad("id","ucBodyHead_hyperlinkConfigurationTab" )
		self.crawler.getOldNames('dataGridAdministrators', 2)
		
		for loc in self.crawler.getLocations():
			name = self.crawler.getAttributeOne(loc, "old name")
			try:
				self.crawler.pageLoad("xpath",'//td[contains(text(),"'+name+'")]/preceding-sibling::td[2]//a')
			except:
				self.newAdmin(loc, event)
			else:
				self.oldAdmin(loc, event)
				self.crawler.pageLoad("id","buttonCancel")
				self.crawler.pageLoad("xpath",'//td[contains(text(),"'+name+'")]/preceding-sibling::td[2]//a')
				self.adminSummary(loc)
				username = self.crawler.getText("xpath", '//td[@id="tdUsernameLiteral"]/strong')
				self.crawler.setAttribute(loc, "Artez Admin Username", username)
				self.crawler.setAttribute(loc, "Artez Password", self.tempPassword)
				self.crawler.pageLoad("id","buttonSubmit")
				
				#self.crawler.pageLoad("id","buttonCancel")
				
			   

			
