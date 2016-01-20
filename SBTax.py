#from WebCrawler import crawler
import pandas as pd
import time

class SBTax():

	def __init__(self, crawler):
		self.crawler = crawler
	
	def goToTaxReceipting(self):
		self.crawler.pageLoad("id","ucBodyHead_hyperlinkConfigurationTab" )
		self.crawler.pageLoad("xpath",'//li[@id="ucMenu_LiteralLiOpen_ConfigOrgTaxReceipting"]/a')
		try:
			self.crawler.pageLoad("id",'buttonShowAll')
		except:
			pass
	
	def filOutBlocks(self, startBlock, endBlock):
		self.crawler.pageClick("id", "linkBlockCreate")
		self.crawler.inputData("id", 'textStarting', int(startBlock))
		self.crawler.inputData("id", 'textEnding', int(endBlock))
		self.crawler.pageClick("id", "buttonSubmit")
	
	def extendBlock(self, endBlock):
		self.crawler.pageClick("xpath", '//table[@id="datagridBlocks"]//tr[last()]//a')
		self.crawler.inputData("id", 'textEnding', endBlock)
		self.crawler.pageClick("id", "buttonSubmit")
		
	def WTHDoIDO(self, loc):
		startBlock = self.crawler.getAttributeOne(loc, "Tax Receipt Number Start")
		endBlock = self.crawler.getAttributeOne(loc, "Tax Receipt Number end")
		print("Charity wants the range: {} to {}".format(startBlock, endBlock))
		#time.sleep(60)			 
		self.crawler.waitForUser()
		
	def setupTR(self):
		self.goToTaxReceipting()
		self.crawler.getOldNames('dataGridTaxReceiptBundles', 0, "Charity's Legal Name")
		
		for loc in self.crawler.getLocations():
			if self.crawler.getAttributeOne(loc, "tax receipts"):
				oldname = self.crawler.getAttributeOne(loc, "old name")
				legalname = self.crawler.getAttributeOne(loc, "Charity's Legal Name")
				found = self.crawler.fineElement("xpath", '//td[contains(text(),"'+oldname+'")]/following-sibling::td[2]//a')
				#see if TR exists or user wants to overwitr
				if not found:
					oldname = "qwuiqhoiqhqopw"
					while (not found) and (oldname):
						print("Tax receipt for {} not found. press enter to make a new one or paste in the Receipt Bundle Name if it does exist".format(loc))
						try:
							oldname = raw_input()
						except:
							oldname = input()
						if oldname:
							found = self.crawler.fineElement("xpath", '//td[contains(text(),"'+oldname+'")]/following-sibling::td[2]//a')

				newTR = False
				if not found:
					#setup TR, product bug when needing to make new TR it gives an error
					newTR = True
					self.crawler.pageLoad("id","linkButtonSetupNewBundle")
					self.crawler.pageLoad("id","hyperlinkEditInformation")
					self.crawler.inputData("id", 'textboxTaxBundle', legalname)
					oldname = self.crawler.getElemAttribute("id", 'textboxTaxBundle', 'value')
					self.crawler.setAttribute(loc, "old name", oldname)
					self.crawler.pageLoad("id","buttonSubmit")
					self.goToTaxReceipting()
					
				#tax receipt settings
				self.crawler.pageLoad("xpath", '//td[contains(text(),"'+oldname+'")]/following-sibling::td[2]//a')
				self.crawler.pageLoad("id","hyperlinkEditInformation")
				
				trname = self.crawler.getElemAttribute("id", 'textboxTaxBundle', 'value')
				self.crawler.setAttribute(loc, "TR name", trname)
				prefix = self.crawler.getAttributeOne(loc, "Tax Receipt Prefix")
				if pd.isnull(prefix):
					prefix = "" 
				self.crawler.inputData("id", 'textPrefix',prefix)
				length = self.crawler.getAttributeOne(loc, "Tax Receipt Number end")
				if pd.isnull(length):
					length = 4
				else:
					length = len(str(length))
				if length == 0:
					length = 4
				self.crawler.inputData("id", 'textLength', length)
				if self.crawler.getAttributeOne(loc, "Leading 0"):
					self.crawler.clickCheckBox('true', "id", 'checkLeadingZeros')
				self.crawler.pageLoad("id","buttonSubmit")
				
				#tax receipt blocks
				#get old blocks
				oldBlocks = self.crawler.getTRBlocks('//table[@id="datagridBlocks"]//tr')
				startBlock = self.crawler.getAttributeOne(loc, "Tax Receipt Number Start")
				endBlock = self.crawler.getAttributeOne(loc, "Tax Receipt Number end")
				
				if not len(oldBlocks):
					if pd.isnull(startBlock):
						startBlock = 1
					if pd.isnull(endBlock):
						endBlock = startBlock + 1000 
					self.filOutBlocks(startBlock, endBlock)
				elif len(oldBlocks) == 1:
					if pd.isnull(startBlock):
						startBlock = oldBlocks[0][0]
					else:
						startBlock = int(startBlock)
					if pd.isnull(endBlock):
						endBlock = oldBlocks[0][1]
					else:
						endBlock = int(endBlock)
					myrange = set(range(startBlock, endBlock))
					oldBlockRange = set(range(oldBlocks[0][0], oldBlocks[0][1]))
					intersect = myrange.intersection(oldBlockRange)
					#if no intersection
					if len(intersect) == 0:
						self.filOutBlocks(startBlock, endBlock)
					#if no change
					elif len(intersect) == len(myrange):
						pass
					#else there is a partial intersection
					#check if need to extend the end number
					elif endBlock >= oldBlocks[0][1]:
						self.extendBlock(endBlock)
					#check if need to make a new block before the intersection
					elif (endBlock > oldBlocks[0][0]) and (endBlock < oldBlocks[0][1]):
						self.filOutBlocks(startBlock, oldBlocks[0][0])
					else:
						self.WTHDoIDO(loc)
				else:
					if not ((pd.isnull(startBlock)) and (pd.isnull(endBlock))):
						self.WTHDoIDO(loc)
					
				#TR Template
				try:
					self.crawler.pageClick("xpath", '//table[@id="datagridTemplates"]//tr[last()]//a')
				except:
					self.crawler.pageLoad("id","linkTemplateCreate")
					newTR = True   
				self.crawler.Ewait(10, "id", "textName")
				self.crawler.inputData("id", 'textName', legalname)
				self.crawler.inputData("id", 'ucPDFTemplateBuilder_CharitableRegistrationNumber', self.crawler.getAttributeOne(loc, "Charitable Business/Registration Number"))
				mylocation = self.crawler.getAttributeOne(loc, "city") + ", Canada"
				self.crawler.inputData("id", 'ucPDFTemplateBuilder_Location', mylocation)
				#creating address label
				a1 = legalname
				a2 = self.crawler.getAttributeOne(loc, "address")
				a3 = self.crawler.getAttributeOne(loc, "city") + " " + self.crawler.getAttributeOne(loc, "province") + " " + self.crawler.getAttributeOne(loc, "postal code")
				a4 = "P. " + self.crawler.getAttributeOne(loc, "TRPhone") + " E. " + self.crawler.getAttributeOne(loc, "TREmail")
				address = "\n".join([a1, a2, a3, a4])
				self.crawler.inputData("id", 'ucPDFTemplateBuilder_OrgAddress', address)
				
				#check if need images
				if newTR:
					print("Please setup the image and signature for new charity: {}".format(loc))
					#time.sleep(60)		
					self.crawler.waitForUser()					
				if self.crawler.getAttributeOne(loc, "newImage") or self.crawler.getAttributeOne(loc, "newSig"):
					print("charity: {} New Image: {} New Signature: {}".format(
																				loc, 
																				self.crawler.getAttributeOne(loc, "newImage"),
																				self.crawler.getAttributeOne(loc, "newSig")
																		))
					#time.sleep(60)	  
					self.crawler.waitForUser()
				self.crawler.pageLoad("id","buttonSubmit")
				self.crawler.pageClick("xpath", '//table[@id="datagridTemplates"]//tr[last()]//a')
				self.crawler.Ewait(10, "id", "linkbuttonPreview")
				self.crawler.pageClick("id", 'linkbuttonPreview')
				self.goToTaxReceipting()
