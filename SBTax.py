#from WebCrawler import crawler
import pandas as pd

class SBTax():

    def __init__(self, crawler):
        self.crawler = crawler
    
    def showall(self):
        try:
            self.crawler.pageLoad("id",'buttonShowAll')
        except:
            pass
        
    def goToTaxReceipting(self):
        self.crawler.pageLoad("id","ucBodyHead_hyperlinkConfigurationTab" )
        self.crawler.pageLoad("xpath",'//li[@id="ucMenu_LiteralLiOpen_ConfigOrgTaxReceipting"]/a')
        self.showall()
    
    def setupTR(self):
        self.goToTaxReceipting()
        print "setting up tax receipts"
        self.crawler.getOldNames('dataGridTaxReceiptBundles', 0, "Charity's Legal Name")
        
        for loc in self.crawler.getLocations():
            if self.crawler.getAttributeOne(loc, "tax receipts"):
                oldname = self.crawler.getAttributeOne(loc, "old name")
                legalname = self.crawler.getAttributeOne(loc, "Charity's Legal Name")
                found = self.crawler.fineElement("xpath", '//td[contains(text(),"'+oldname+'")]/following-sibling::td[2]//a')
                #see if TR exists
                if not found:
                    #setup TR, product bug when needing to make new TR it gives an error
                    self.crawler.pageLoad("id","linkButtonSetupNewBundle")
                    self.crawler.pageLoad("id","hyperlinkEditInformation")
                    self.crawler.inputData("id", 'textboxTaxBundle', legalname)
                    oldname = self.crawler.getElemAttribute("id", 'textboxTaxBundle', 'value')
                    self.crawler.setAttribute(loc, "old name", oldname)
                    self.crawler.pageLoad("id","buttonSubmit")
                    self.goToTaxReceipting()
                
                self.crawler.pageLoad("xpath", '//td[contains(text(),"'+oldname+'")]/following-sibling::td[2]//a')
                self.crawler.pageLoad("id","hyperlinkEditInformation")
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
                    self.crawler.pageClick("id", "checkLeadingZeros")
                self.crawler.pageLoad("id","buttonSubmit")
                
                
                
                self.goToTaxReceipting()
