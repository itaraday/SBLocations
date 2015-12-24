from bs4 import BeautifulSoup
import time

class SBEmail():

	def __init__(self, crawler):
		self.crawler = crawler
		
	def fixEmail(self, loc, needTR):
		adminEmail = self.crawler.getAttributeOne(loc, "Email Administrator")
		sendername = "Scotiabank Charity Challenge l " + loc
		self.crawler.pageClick("id", "cke_33")
		email = self.crawler.getElemAttribute("xpath", '//div[@id="cke_1_contents"]/textarea', "value")
		soup = BeautifulSoup(email, "lxml")
		[x.extract() for x in soup.findAll('h1')]
		try:
			soup.find(text="%OrganizationName%").replaceWith('%LocationName%')
		except:
			pass
		soup.body.hidden=True
		self.crawler.inputData("xpath", '//div[@id="cke_1_contents"]/textarea', soup.body.prettify())
		self.crawler.pageClick("id", "cke_33")
		if needTR:
			print needTR
			self.crawler.selectLast("id", "ddlTaxReceiptTemplate")
		self.crawler.Ewait(10, "id", "showAdvancedOptions")
		self.crawler.pageClick("id", "showAdvancedOptions")
		self.crawler.Ewait(10, "id", "txtSenderName")
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
			self.crawler.select("id", "dropdownlistLocationValue", loc)
			for key in emails:		
				if self.crawler.getAttributeOne(loc, key):
					for email in emails[key]:
						self.crawler.pageLoad("text", email)
						self.fixEmail(loc, emails[key][email])
						self.crawler.clickCheckboxes("xpath", '''//td[contains(text(), "'''+email+'''")]
														/preceding-sibling::td[0]
														//input[@type="checkbox"]''', 'true')
			