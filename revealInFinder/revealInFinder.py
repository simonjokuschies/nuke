###########################################################################################################
#
#  revealInFinder
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  "custom" tab in read node with knob "reveal in finder". Reveal the fottage in finder
#
#  instalation
#
#  put revealInFinder folder in nuke home directory
#  in init.py write this line (without the '#' in the beginning):
#
#  nuke.pluginAddPath('revealInFinder')
#
##########################################################################################################

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke
import os
import sys
import subprocess

def openFolder(path):
	'''
	open explorer located at path
	'''

	if sys.platform == 'darwin':
		subprocess.check_call(['open', '--', path])
	elif sys.platform == 'linux2':
		subprocess.check_call(['gnome-open', '--', path])
	elif sys.platform == 'windows':
		subprocess.check_call(['explorer', path])

def revealInFinder():
	'''
	get filepath and reveal src in finder
	'''

	n = nuke.thisNode()
	k = nuke.thisKnob()
	if k.name() == "revealInFinder":
		f = n.knob("file").value()
		path = "/".join(f.split("/")[:-1])
		openFolder(path)

def addRevealButton():
	'''
	add custom tab in read node and add reveal button
	'''
	
	n = nuke.thisNode()
	rB = nuke.PyScript_Knob('revealInFinder', 'reveal in finder', '')
	cT = nuke.Tab_Knob("custom", "custom")
	n.addKnob(cT)
	n.addKnob(rB)

nuke.addOnUserCreate(addRevealButton, nodeClass = 'Read')
nuke.addKnobChanged(revealInFinder, nodeClass="Read")




