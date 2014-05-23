###########################################################################################################
#
#  nukePluginManager
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  Plugin Manager for nuke. In some kind of way what Maya has. Panel with which you can control which
#  scripts and plugins you want to load at nuke startup. The nice thing is that you can just drop some new stuff in
#  and it will be loaded automatically. No setting up a separate init.py anymore for that.
#
#  instalation
#
#  put nukePluginManager folder in nuke home directory
#  in init.py write this line (without the '#' in the beginning):
#
#  nuke.pluginAddPath('nukePluginManager')
#
#  Please note:
#  you need to put all of your scripts in sub folders in one python scripts directory like this:
#
#   PythonScriptsDirectory
#		script01
#			script01.py
#			menu.py
#		script02
#			script02.py
#			menu.py
#		script02
#			script03.py
#			menu.py
#
#  furthermore specify where the main python scripts directory is located (variable called scriptPath).
#  to exclude something to be loaded at all just rename your folder not to be included starting with an underscore or
#  it to the dontInclude list (below).
#
#
##########################################################################################################

import nuke
import nukescripts
import os
import getpass
import sys
import subprocess
import platform
import thread

global scriptsPath
global currentPref
global dontInclude


scriptsPath = "/Users/%s/Dropbox/simons_stuff/_nuke/_NUKE_SIMON_MASTER/python" % getpass.getuser()
pluginManagerDir = os.getenv("HOME")+"/.nuke/pluginManager"
dontInclude = [".DS_Store", "nukePluginManager"]

#no need to change anything from here. Edit only if you exactly know what you're doing.

files=""
scripts=[]
try:
	nuke.pluginList=[]
except:
	nuke.pluginList=[]

currentPref = pluginManagerDir+"/currentPref.txt"
prefsDir = pluginManagerDir+"/prefs/"
loadSaveToggle=0
prefs=[]
prefsBtn=[]

def initPL():
	'''
	make sure that the currentPref and prefs directory exist
	load the prefs
	'''	
	if not os.path.isfile(currentPref):
		if not os.path.isdir(os.path.dirname(currentPref)):
			os.makedirs(os.path.dirname(currentPref))
		loadCurrentPref = open(currentPref,'w')

	if not os.path.isdir(prefsDir):
		os.makedirs(os.path.dirname(prefsDir))

	for prefFile in os.listdir(prefsDir):
		if prefFile not in dontInclude:
			fileN, fileExt = os.path.splitext(prefFile)
			prefs.append(fileN)

def openFileReturnArr(file):
	'''
	open text file, read in all lines and
	return an array with all the lines
	'''
	arr=[]
	fobj = open("%s"%file, "r")
	#load in all lines
	for line in fobj:
		#delete word wrap at the end of each line
		line=line.replace("\n", "")
		arr.append(line)
	fobj.close()
	return arr

def getScripts(scriptsPath):
	'''
	load all scripts into list
	@return list
	'''

	for filename in os.listdir(scriptsPath):
		if filename not in dontInclude and filename[0] != "_":
			scripts.append(filename)		
	scripts.reverse()
	return scripts

def initScripts():
	
	excludeList = openFileReturnArr(currentPref)

	if os.path.isdir(scriptsPath):
		scripts = getScripts(scriptsPath)
	 	for script in scripts:
	 		if script not in excludeList:
	 			nuke.pluginAddPath("{scriptsPath}/{script}".format(scriptsPath=scriptsPath, script=script))
	else:
		nuke.message("could'nt find the python script path")
	
def deletePrefs(panel):
	'''
	delete prefs
	'''
	
	dpp = nuke.Panel('PluginManager - delete pref list')
	for p in prefsBtn:
		dpp.addBooleanCheckBox(p.name(), False)
	
	if dpp.show():
		
		for p in prefsBtn:
			if dpp.value(p.name())==True:
				try:
					os.remove(prefsDir+p.name()+".txt")
					panel.removeKnob(p)
					prefs.remove(p.name())
					prefsBtn.remove(p)
				except:
					print "Could not delete %s" % p.name()

class PluginManagerPanel(nukescripts.PythonPanel):
	'''
	PluginManagerPanel
	'''

	def __init__( self ):
        
		nukescripts.PythonPanel.__init__(self, "PluginManager", "PluginManager")       
        
		scripts.reverse()

		#plugins
		for script in scripts:
			self.sc = nuke.Boolean_Knob(script, script ,"1") 
			self.sc.setFlag(nuke.STARTLINE)
			self.addKnob(self.sc)
			nuke.pluginList.append(self.sc)
		
		#other knobs
		self.div=nuke.Text_Knob("","","")
		self.div.setFlag(nuke.STARTLINE)
		self.div2=nuke.Text_Knob("","","")
		self.div2.setFlag(nuke.STARTLINE)
		self.div3=nuke.Text_Knob("","","")
		self.div3.setFlag(nuke.STARTLINE)
		self.deselectAll = nuke.Script_Knob("deselect all", "deselect all")
		self.selectAll = nuke.Script_Knob("select all", "select all")
		self.openPrefDir = nuke.Script_Knob("open pref dir", "open pref dir")
		self.loadSave = nuke.Script_Knob("loadSave", "load/save")
		self.update = nuke.Script_Knob("update", "<span style='color:green'>update<span>")
		#add other knobs
		self.addKnob(self.div)
		self.addKnob(self.deselectAll)
		self.addKnob(self.selectAll)
		self.addKnob(self.openPrefDir)
		self.addKnob(self.loadSave)
		self.addKnob(self.update)
		self.addKnob(self.div2)




		#deselect excluded knobs
		excludeList = openFileReturnArr(currentPref)
		for pl in nuke.pluginList:
			if pl.name() in excludeList:
				pl.setValue(0)

		#prefs
		self.prefsName = nuke.String_Knob('name', '')
		self.prefsName.setFlag(nuke.STARTLINE)
		self.savePrefs = nuke.Script_Knob("save list", "save list")
		self.deletePrefs = nuke.Script_Knob("delete list", "delete list")
        
		#prefsBtn
		i=0
		for p in prefs:
			self.pknob = nuke.Script_Knob(p,p)
			if i%5==0:
				self.pknob.setFlag(nuke.STARTLINE)
			prefsBtn.append(self.pknob)
			i+=1

	def showModal( self ):
		result = nukescripts.PythonPanel.showModalDialog(self)
		self.prefsName.setFlag(nuke.STARTLINE)

	def knobChanged( self, knob ): 
        
		if knob.name() == "deselect all":
			for pl in nuke.pluginList:
				pl.setValue(0)

		if knob.name() == "select all":
			for pl in nuke.pluginList:
				pl.setValue(1)

		if knob.name() == "update":
			#write new knobInit
			try:
				f = open(currentPref,'w+')
				for pl in nuke.pluginList:
					if pl.getValue() == 0:
						f.write("%s\n" % pl.name())	
				f.close()
			except:
				nuke.message("an error occured while trying to edit the currentPref file")

			if nuke.ask("Your nuke must be restarted before the updated plugin settings work. restart now?"):
				thread.start_new_thread(killNuke, ())
			
		if knob.name()=="loadSave":
			global loadSaveToggle
			loadSaveToggle+=1
			
			if loadSaveToggle%2==0:
				self.removeKnob(self.prefsName)
				self.removeKnob(self.savePrefs)
				self.removeKnob(self.deletePrefs)
				self.removeKnob(self.div3)
				for pknob in prefsBtn:
					self.removeKnob(pknob)
			else:
				self.addKnob(self.prefsName)
				self.addKnob(self.savePrefs)
				self.addKnob(self.deletePrefs)
				self.addKnob(self.div3)
				for pknob in prefsBtn:
					self.addKnob(pknob)

		if knob.name()=="save list":
			listName=self.prefsName.getValue()
			listName=listName.replace(" ","_")
			newPrefFile=prefsDir+listName+".txt"
			
			if listName!="":
				overwrite=True
				if os.path.isfile(newPrefFile):
					overwrite=False
					if nuke.ask("name already exists. overwrite it?"):
						overwrite=True
				
				if overwrite==True:
					f = open(newPrefFile,'w+')
					for n in nuke.pluginList:
						if n.value()==False:
							f.write(n.name()+"\n")    			

					#refresh prefsBtn - remove all knobs, add the specific new one and load them back
					for p in prefsBtn:
						self.removeKnob(p)

					for p in prefsBtn:
						if listName==p.name():
							prefs.remove(listName)
							prefsBtn.remove(p)
					
					self.pk = nuke.Script_Knob(listName,listName)
					prefsBtn.append(self.pk)
					prefs.append(listName)

					#refresh prefsBtn
					i=0
					for p in prefsBtn:
						p.clearFlag(nuke.STARTLINE)
						if i%5==0:
							p.setFlag(nuke.STARTLINE)
						self.addKnob(p)
						i+=1
					
					self.prefsName.setValue("")
				
			else:
				nuke.message("please enter a name for the list")

		if knob.name()=="delete list":
			deletePrefs(self)

		if knob.name() == "open pref dir":	
			currentPrefDir = os.path.dirname(currentPref)
			if os.path.isdir(currentPrefDir):
				try:
					if platform.system() == "Windows":
						os.startfile(currentPrefDir)
					elif platform.system() == "Darwin":
						subprocess.Popen(["open", currentPrefDir])
					else:
						subprocess.Popen(["xdg-open", currentPrefDir])
				except:
					nuke.message("error opening the pref dir")
			else:
				nuke.message("Couldn't find the pref dir")

		if knob.name() in prefs:
			#prefsknobs
			prefFile = prefsDir+knob.name()+".txt"
			if os.path.isfile(prefFile):
				prefList = openFileReturnArr(prefFile)

				#set new prefs
				for pl in nuke.pluginList:
					pl.setValue(True)
					if pl.name() in prefList:
						pl.setValue(False)

			else:
				nuke.message("Couldn't find the prefFile '%s'. No such file." % knob.name())
			
def addPMPanel():
	global pm
	pm = PluginManagerPanel()
	return pm.addToPane()

def init():
	initPL()
	initScripts()

def killNuke():
	nuke.executeInMainThread(nuke.scriptClose, ()) 

	
