###########################################################################################################
#
#  default
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  Set knob defaults on the fly so you dont't have to write them manually into your nuke home directory.
#  Just set a knob like you want to have it as knobdefault and then right click, choose myDefaults - set as knob default
#  If you want to get rid of the knob default just right click on the knob and choose myDefaults - reset.
#
#  instalation
#
#  put myDefaults folder inside nuke home directory. In your int.py write (without the '#'):
#  nuke.pluginAddPath("default")
#
##########################################################################################################

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke
import os
import helper

global default_dir
global knobInit
global ctrl

default_dir = os.path.dirname(__file__)
knobInit = default_dir+"/init.py"
ctrl = False

def checkExistingInit():
	'''
	check if knobInit exists
	if not create one
	'''
	
	if not os.path.isfile(knobInit):
		try:
			open(knobInit,'w')
			if ctrl == True:
					print "created knobInit"
		except:
			if ctrl == True:
					print "couldn't create knobInit"
	else:
		if ctrl == True:
			print "knobInit exists"

def createDefault():
	'''
	create custom knobDefault value
	'''

	n = nuke.thisNode()
	k = nuke.thisKnob()
	
	#set default for current nuke session
	nuke.knobDefault("{node}.{knob}".format(node=n.Class(), knob=k.name()), "{val}".format(val=k.value()))

	# set 
	updateKnobInit(n.Class(),k.name(),k.value(),"write")

def resetToDefault():
	'''
	reset to standard knob default value
	'''

	n = nuke.thisNode()
	k = nuke.thisKnob()

	k.setValue(k.defaultValue())
	nuke.knobDefault("{node}.{knob}".format(node=n.Class(), knob=k.name()), "{val}".format(val=k.defaultValue()))
	updateKnobInit(n.Class(),k.name(),"","del")

def updateKnobInit(node,knob,value,mode):
	'''
	update knob init.py - delete or append knobDefault depending on mode
	'''

	knobDefaults = helper.openFileReturnArr(knobInit)

	if mode == "del":
		
		found = 0

		for d in knobDefaults:
			if "{node}.{knob}".format(node=node, knob=knob) in d:
				found+=1
				if ctrl == True:
					print "found in knobInit"
					print d
				knobDefaults.remove(d)
			else:
				pass
		if found < 1:
			if ctrl == True:
				print "not found in knobInit"
		
		#write new knobInit
		try:
			f = open(knobInit,'w+')
			for d in knobDefaults:
				f.write(d+"\n")
			f.close()
		except:
			nuke.message("an error occured while trying to edit the knobDefaults file")

	if mode == "write":
		#get rid of old knobDefaults of the current knob and write new knobDefault			
		updateKnobInit(node,knob,"","del")
		try:
			f = open(knobInit,'a')
			newKnobDefault = 'nuke.knobDefault("{node}.{knob}", "{val}")\n'.format(node=node, knob=knob, val=value)
			f.write(newKnobDefault)
			f.close()
		except:
			nuke.message("an error occured while trying to edit the knobDefaults file")

checkExistingInit()





