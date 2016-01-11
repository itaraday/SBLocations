import pandas as pd
import time
import string
import re

def getOptions():
	return {'newImage': 'new image',
			'newSig': 'New Sig',
			'French': 'French'}

def removecurrency(data, remcur):
	for col in remcur:
		try:
			data.loc[data[col].notnull(), col] = data.loc[data[col].notnull(), col].str.replace("[^\d\.]","").astype(int)
		except:
			data.loc[data[col].notnull(), col] = data.loc[data[col].notnull(), col].astype(int)
	return data
	
class dataset: 
	def __init__(self, filePath):
		self.filePath = filePath
		self.df = pd.read_csv(filePath, encoding='mbcs')
		self.df = self.df[self.df["Ignore"].isnull()] 
		self.df.loc[self.df["Charity's Name"].isnull(), "Charity's Name"] = self.df["Charity's Legal Name"]
		self.df.loc[self.df["Description Personal"].isnull(), "Description Personal"] = self.df["description"]
		self.df["old name"] = self.df["Charity's Name"]
		self.df.dropna(how="all", inplace=True) 
		self.df['newImage'] = False
		self.df['newSig'] = False
		self.df['French'] = False
		self.df['new'] = False
		self.df["city"] = self.df["city"].str.title()
		self.df["province"] = self.df["province"].str.title()
		remcur = ["goal", "Minimum donation amount to issue tax receipt", "Tax Receipt Number Start", "Tax Receipt Number end"]
		self.df = removecurrency(self.df, remcur)
		provconvert = {
				"Ab": "Alberta",
				"Mb": "Manitoba",
				"Nb": "New Brunswick",
				"Nl": "Newfoundland and Labrador",
				"Ns": "Nova Scotia",
				"Nt": "Northwest Territories",
				"Nu": "Nunavut",
				"On": "Ontario",
				"Pe": "Prince Edward Island",
				"Qc": "Quebec",
				"Sk": "Saskatchewan",
				"Ty": "Yukon"}
		for prov in provconvert:
			self.df.loc[self.df["province"] == prov, "province"] = provconvert[prov]
		
	
	def save(self, filepath):
		self.df.to_csv(filepath, encoding='mbcs', index=False) 
		
	def getLocations(self, returningStatus="all", myName = "Charity's Name"):
		if returningStatus == "new":
			return self.df.loc[(self.df["Charity added by"].isnull()) & (self.df["new"] == True), myName] 
		elif returningStatus == "returning":
			return self.df.loc[(self.df["Charity added by"].isnull()) & (self.df["new"] == False), myName] 
		else:
			return self.df.loc[self.df["Charity added by"].isnull(), myName]
	
	#if charity name is one word the name is prefix_charity
	#if charity name is mulitple words take first character from each word 
	def makeAdminName(self, loc, prefix):
		re.sub(r'\(.*?\)', '', loc)
		exclude = set(string.punctuation)
		locName = ''.join(ch for ch in loc if ch not in exclude)
		if len(locName.split()) > 1:
			username = "".join(item[0].upper() for item in locName.split())
			username = "_".join([prefix, username])
		else:
			username = "_".join([prefix, locName])
		username = username
		return username
		
	def resetOld(self):
		self.df["old name"] = self.df["Charity's Name"]
	
	def setAttribute(self, name, attribute, val):
		self.df.loc[self.df["Charity's Name"] == name, attribute] = val
		
	def getAttribute(self, name, attribute):
		return self.df.loc[self.df["Charity's Name"] == name, attribute]

	def getAttributeOne(self, name, attribute):
		return self.df.loc[self.df["Charity's Name"] == name, attribute].iloc[0]
	
	def done(self, username):
		username = username[1:] + " " + time.strftime("%Y/%m/%d") 
		self.df.loc[self.df["Charity added by"].isnull(), "Charity added by"] = username