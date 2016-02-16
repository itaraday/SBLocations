from bs4 import BeautifulSoup
import numpy as np
import time

class SBEmail():

	def __init__(self, crawler):
		self.crawler = crawler
		
	def fixEmail(self, loc, needTR):
		adminEmail = self.crawler.getAttributeOne(loc, "Email Administrator")
		sendername = "Scotiabank Charity Challenge l " + loc
		self.crawler.Ewait(10, "id", "cke_33")
		self.crawler.pageClick("id", "cke_33")
		email = self.crawler.getElemAttribute("xpath", '//div[@id="cke_1_contents"]/textarea', "value")
		soup = BeautifulSoup(email, "lxml")
		[x.extract() for x in soup.findAll('h1')]
		try:
			soup.find(text="%OrganizationName%").replaceWith('%LocationName%')
		except:
			try:
				soup.find(text="%LocationName%").replaceWith('%LocationName%')
			except:
				soup.body.append(BeautifulSoup('<p>%LocationName%</p>', 'html.parser'))					
		soup.body.hidden=True
		foo = soup.body.prettify()
		self.crawler.inputData("xpath", '//div[@id="cke_1_contents"]/textarea', foo)
		self.crawler.pageClick("id", "cke_33")
		if needTR:
			self.crawler.selectLast("id", "ddlTaxReceiptTemplate")
		else:
			time.sleep(3)
		self.crawler.Ewait(20, "id", "showAdvancedOptions")
		self.crawler.pageClick("id", "showAdvancedOptions")
		self.crawler.Ewait(20, "id", "txtSenderName") #something wrong here with last duplicate email
		self.crawler.inputData("id", "txtSenderName", sendername)
		self.crawler.inputData("id", "txtReplyToEmailAddress", adminEmail)
		self.crawler.pageLoad("id", "buttonSave")
		self.crawler.pageLoad("text", "Email Management")
	
	def setupEmail(self):
		self.crawler.pageLoad("xpath",'//li[@id="ucMenu_LiteralLiOpen_EventEmails"]/a')
		emails = {
			"Pledge": {
				"Request Pledge Sheet (Here is your Pledge Sheet)": False
			},
			"tax receipts": {
				"Tax Receipt - Solicited Donation (Here is your tax receipt, solicited)": True,
				"Tax Receipt - Team Donation (Here is your tax receipt, team)": True,
				"Tax Receipt - Correction (Here is your new tax receipt, corrected)": True,
				"Tax Receipt - Duplicate (Here is your duplicate tax receipt)": False
			}
		}
		for loc in self.crawler.getLocations():
			if not self.crawler.getAttributeOne(loc, "emailSetup"):
				self.crawler.select("id", "dropdownlistLocationValue", loc)
				for key in emails:		
					if self.crawler.getAttributeOne(loc, key):
						for email in emails[key]:
							self.crawler.pageLoad("text", email)
							self.fixEmail(loc, emails[key][email])
							self.crawler.clickCheckboxes("xpath", '''//a[contains(text(), "'''+email+'''")]
															/..
															/preceding-sibling::td
															//input[@type="checkbox"]''', 'true')
				self.crawler.setAttribute(loc, "emailSetup", True)