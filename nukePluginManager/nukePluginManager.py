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
#  you need to put all of your scripts in sub folders in one directory like this:
#
#	pythonscripts
#		script01
#			scriptcontent
#			menu.py
#		script02
#			scriptcontent
#			menu.py
#		script02
#			scriptcontent
#			menu.py
#
#
#  furthermore specify where the main python scripts directory is located. fill out the varible "scriptsPath" (below).
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
global excludeSet
global dontInclude


scriptsPath = "/Users/%s/Dropbox/simons_stuff/_nuke/_NUKE_SIMON_MASTER/python" % getpass.getuser()
excludeSet = os.getenv("HOME")+"/.nuke/pluginManager/excludeSet.txt"
dontInclude = [".DS_Store", "nukePluginManager"]

#no need to change anything from here. Edit only if you exactly know what you're doing.

files=""
scripts=[]
try:
	nuke.pluginList=[]
except:
	nuke.pluginList=[]

def initExcludeSet():
	'''
	make sure that the excludeSet and its directory exist
	'''	
	if not os.path.isfile(excludeSet):
		if not os.path.isdir(os.path.dirname(excludeSet)):
			os.makedirs(os.path.dirname(excludeSet))
		loadExcludeSet = open(excludeSet,'w')
		print loadExcludeSet

#  open text file, read in all lines and
#  return an array with all the lines
def openFileReturnArr(file):
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
	
	excludeList = openFileReturnArr(excludeSet)

	if os.path.isdir(scriptsPath):
		scripts = getScripts(scriptsPath)
	 	for script in scripts:
	 		if script not in excludeList:
	 			nuke.pluginAddPath("{scriptsPath}/{script}".format(scriptsPath=scriptsPath, script=script))
	else:
		nuke.message("could'nt find the python script path")
	
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
    	self.deselectAll = nuke.Script_Knob("deselect all", "deselect all")
    	self.selectAll = nuke.Script_Knob("select all", "select all")
    	self.update = nuke.Script_Knob("update", "update")
    	self.openExcludeSet = nuke.Script_Knob("open exclude set", "open exclude set")
    	#add other knobs
    	self.addKnob(self.div)
    	self.addKnob(self.deselectAll)
    	self.addKnob(self.selectAll)
    	self.addKnob(self.update)
    	self.addKnob(self.openExcludeSet)

    	#deselect excluded knobs
    	excludeList = openFileReturnArr(excludeSet)
    	for pl in nuke.pluginList:
    		if pl.name() in excludeList:
    			pl.setValue(0)
    	
    def showModal( self ):
        result = nukescripts.PythonPanel.showModalDialog(self)

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
				f = open(excludeSet,'w+')
				for pl in nuke.pluginList:
					if pl.getValue() == 0:
						f.write("%s\n" % pl.name())	
				f.close()
			except:
				nuke.message("an error occured while trying to edit the excludeSet file")

			
			if nuke.ask("Your nuke must be restarted before the updated plugin settings work. restart now?"):
				thread.start_new_thread(killNuke, ())
			
		if knob.name() == "open exclude set":	
			excludeSetDir = os.path.dirname(excludeSet)
			if os.path.isdir(excludeSetDir):
				try:
					if platform.system() == "Windows":
						os.startfile(excludeSetDir)
					elif platform.system() == "Darwin":
						subprocess.Popen(["open", excludeSetDir])
					else:
						subprocess.Popen(["xdg-open", excludeSetDir])
				except:
					nuke.message("error opening excludeSetDir")
			else:
				nuke.message("Couldn't find the excludeSet dir")

def addPMPanel():
    global pm
    pm = PluginManagerPanel()
    return pm.addToPane()

def init():
	initExcludeSet()
	initScripts()

def killNuke():
	nuke.executeInMainThread(nuke.scriptClose, ()) 

	
