#from WebCrawler import crawler


class SBLocations():

	def __init__(self, crawler):
		self.crawler = crawler
		
	def goToEvent(self, event):
		#Go to events page
		self.crawler.pageLoad("id","ucBodyHead_hyperlinkEventTab" )
		#go to event
		self.crawler.pageLoad("text",event )		
	
	def goToLocations(self, event):
		self.goToEvent(event)
		#go to locations
		self.crawler.pageLoad("id","ucMenu_HyperLinkMenu_EventLocation" )		 
	
	def finishDesc(self, event):
		self.goToLocations(event)
		try:
			self.crawler.pageLoad("id","buttonShowAll" )
		except:
			pass		
		self.crawler.getOldNames('datagridLocations', 0)
		for loc in self.crawler.getLocations():
			if self.crawler.getAttributeOne(loc, "tax receipts"):
				try:
					self.crawler.pageLoad("id","buttonShowAll" )
				except:
					pass
				self.crawler.pageLoad("text", self.crawler.getAttributeOne(loc, "old name")) 		
				self.crawler.pageLoad("id", "hyperlinkEditInfo")
				myurl = self.crawler.getAttributeOne(loc, "Donation Page")
				message = '\nTo make a direct donation to '+loc+' please <a href="'+myurl+'">visit our donation page</a>.\nThank you!'
				self.crawler.inputData("id", "ucEventLocationContent_textboxLocationLongDescription1", message, False)
				
	def enableTR(self, event):
		self.goToLocations(event)
		try:
			self.crawler.pageLoad("id","buttonShowAll" )
		except:
			pass		
		self.crawler.getOldNames('datagridLocations', 0)
		for loc in self.crawler.getLocations():
			if self.crawler.getAttributeOne(loc, "tax receipts"):
				try:
					self.crawler.pageLoad("id","buttonShowAll" )
				except:
					pass
				self.crawler.pageLoad("text", self.crawler.getAttributeOne(loc, "old name")) 
				self.crawler.pageLoad("xpath", '//li[@id="ucMenu_liEventLocationTax"]/a')
				self.crawler.select("id", "dropDownListBundleName", self.crawler.getAttributeOne(loc, "TR name"))
				self.crawler.pageLoad("id", "buttonSubmit")
				self.goToLocations(event)
				
				
		
	
	def LocationContent(self, loc, newimage):
		self.crawler.inputData("id", 'ucEventLocationContent_textboxLocationName', loc)
		self.crawler.inputData("id", 'ucEventLocationContent_textboxExportLocationID', loc)
		self.crawler.inputData("id", 'ucEventLocationContent_textboxAddressLine1', self.crawler.getAttributeOne(loc, "address"))
		self.crawler.inputData("id", 'ucEventLocationContent_textboxCity', self.crawler.getAttributeOne(loc, "city"))
		self.crawler.inputData("id", 'ucEventLocationContent_ucPostalCode_txtPostalCode', self.crawler.getAttributeOne(loc, "postal code"))
		self.crawler.select("id", "ucEventLocationContent_dropdownlistProvince", self.crawler.getAttributeOne(loc, "province"))
		
		
		if newimage:
			#if there is an old image try to remove it
			try:
				self.crawler.pageLoad("id","ucEventLocationContent_linkbuttonRemoveExistingImage" )
				self.crawler.wait(10)
				
			except:
				pass					
			
			self.crawler.pageClick("id","ucEventLocationContent_ucImageLoader_fileUpload")				 
			try:
				self.crawler.Ewait(60, "xpath", '//div[@id="divPreviewThubnail"]/img')
			except:
				print "Took too long to select an image for: {}".fomat(loc)
		self.crawler.inputData("id", 'ucEventLocationContent_textboxLocationLongDescription1', self.crawler.getAttributeOne(loc, "description"))
		
	def LoctionDetails(self, loc):
		self.crawler.inputData("id", 'ucEventLocationDetail_textboxFundraisingGoal', self.crawler.getAttributeOne(loc, "goal"))

			
	def getLocURL(self, event):
		self.goToEvent(event)
		self.crawler.pageLoad("id", "linkbuttonEventLocationLink")
		self.crawler.pageClick("id", "rdoIndividualLinks")
		for loc in self.crawler.getLocations():
			myurl = self.crawler.getElemAttribute("xpath", '''//div[@id="divLocationHomePageLinks"]
												//div[contains(text(), "'''+loc+'''")]
												/following-sibling::div
												//input[@type="text"]''', "value")
			self.crawler.setAttribute(loc, 'Location Page', myurl)
		
	def setupLocations(self, event):		

		self.goToLocations(event)
		#get all removed locations
		self.crawler.pageClick("id","chkShowRemovedLocations" )	 
		try:
			self.crawler.pageLoad("id","buttonShowAll" )
		except:
			pass
		
		self.crawler.getOldNames('datagridLocations', 0)
		
		#reactivate locations (and note new ones)
		needreload = False
		for loc in self.crawler.getLocations():
			if needreload:
				self.crawler.pageClick("id","chkShowRemovedLocations" )	   
				try:
					self.crawler.pageLoad("id","buttonShowAll" )	
				except:
					pass
			try:
				self.crawler.pageLoad("text", self.crawler.getAttributeOne(loc, "old name")) 
			except:
				print "{} is a new location".format(loc)
				self.crawler.setAttribute(loc, 'new', True)
				needreload = False
			else:
				self.crawler.pageLoad("id","linkbuttonActivateLocation" )
				needreload = True
			   
		#enter new locations	
		for loc in self.crawler.getLocations("new"):
			self.crawler.pageLoad("id","linkbuttonLocationCreate" )
			self.LocationContent(loc, True)
			self.crawler.setAttribute(loc, 'newImage', False)  
			self.crawler.pageLoad("id","buttonNext" )
			self.LoctionDetails(loc)
			self.crawler.pageLoad("id","buttonFinish" )

			
		#enter returning locations
		for loc in self.crawler.getLocations("returning"):
			try:
				self.crawler.pageLoad("id","buttonShowAll" )
			except:
				pass
			self.crawler.pageLoad("text",self.crawler.getAttributeOne(loc, "old name"))

			self.crawler.pageLoad("text","Edit Location Content" )
			self.LocationContent(loc, self.crawler.getAttributeOne(loc, "newImage"))
			self.crawler.pageLoad("id","buttonSubmit" )
			self.crawler.pageLoad("text","Edit Location Details")
			self.LoctionDetails(loc)
			self.crawler.pageLoad("id","buttonSubmit" )
			self.crawler.pageLoad("text","Locations" )
