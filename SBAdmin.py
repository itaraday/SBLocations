#from WebCrawler import crawler


class SBAdmin():

	def __init__(self, crawler):
		self.crawler = crawler
		self.tempPassword = "Password1!"

		
	def rightLocations(self, loc, event):
		self.crawler.pageLoad("xpath",'//a[@eventname="'+event+'"]')
		self.crawler.pageClick("xpath", '//td[contains(text(),"'+loc+'")]/following-sibling::td[2]//input[@type="checkbox"]')
			
	def rightLocationsNew(self, loc, event):
		self.crawler.pageLoad('id', 'checkboxAccessAllEvents')
		self.rightLocations(loc, event)
		
	def cleanPermission(self):
		self.crawler.clickCheckboxes("xpath", '//input[@type="checkbox"]', None)
		self.crawler.pageClick("xpath", '//span[@accesscontrolledunitid="RelationshipSearch"]/input')
		self.crawler.pageClick("xpath", '//span[@accesscontrolledunitid="GenerateReports"]/input')
		self.crawler.pageClick("xpath", '//span[@accesscontrolledunitid="ReportCustom"]/input')
		self.crawler.pageLoad('id', 'buttonSubmit')
				
	def newAdmin(self, loc, event):
		self.crawler.pageLoad("id","linkCreateAdministrator" )
		username = self.crawler.makeAdminName(loc, "Admin")
		self.crawler.inputData("id", 'textUsername', username)
		self.crawler.inputData("id", 'textPassword', self.tempPassword)
		self.crawler.inputData("id", 'textConfirmPassword', self.tempPassword)
		self.crawler.inputData("id", 'textFirstName', self.crawler.getAttributeOne(loc, "First Name Administrator"))
		self.crawler.inputData("id", 'textLastName', self.crawler.getAttributeOne(loc, "Last Name Administrator"))
		self.crawler.inputData("id", 'textRegion', loc)
		self.crawler.inputData("id", 'contactInfoControl_txtEmailAddress', self.crawler.getAttributeOne(loc, "Email Administrator"))
		
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
		
	def setupAdmin(self, event):
		self.crawler.pageLoad("id","ucBodyHead_hyperlinkConfigurationTab" )
		self.crawler.getOldNames('ucBodyHead_hyperlinkConfigurationTab', 2)
		
		for loc in self.crawler.getLocations():
			name = self.crawler.getAttributeOne(loc, "old name")
			print name
			try:
				self.crawler.pageLoad("xpath",'//td[contains(text(),"'+name+'")]/preceding-sibling::td[2]//a')
			except:
				print "new admin {}".format(loc)
				self.newAdmin(loc, event)
			else:
				print "oldAdmin: {}".format(loc)
				self.crawler.pageLoad("id","buttonCancel")
				
			   

			
