###########################################################################################################
#
#  saveImage
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  quickly save out a jpeg from selected node on your desktop or besides your nuke script
#
#  instalation
#
#  put saveImage folder in nuke home directory
#  in init.py write this line (without the '#' in the beginning):
#
#  nuke.pluginAddPath('saveImage')
#
##########################################################################################################

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke
import os
import sys
import subprocess
import datetime

def openFolder(path):
	if sys.platform == 'darwin':
		subprocess.check_call(['open', '--', path])
	elif sys.platform == 'linux2':
		subprocess.check_call(['gnome-open', '--', path])
	elif sys.platform == 'windows':
		subprocess.check_call(['explorer', path])

#get and format time for unique render paths
def getTime():
    t = str(datetime.datetime.now())
    t = t.replace(' ', '_')
    t = t.replace(':','-')
    dArr = t.split(".")
    d=dArr[0]
    return d

def createPanel():
	'''
	imageSaver panel for user
	'''
	p=nuke.Panel('ImageSaver')
	p.setWidth(400)   
	p.addEnumerationPulldown('render to', 'desktop scriptPath')
	p.addEnumerationPulldown('filetype', 'jpeg tiff png' )      
	return p

def saveImage(sel, renderTo, filetype):

	w = nuke.nodes.Write()
	w.setInput(0,sel[0])
	w.setXpos(sel[0].xpos())
	w.setYpos(sel[0].ypos()+150)
	w.knob("name").setValue("capture")
	w.knob("use_limit").setValue(True)
	w.knob("first").setValue(nuke.frame())
	w.knob("last").setValue(nuke.frame())
	w.knob("file_type").setValue(filetype)
	w.knob("file").setValue(renderTo+"capture_{time}.{ext}".format(time=getTime(), ext=filetype))
	nuke.execute(w,nuke.frame(),nuke.frame())
	nuke.delete(w)

	openFolder(renderTo)

def imageSaver():
	
	sel = nuke.selectedNodes()

	if len(sel)<1:
		nuke.message("please select a node to save an image from")
	
	elif len(sel)>1:
		nuke.message("please select only one node")

	elif len(sel)==1:

		p = createPanel()

		if p.show():

			if p.value("render to")=="scriptPath":
			 	if nuke.root().name()=="Root" or nuke.root().name() == "":
			 		nuke.message("You haven't set up your project. Please make sure to set it up first if you want to save the capture to your script.")
			 		return
				else:
					renderTo = "/".join(nuke.root().name().split("/")[:-1])+"/"
				
			else:
				renderTo = os.path.expanduser("~/Desktop/")

			filetype = p.value("filetype")
			saveImage(sel,renderTo,filetype)