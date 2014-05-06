###########################################################################################################
#
#  nextVersion
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  automatically version up the current script and all selected write nodes, extra functionality for
#  write nodes: reveal render in finder, create next version, force create render directory, save backup of script after render.
#
#  instalation
#
#  put nextVersion folder in nuke home directory
#  in init.py write this line (without the '#' in the beginning):
#
#  nuke.pluginAddPath('nextVersion')
#
##########################################################################################################


import nuke
import nukescripts
import os
import sys
import subprocess
import platform

def addCustomElements():
	
	node = nuke.thisNode()
	
	#init custom elements
	tab_next = nuke.Tab_Knob("next", "next")
	btn_revealInFinder = nuke.PyScript_Knob('reveal in explorer', 'reveal in explorer', '')
	btn_createNextVersionFolder = nuke.PyScript_Knob('create next version', 'create next version', '')
	btn_forceCreateDirectory = nuke.PyScript_Knob('force create directory', 'force create directory', '')
	chBox_saveBackup = nuke.Boolean_Knob('save backup', 'save backup')

	#add custom elements to node
	node.addKnob(tab_next)
	node.addKnob(btn_revealInFinder)
	node.addKnob(btn_createNextVersionFolder)
	node.addKnob(btn_forceCreateDirectory)
	node.addKnob(chBox_saveBackup)

def nextVersionPanel():
	
	p = nuke.Panel('nextVersion - Select write nodes to increment version')
	p.setWidth(500)
	for node in nuke.allNodes("Write"):
		p.addBooleanCheckBox("%s" % node.name() , 1)
	return p

def saveBackup(writeName):
	
	scriptLocation = nuke.root().name()
	scriptName = os.path.basename(scriptLocation)
	fileValue = nuke.toNode(writeName)['file'].getValue()
	renderPath = os.path.dirname(fileValue)
	
	nuke.scriptSave(renderPath + "/backup_" + scriptName)	

def performCustomAction():
	
	node = nuke.thisNode()
	knob = nuke.thisKnob()

	fileValue = node["file"].getValue()
	renderPath = os.path.dirname(fileValue)

	#reveal in explorer
	if knob.name() == "reveal in explorer":
		if renderPath!="":
			try:
				if platform.system() == "Windows":
					os.startfile(renderPath)
				elif platform.system() == "Darwin":
					subprocess.Popen(["open", renderPath])
				else:
					subprocess.Popen(["xdg-open", renderPath])
			except:
				nuke.message("couldn't open render path. No such directory")
		else:
			nuke.message("Please make sure to set a render path")

	#create next version
	if knob.name() == "create next version":	
		if renderPath != "":
			nukescripts.clear_selection_recursive()
			node.setSelected(True)
			nukescripts.version_up()
			node.setSelected(False)

			fileValue = node["file"].getValue()
			renderPath = os.path.dirname(fileValue)

			if not os.path.isdir(renderPath):
				os.makedirs(renderPath)
				nuke.message("successfully versioned up")
			else:
				nuke.message("Renderfolder '%s' seems to exist" % renderPath)
		else:
			nuke.message("Please make sure to set a render path")

	#force create directory
	if knob.name() == "force create directory":
		if renderPath != "":	
			if not os.path.isdir(renderPath):
				os.makedirs(renderPath)
				nuke.message("successfully created render directory at: \n\n%s" % renderPath)
			else:
				nuke.message("render directory exists")	
		else:
			nuke.message("Please make sure to set a render path")
	
	#save backup
	if knob.name() == "save backup":
		if knob.getValue() == 1.0:
			node["beforeRender"].setValue("nextVersion.saveBackup('%s')" % node.name())
		else:
			node["beforeRender"].setValue("")

def nextVersion():
	
	p = nextVersionPanel()
	if p.show():
		#script version up
		nukescripts.script_version_up()
		#writeNode version up and create folder
		for node in nuke.allNodes("Write"):
			name = node.name()
			if p.value(name) == 1:
				node.knob("create next version").execute()






