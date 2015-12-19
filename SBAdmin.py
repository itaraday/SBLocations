#from WebCrawler import crawler


class SBAdmin():

    def __init__(self, crawler):
        self.crawler = crawler
        
    def setupAdmin(self):
        self.crawler.pageLoad("id","ucBodyHead_hyperlinkConfigurationTab" )
        self.crawler.getOldNames('ucBodyHead_hyperlinkConfigurationTab', 2)
        
        for loc in self.crawler.getLocations():
            try:
                self.crawler.pageLoad("text",self.crawler.getAttributeOne(loc, "old name"))
            except:
                newAdmin(loc)
            else:
                print "oldAdmin(loc)"
            
        def newAdmin(loc):
            self.crawler.pageLoad("id","linkCreateAdministrator" )
            username = self.crawler.makeAdminName(loc)
            self.crawler.inputData("name", 'textUsername', username)
            self.crawler.inputData("name", 'textPassword', 'Password1!')
            self.crawler.inputData("name", 'textConfirmPassword', 'Password1!')
            self.crawler.inputData("name", 'textFirstName', self.crawler.getAttributeOne(loc, "First Name Administrator"))
            self.crawler.inputData("name", 'textLastName', self.crawler.getAttributeOne(loc, "Last Name Administrator"))
            self.crawler.inputData("name", 'textRegion', loc)
            self.crawler.inputData("name", 'contactInfoControl_txtEmailAddress', self.crawler.getAttributeOne(loc, "Email Administrator"))
            
            self.crawler.pageLoad("id","buttonContinue" )
            self.crawler.pageLoad("id","linkbuttonTabs" )
            cleanPermission()
            self.crawler.pageLoad("id","linkbuttonEvents" )
            rightLocationsNew(loc)
            
        
        def rightLocationsNew(loc):
            with wait_for_page_load(self.browser):
                self.browser.find_elements_by_id("checkboxAccessAllEvents").click()
            rightLocations
        
        def rightLocations(loc):
            with wait_for_page_load(self.browser):
                self.browser.find_element_by_xpath('//a[@eventname="'+self.event+'"]').click()
            self.browser.find_element_by_xpath("""//td[contains(text(),'Between Friends')]/
                                                    following-sibling::td/
                                                    following-sibling::td//
                                                    input""").click()
            with wait_for_page_load(self.browser):
                self.browser.find_elements_by_id("submit").click()
            
            
        def cleanPermission():
            checkboxes = self.browser.find_elements_by_xpath("//input[@type='checkbox']")
            for box in checkboxes:
                if box.get_attribute("checked") != None:
                    box.click()
            self.browser.find_element_by_xpath('//span[@accesscontrolledunitid="RelationshipSearch"]/input').click()
            self.browser.find_element_by_xpath('//span[@accesscontrolledunitid="GenerateReports"]/input').click()
            self.browser.find_element_by_xpath('//span[@accesscontrolledunitid="ReportCustom"]/input').click()
            with wait_for_page_load(self.browser):
                self.browser.find_element_by_id('buttonSubmit').click()
            
