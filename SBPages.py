#from WebCrawler import crawler
import pandas as pd
import time

class SBPages():

    def __init__(self, crawler):
        self.crawler = crawler
    
    def GoToRelationships(self):
        self.crawler.pageLoad("id", "ucBodyHead_hyperlinkRelationshipsTab")
        
    def findLogin(self):
        self.GoToRelationships()
        for loc in self.crawler.getLocations():
            regID = self.crawler.getAttributeOne(loc, "oldRegID")
            if not pd.isnull(regID):
                regID = 2494748
                self.crawler.inputData("id", "textRegistrationId", regID)
                self.crawler.pageLoad("id", "buttonRegistrationSearch")
                self.crawler.pageLoad("xpath", '//table[@id="datagridRegistrantsResults"]//a')
                username = self.crawler.getText('xpath', '''//td[contains(text(), "Username")]
                                                            /following-sibling::td''')
                self.crawler.inputData("id", "textPassword", username)
                self.crawler.inputData("id", "textPasswordConfirm", username)
                self.crawler.setAttribute(loc, "Direct Donation Admin Username", username)
                self.crawler.setAttribute(loc, "Direct Donation Admin Password", username)
                self.crawler.pageLoad("id", "buttonSubmitPwd")
                self.GoToRelationships()
                
                
                
    def setuppages(self):
        self.crawler.newTab()
        for loc in self.crawler.getLocations():
            myUrl = self.crawler.getAttributeOne(loc, "Location Page")
            self.crawler.goToUrl(myUrl)
            
            self.crawler.stealImage("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_locationImage", loc +".png")
            username = self.crawler.getAttributeOne(loc, "Direct Donation Admin Username")
            newUser = False
            if pd.isnull(username):
                newUser = True
                username = self.crawler.makeAdminName(loc, "Charity")
                self.crawler.pageLoad("id", "ctl00_ctl00_mainContent_cphLoginRegister_btnRegister")
                self.crawler.pageLoad("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_buttonCreateNewAccount")        
            else:
                self.crawler.inputData("id", "ctl00_ctl00_mainContent_cphLoginRegister_ucLogin_txtUserID", username)
                self.crawler.inputData("id", "ctl00_ctl00_mainContent_cphLoginRegister_ucLogin_txtPassword", username)
                self.crawler.pageLoad("id", "ctl00_ctl00_mainContent_cphLoginRegister_ucLogin_btnLogin")
                self.crawler.pageLoad("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_btnSubmit")
                
            self.crawler.pageClick("id", "individualParticipantTypeButton")
            
            self.crawler.Ewait(20, "id", "contactForm")
            self.crawler.inputdata("id", "BusinessTitle", "charity")
            self.crawler.inputdata("id", "FirstName", loc)
            self.crawler.inputdata("id", "LastName", "Donations")
            self.crawler.inputdata("id", "AddressLine1", self.crawler.getAttributeOne(loc, "address"))
            self.crawler.inputdata("id", "City", self.crawler.getAttributeOne(loc, "city"))
            self.crawler.select("id", "CAProvince", self.crawler.getAttributeOne(loc, "province"))
            self.crawler.inputdata( "id", "PostalCode", self.crawler.getAttributeOne(loc, "postal code"))
            self.crawler.inputdata("id", "EmailAddress", "scotiabankgroupcharitychallenge@artez.com")
            self.crawler.inputdata("id", "EmailAddressConfirm", "scotiabankgroupcharitychallenge@artez.com")     
            if newUser:
                self.crawler.inputdata("id", "LoginName", username)
                self.crawler.inputdata("id", "Password", username)
                self.crawler.inputdata("id", "PasswordConfirm", username)
            self.crawler.pageClick("id", "contactNextButton2")
            
            self.crawler.Ewait(20, "id", "additionalInfo")
            self.crawler.clickCheckboxes("xpath", '//fieldset[@id="fsPermissions"]//input[@type="checkbox"]', None)
            self.crawler.pageClick("id", "SearchPermission")
            self.crawler.execute_script("$('#registrationUDFFieldset').hide(); $('#additionalInfoNextButton2').click();")
            
            self.crawler.pageLoad("id", "registerNoPay2")
            self.crawler.pageLoad("path", '//div[@id="ctl00_ctl00_mainContent_fundraisingNavContainer"]/a')

            personalPageURL = self.crawler.getElemAttribute("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_ucPerformanceParticipant_textboxPersonalPageLink", 'value')
            self.crawler.setAttribute(loc, "Personal Page", personalPageURL)
            self.crawler.writeInIFrame("xpath", '//div[@id="cke_1_contents"]/iframe', 'tag', 'body', self.crawler.getAttributeOne(loc, "Description Personal"))
            print "You have 30secs to add image saved, please don't leave this page"
            time.sleep(30)   
            self.crawler.pageClick("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_ucPersonalization_buttonSavePersonalization")
            self.crawler.goToUrl(personalPageURL)
            
            self.crawler.pageLoad("id", "ctl00_ctl00_mainContent_bodyContentPlaceHolder_buttonDonate")
            donationPageUrl = self.crawler.cleanURL(self.crawler.getUrl())
            self.crawler.setAttribute(loc, "Donation Page", donationPageUrl)       
        self.crawler.closeTab()