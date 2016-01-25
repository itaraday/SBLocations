import time

class SBPledge():

	def __init__(self, crawler):
		self.crawler = crawler
	
	def setupPledge(self):
		self.crawler.pageLoad("xpath",'//li[@id="ucMenu_LiteralLiOpen_EventPaperPledge"]/a')
		pos = 1
		tens = 0
		jump = False
		while pos > 0:
			for loc in self.crawler.getLocations():
				if self.crawler.getAttributeOne(loc, "Pledge"):
					try:
						self.crawler.pageLoad("xpath", '''
														//table[@id="datagridLocations"]
														//td[contains(text(), "'''+loc+'''")]
														/following-sibling::td[2]/a''')
					except:
						pass
					else:
						print("Add custom pledge form for {}".format(loc))
						#time.sleep(30)	
						self.crawler.waitForUser()
						self.crawler.pageLoad("id",'buttonSubmit')						
						if pos > 10:
							tens = pos / 10
							for i in range(0, tens):
								self.crawler.pageLoad("xpath", '//table[@id="datagridLocations"]/tbody/tr[1]/td/a[last()]')
						elif pos != 1:
							self.crawler.pageLoad("text", str(pos))							
			if (pos % 10) == 0:
				foo = self.crawler.getElemAttribute('xpath', '//table[@id="datagridLocations"]/tbody/tr[1]/td/a[last()]', 'text')
				if foo == '...':
					self.crawler.pageLoad("xpath", '//table[@id="datagridLocations"]/tbody/tr[1]/td/a[last()]')
					pos = pos + 1
				else:
					pos = 0
			else:
				pos = pos + 1
				try:
					self.crawler.pageLoad("text", str(pos))			
					# need to check for more than 10
				except:
					pos = 0
						

			
