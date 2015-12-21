#from WebCrawler import crawler


class SBTax():

    def __init__(self, crawler):
        self.crawler = crawler
        
    def setupTR(self):
        self.crawler.pageLoad("id","ucBodyHead_hyperlinkConfigurationTab" )
        self.crawler.pageLoad("xpath",'//li[@id="ucMenu_LiteralLiOpen_ConfigOrgTaxReceipting"]/a')
        try:
            self.crawler.pageLoad("id",'buttonShowAll')
        except:
            pass
        print "setting up tax receipts"
        self.crawler.getOldNames('dataGridTaxReceiptBundles', 0, "Charity's Legal Name")
                
               

            
