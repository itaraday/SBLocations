'''
Created on Dec 15, 2015

@author: itaraday
'''

try:
	from tkinter import *
	from tkinter import filedialog, messagebox 
	from tkinter import font 
except:
	from Tkinter import *
	import ttk
	import tkMessageBox as messagebox
	import tkFileDialog as filedialog
	from string import maketrans
	import tkFont as font

from tempfile import mkstemp
import Data as data
import WebCrawler 
import random
from DropDownBox import DropDownBox
import mycheckbox as chk
import base64
import zlib

def ask_quit(root, crawler, filePath, maindata):
	if messagebox.askokcancel("Quit", "You want to quit now? *sniff*"):
		print("Saving: {}".format(filePath))
		maindata.save(filePath)
		crawler.quit()
		root.destroy()

def MORECOLOR():
	de=("%02x"%random.randint(0,255))
	re=("%02x"%random.randint(0,255))
	we=("%02x"%random.randint(0,255))
	code = de+re+we
	colorbg="#"+code
	#inverse color
	try:
		table = str.maketrans('0123456789abcdef','fedcba9876543210')
	except:
		table = maketrans('0123456789abcdef','fedcba9876543210')
	colorfg = "#"+code.translate(table)
	return ([colorbg, colorfg])	   
	
def begin(maindata, crawler, checkboxes, username, password, org, locationBtn, filepath):
	good = True
	if (org == "Please select an Org") or (not username) or (not password) or (filepath == "Save Temp Files At"):
		good = False
		error = ["List of why this isn't working:\n"]
		if not username:
			error.append("-Username enter you must\n")
		if not password:
			error.append("-You can trust me with your password ;)\n")
		if (org == "Please select an Org"):
			error.append("-I pity the fool that doesn't enter an org\n")
		if (filepath == "Save Temp Files At"):
			error.append('-I can\'t let you do that until you tell me where "{}" is\n'.format(filepath))
		messagebox.showerror(
			"This is why we can't have nice things",
			error
		)
	if good:
		locationBtn.config(state="normal")
		for box in checkboxes:
			if checkboxes[box].ischeck():
				val = box.split('**')
				maindata.setAttribute(val[0], val[1], True)
		crawler.setup(maindata, username, password, org, filepath)


def setupLocs(crawler, name, buttons = None, root = None):
	if buttons:
		for key in buttons:
			buttons[key].config(state="normal")
	if name == 'locations':
		crawler.setupLocations()
	elif name == 'Admin':
		crawler.setupAdmin()
	elif name == 'Tax':
		crawler.setupTR()
	elif name == 'Pages':
		crawler.setupPages()
	elif name == 'Email':
		crawler.setupEmail()
	elif name == 'Pledge':
		crawler.setupPledge()
	elif name == 'Done':
		crawler.Done()
		ask_quit(root, crawler, crawler.maindata.filePath, crawler.maindata)
	
def folderSaveTo(mybutton, root):
	myfolder = filedialog.askdirectory(parent=root, title='Choose a folder to save temp files to')
	if myfolder:
		mybutton.config(text=myfolder)
	
		
def main():	  
	print("Starting!!")
	root = Tk()
	filePath = filedialog.askopenfilename(parent=root,title='Choose a file',filetypes=[('CSV files', '.csv')])
	if not len(filePath):
		messagebox.showerror(
			"KA-BOOM",
			"Well if you're not going to enter a file I QUIT"
		)
		quit()
	crawler = WebCrawler.crawler()	
	myorgs = crawler.getOrgs()
	myorgs.insert(0,"Please select an Org")
	maindata = data.dataset(filePath)
	#removing the Tkinter logo by creating a temp blank icon file
	ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
	'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

	_, ICON_PATH = mkstemp()
	with open(ICON_PATH, 'wb') as icon_file:
		icon_file.write(ICON)	 
		  
	root.iconbitmap(default=ICON_PATH)
	
	root.title("SB Location Enterer")
	root.protocol("WM_DELETE_WINDOW",lambda: ask_quit(root, crawler, filePath, maindata))
	
	root.resizable(0,0)
	userinfo = Frame(root, padx=4, pady=4)
	userinfo.grid(column=0, row=0, sticky=(N,S,E,W))
	
	Label(userinfo, text="Username").grid(column=0, row=0, sticky=(W))
	username = StringVar()
	Entry(userinfo, textvariable=username).grid(column=1, row=0, sticky=(N, S, E, W))
	Label(userinfo, text="Password").grid(column=0, row=1, sticky=(W))
	password = StringVar()
	Entry(userinfo, textvariable=password, show='*').grid(column=1, row=1, sticky=(N, S, E, W)) 
	Label(userinfo, text="Org").grid(column=0, row=2, sticky=(W))
	org = DropDownBox(userinfo, myorgs, 1, 2)
	fileBtn = Button(userinfo, text="Save Temp Files At", command= lambda: folderSaveTo(fileBtn, root))
	fileBtn.grid(column=1, row=3, sticky=(W))	
	
	content = Frame(root, padx=4, pady=4)
	content.grid(column=0, row=1, sticky=(N,S,E,W))
	mylocations = maindata.getLocations()
	x = 0
	y = 0
	checkboxes = {}
	myoptions = data.getOptions()
	for loc in mylocations:
		Label(content, text=loc).grid(column=x, row=y, sticky=(W))
		for option in myoptions:
			x = x + 1
			checkboxes[loc + '**'+option] = chk.singlecheck(content, myoptions[option], x, y)
		x = 0
		y = y + 1
	
	control = Frame(root)
	control.grid(column=0, row=2, padx=5, pady=15)
	button = {}
	helv36 = font.Font(family='Helvetica', size=12, weight='bold')
	
	color = MORECOLOR()
	button['locations'] = Button(control, state = DISABLED, background=color[0], fg=color[1], text="Setup Locations", command= lambda: setupLocs(crawler, 'locations', button))
	button['locations'].grid(column=0, row=1, pady=2, columnspan = 3) 
	button['locations']['font'] = helv36
	
	color = MORECOLOR()
	button['Admin'] = Button(control, state = DISABLED, background=color[0], fg=color[1], text="Setup Admin", command= lambda: setupLocs(crawler, 'Admin'))
	button['Admin'].grid(column=0, row=3, pady=2, padx=3)	 
	button['Admin']['font'] = helv36
	
	color = MORECOLOR()
	button['Tax'] = Button(control, state = DISABLED, background=color[0], fg=color[1], text="Setup Tax Receipt", command= lambda: setupLocs(crawler, 'Tax'))
	button['Tax'].grid(column=1, row=3, pady=2, padx=3)	 
	button['Tax']['font'] = helv36
	
	color = MORECOLOR()
	button['Pages'] = Button(control, state = DISABLED, background=color[0], fg=color[1], text="Setup Pages", command= lambda: setupLocs(crawler, 'Pages'))
	button['Pages'].grid(column=2, row=3, pady=2, padx=3)  
	button['Pages']['font'] = helv36
	
	color = MORECOLOR()
	button['Pledge'] = Button(control, state = DISABLED, background=color[0], fg=color[1], text="Setup Pledge", command= lambda: setupLocs(crawler, 'Pledge'))
	button['Pledge'].grid(column=0, row=4, pady=2, padx=3)	
	button['Pledge']['font'] = helv36
	
	color = MORECOLOR()
	button['Email'] = Button(control, state = DISABLED, background=color[0], fg=color[1], text="Setup Email", command= lambda: setupLocs(crawler, 'Email'))
	button['Email'].grid(column=1, row=4, pady=2, padx=3)  
	button['Email']['font'] = helv36
	
	color = MORECOLOR()
	button['Done'] = Button(control, background=color[0], fg=color[1], text="DONE!1!ONE!", command= lambda: setupLocs(crawler, 'Done',root = root))
	button['Done'].grid(column=2, row=4, pady=2, padx=3)  
	button['Done']['font'] = helv36
	
	color = MORECOLOR()
	runbtn = Button(control, background=color[0], fg=color[1], text="And we're off", command= lambda: begin(maindata, crawler, checkboxes, username.get(), password.get(), org.getSelecton(), button['locations'], fileBtn["text"]))
	runbtn['font'] = helv36
	runbtn.grid(column=0, row=0, pady=2, columnspan = 3)   
	
	for key in button:
		button[key].config(state="normal")
			   
	root.mainloop()
	
	
	
if __name__ == '__main__':
	main() 

	
	