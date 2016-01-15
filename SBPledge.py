import time

class SBPledge():

	def __init__(self, crawler):
		self.crawler = crawler
	
	def setupPledge(self):
		self.crawler.pageLoad("xpath",'//li[@id="ucMenu_LiteralLiOpen_EventPaperPledge"]/a')
		pos = 1
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
						print("You have 30secs to add custom pledge form for {}".format(loc))
						print("please don't leave this page")
						#time.sleep(30)	
						self.crawler.waitForUser()
						self.crawler.pageLoad("id",'buttonSubmit')						
						if pos != 1:
							self.crawler.pageLoad("text", str(pos))					
			pos = pos + 1
			try:
				self.crawler.pageLoad("text", str(pos))				
			except:
				pos = 0

			
